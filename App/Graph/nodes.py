from App.Agents.AssessmentAgent.agent import AssessmentGenerationAgent
from App.Agents.Router.router import Router
from App.tools.google_form import create_google_form_tool




assessment_agent = AssessmentGenerationAgent()
router_agent = Router()

async def assessment_node(state):
    return await assessment_agent.ainvoke(state)

async def router_node(state):
    return await router_agent.ainvoke(state)