

from sqlalchemy import Integer,Mapped


from app.core.database import Base 


class Order(Base):
    __tablename__ = 'orders'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
