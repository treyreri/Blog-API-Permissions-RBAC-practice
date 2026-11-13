from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(40) , unique= True, index= True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    role : Mapped[str] = mapped_column(String(20) , default = "user")
    is_active: Mapped[bool] = mapped_column(default = True)

class Post(Base):
    __tablename__ = "posts"
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(200))
    content : Mapped[str] = mapped_column(Text)
    is_hidden: Mapped[bool] = mapped_column(default = False)
    author_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at : Mapped[datetime] = mapped_column( DateTime(timezone=True) , server_default=func.now())
    