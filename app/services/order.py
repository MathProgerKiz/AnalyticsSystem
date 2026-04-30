class OrderService:
    def __init__(self, order_repository):
        self.order_repository = order_repository

    async def create_order(self, order_data):
        return await self.order_repository.create_order(order_data)

    async def get_order(self, order_id):
        return await self.order_repository.get_order(order_id)

    async def get_orders(self):
        return await self.order_repository.get_orders()

    async def update_order(self, order_id, order_data):
        return await self.order_repository.update_order(order_id, order_data)

    async def delete_order(self, order_id):
        return await self.order_repository.delete_order(order_id)
