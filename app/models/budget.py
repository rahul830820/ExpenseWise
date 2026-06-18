from sqlalchemy import Column, Integer, Float, ForeignKey

from sqlalchemy.orm import relationship

from app.db.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = relationship("Category")

    user = relationship("User")
