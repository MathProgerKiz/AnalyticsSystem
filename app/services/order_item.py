class OrderItemService:
    def __init__(self, order_item_repository):
        self.order_item_repository = order_item_repository

    async def create_order_item(self, order_item_data):
        return await self.order_item_repository.create_order_item(order_item_data)

    async def get_order_item(self, order_item_id):
        return await self.order_item_repository.get_order_item(order_item_id)

    async def get_order_items(self):
        return await self.order_item_repository.get_order_items()

    async def get_order_items_by_order(self, order_id):
        return await self.order_item_repository.get_order_items_by_order(order_id)

    async def update_order_item(self, order_item_id, order_item_data):
        return await self.order_item_repository.update_order_item(
            order_item_id,
            order_item_data,
        )

    async def delete_order_item(self, order_item_id):
        return await self.order_item_repository.delete_order_item(order_item_id)
