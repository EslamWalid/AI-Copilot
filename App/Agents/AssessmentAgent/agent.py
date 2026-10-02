from langchain_core.messages import SystemMessage, AIMessage

from App.LLM.client import get_client_main, get_client_fallback
from App.tools.google_form import create_google_form_tool

from App.Agents.AssessmentAgent.prompt import ASSESSMENT_AGENT_SYSTEM_PROMPT
from App.Agents.AssessmentAgent.schema import Assessment

from App.utils.logger import get_logger

logger = get_logger(__name__)

llm_main = get_client_main()
llm_fallback = get_client_fallback()


class AssessmentGenerationAgent:

    def __init__(self):

        main = llm_main.with_structured_output(Assessment)

        fallback = llm_fallback.with_structured_output(Assessment)

        self.llm = main.with_fallbacks([fallback])

    async def ainvoke(self, state):
        logger.info("Assessment Generation Agent invoked")

        messages = [
            SystemMessage(
                content = ASSESSMENT_AGENT_SYSTEM_PROMPT
            )
        ]

        # --------------------------------
        # Current Assessment
        # --------------------------------

        current_assessment = state.get("assessment")

        if current_assessment:

            messages.append(
                SystemMessage(
                    content=(
                        "Current assessment:\n\n"
                        f"{current_assessment.model_dump_json()}"
                    )
                )
            )

        # --------------------------------
        # Chat History
        # --------------------------------

        for msg in state.get("messages", []):

            # Don't resend system messages
            if isinstance(msg, SystemMessage):
                continue

            # Don't resend previous generated assessment
            if isinstance(msg, AIMessage):
                continue

            messages.append(msg)

        # --------------------------------
        # LLM
        # --------------------------------

        result = await self.llm.ainvoke(messages)

        # --------------------------------
        # State Update
        # --------------------------------

        return {"assessment": result}
