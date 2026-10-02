from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver


from App.Graph.state import InstructorState

from App.Graph.nodes import assessment_node, router_node


builder = StateGraph(InstructorState)

builder.add_node(
    "assessment",
    assessment_node
)

builder.add_node(
    "router",
    router_node
)


builder.set_entry_point(
    "assessment"
)

builder.set_finish_point(
    "assessment"
)

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)