

from app.dependency import analytics
from app.llm.llm_agents.gigachat import get_gigachat
from app.llm.tools.analytics_tools import ANALYTICS_TOOL_SCHEMAS, get_analytics_tool_method


class LLMManager:
    def __init__(self):
        self.agent = get_gigachat()
    
    async def generate_response(self, prompt: str) -> str:
        llm_with_tools = self.agent.bind_tools(ANALYTICS_TOOL_SCHEMAS)

        ai_message = await llm_with_tools.ainvoke([
            {"role": "user", "content": prompt}
        ])

        if not ai_message.tool_calls:
            return ai_message.content

        tool_call = ai_message.tool_calls[0]

        method = get_analytics_tool_method(
            name=tool_call["name"]
        )

        result = await method(**tool_call["arguments"])

    
        final = await llm_with_tools.ainvoke([
            {"role": "user", "content": prompt},
            ai_message,
            {
                "role": "tool",
                "name": tool_call["name"],
                "content": str(result)
            }
        ])

        return final.content