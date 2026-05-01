

class AnalyticsService:
    
    @staticmethod   
    async def query(prompt: str, analytics_repository) -> str:
        from app.llm.llm_manager import LLMManager

        llm_manager = LLMManager()

        response = await llm_manager.generate_response(prompt, analytics_repository)

        return response
