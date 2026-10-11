from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from database import Base

class Tea(Base):
    __tablename__ = "teas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)