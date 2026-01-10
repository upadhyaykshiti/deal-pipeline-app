
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import api from "../api";
import Navbar from "../components/Navbar";   

const STAGES = ["Sourced", "Screen", "Diligence", "IC", "Invested", "Passed"];

export default function Kanban() {
  const [deals, setDeals] = useState([]);
  const [activityMap, setActivityMap] = useState({});
  const navigate = useNavigate();

  const role = localStorage.getItem("role");

  useEffect(() => {
    loadDeals();
  }, []);

  async function loadDeals() {
    const dealsRes = await api.get("/deals/");
    setDeals(dealsRes.data);

    const actRes = await api.get("/activities/latest");
    setActivityMap(actRes.data);
  }

  async function moveDeal(id, newStage) {
    await api.post(`/deals/${id}/move?stage=${newStage}`);
    loadDeals();
  }

  async function createDeal() {
    const name = prompt("Deal name?");
    if (!name) return;
    await api.post("/deals", { name });
    loadDeals();
  }

  function onDragEnd(result) {
    if (role === "partner") return;

    const { draggableId, destination } = result;
    if (!destination) return;

    const newStage = destination.droppableId;
    const dealId = parseInt(draggableId);

    const deal = deals.find(d => d.id === dealId);
    if (!deal) return;

    if (deal.ic_locked) return;
    if (role === "analyst" && deal.stage === "IC") return;
    if (deal.stage === newStage) return;

    moveDeal(dealId, newStage);
  }

  const dealsByStage = STAGES.reduce((acc, stage) => {
    acc[stage] = deals.filter(d => d.stage === stage);
    return acc;
  }, {});

  return (
    <>
      {/* 🔹 NAVBAR */}
      <Navbar />

      {/* 🔹 KANBAN */}
      <div style={{ padding: 20 }}>
        {role !== "partner" && (
          <button onClick={createDeal}>+ New Deal</button>
        )}

        <DragDropContext onDragEnd={onDragEnd}>
          <div style={{ display: "flex", gap: 20, marginTop: 20 }}>
            {STAGES.map(stage => (
              <Droppable droppableId={stage} key={stage}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    style={{
                      width: 260,
                      minHeight: 500,
                      border: "1px solid #ccc",
                      borderRadius: 4,
                      padding: 10,
                      background: "#f7f7f7"
                    }}
                  >
                    <h3>{stage}</h3>

                    {dealsByStage[stage].map((d, index) => (
                      <Draggable
                        key={d.id}
                        draggableId={d.id.toString()}
                        index={index}
                        isDragDisabled={
                          role === "partner" || d.ic_locked
                        }
                      >
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            style={{
                              ...provided.draggableProps.style,
                              border: "1px solid #ccc",
                              borderRadius: 4,
                              marginBottom: 8,
                              padding: 8,
                              background: "white",
                              fontSize: 13,
                              cursor:
                                role === "partner" || d.ic_locked
                                  ? "not-allowed"
                                  : "grab",
                              opacity: d.ic_locked ? 0.6 : 1
                            }}
                            onClick={() =>
                              navigate(`/deals/${d.id}/memo`)
                            }
                          >
                            <b>{d.name}</b>
                            <div>Company: {d.company_url || "-"}</div>
                            <div>Round: {d.round || "-"}</div>
                            <div>Check: {d.check_size || "-"}</div>
                            <div>Status: {d.status || "-"}</div>

                            {activityMap[d.id] && (
                              <div
                                style={{
                                  marginTop: 6,
                                  color: "#666",
                                  fontSize: 12
                                }}
                              >
                                🕒 {activityMap[d.id].action}
                              </div>
                            )}
                          </div>
                        )}
                      </Draggable>
                    ))}

                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            ))}
          </div>
        </DragDropContext>
      </div>
    </>
  );
}
