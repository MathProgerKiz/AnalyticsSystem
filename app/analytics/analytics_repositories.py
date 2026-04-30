

class AnalicsRepository:
    def __init__(self, db):
        self.db = db
    
    async def get_top_selling_products(self, limit: int = 10):
    
