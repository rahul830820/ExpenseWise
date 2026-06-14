from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    description = Column(
        String(255),
        nullable=False
    )

    expense_date = Column(
        Date,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    category = relationship(
        "Category"
    )

    user = relationship(
        "User"
    )