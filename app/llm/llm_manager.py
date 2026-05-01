from datetime import datetime
import json

from langchain_core.messages import ToolMessage

from app.llm.llm_agents.gigachat import get_gigachat
from app.llm.tools.analytics_tools import (
    ANALYTICS_TOOL_SCHEMAS,
    get_analytics_tool_method,
)


class LLMManager:
    def __init__(self):
        self.agent = get_gigachat()

    async def generate_response(self, prompt: str, analytics_repository) -> str:
        llm_with_tools = self.agent.bind_tools(ANALYTICS_TOOL_SCHEMAS)
        ai_message = await llm_with_tools.ainvoke(
            [
                {
                    "role": "system",
                    "content": f"""
                Ты аналитический ассистент.

                ТЕКУЩЕЕ ВРЕМЯ:
                {datetime.now().isoformat()}

                ВАЖНО:
                - НЕ вычисляй даты самостоятельно
                - Всегда используй tools
                - Если пользователь говорит "последний месяц", "неделя" → передай period в tool
                - Никогда не подставляй даты вручную
                """,
                },
                {"role": "user", "content": prompt},
            ]
        )

        if not ai_message.tool_calls:
            return ai_message.content

        tool_call = ai_message.tool_calls[0]
        tool_args = tool_call.get("args") or tool_call.get("arguments") or {}
        if isinstance(tool_args, str):
            tool_args = json.loads(tool_args)

        method = get_analytics_tool_method(
            analytics_repository=analytics_repository,
            name=tool_call["name"],
        )

        result = await method(**tool_args)
        tool_call_id = str(tool_call.get("id") or tool_call["name"])
        tool_content = json.dumps(result, ensure_ascii=False, default=str)

        final = await llm_with_tools.ainvoke(
            [
                {"role": "user", "content": prompt},
                ai_message,
                ToolMessage(
                    content=tool_content,
                    name=tool_call["name"],
                    tool_call_id=tool_call_id,
                ),
            ]
        )

        return final.content
