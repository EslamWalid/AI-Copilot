from App.Agents.Router.schema import RouterState
from App.Agents.Router.prompt import ROUTER_SYSTEM_PROMPT
from App.LLM.client import get_client_router, get_client_fallback
from langchain_core.messages import SystemMessage, AIMessage
from App.utils.logger import get_logger

logger = get_logger(__name__)


class Router:

    def __init__(self):

        main = get_client_router().with_structured_output(RouterState)

        fallback = get_client_fallback().with_structured_output(RouterState)

        self.llm = main.with_fallbacks([fallback])

    async def ainvoke(self, state):

        logger.info("Router Agent invoked")

        messages = [
            SystemMessage(
                content=ROUTER_SYSTEM_PROMPT
            )
        ]

        # --------------------------------
        # Current Assessment
        # --------------------------------

        has_assessment = state.get("assessment") is not None

        messages.append(
            SystemMessage(
                content=(
                    f"An assessment currently exists: {has_assessment}"
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

            # Don't resend previous generated router state
            if isinstance(msg, AIMessage):
                continue

            messages.append(msg)

        # --------------------------------
        # LLM
        # --------------------------------
        result = await self.llm.ainvoke(messages)

        return result