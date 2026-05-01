

class AnalyticsService:
    
    @staticmethod   
    async def query(prompt: str) -> str:
        from app.llm.llm_manager import LLMManager

        llm_manager = LLMManager()

        response = await llm_manager.generate_response(prompt)

        return response