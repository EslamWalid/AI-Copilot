from App.Agents.AssessmentAgent.schema import Assessment
from App.Agents.Router.schema import RouterState
from langgraph.graph import MessagesState



class InstructorState(MessagesState):

    assessment: Assessment | None
    router_state: RouterState | None