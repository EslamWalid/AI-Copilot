import asyncio
import json
from App.Graph.builder import graph
from langchain_core.messages import HumanMessage
from App.tools.google_form import create_google_form_tool

config = {
    "configurable": {
        "thread_id": "instructor-1"
    }
}

async def main():
    while True:
        user_query = input("Enter your request: ")

        if user_query.lower() == "quit":
            break

        result = await graph.ainvoke(
            {
                "messages": [
                    HumanMessage(content=user_query)
                ]
            },
            config=config
        )

        assessment = result.get('assessment')

        if assessment is None:
            # Check if the LLM outputted a raw message instead of structured output
            last_message = result.get("messages", [])[-1]
            print(f"\n[Warning] Assessment object was not generated. Response message:")
            print(last_message.content)
            print("***********\n")
            continue

        print(f"{assessment}")

        # Call tool with safe access
        create_google_form_tool(
            form_title=assessment.form_title,
            form_description=assessment.form_description,
            payload=assessment.questions
        )

        print("***********")

if __name__ == "__main__":
    asyncio.run(main())