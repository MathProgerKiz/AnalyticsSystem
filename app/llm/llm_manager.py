

from app.llm.llm_agents.gigachat import get_gigachat


class LLMManager:
    def __init__(self):
        self.agent = get_gigachat()
    
    async def generate_response(self, prompt: str) -> str:
        pass

