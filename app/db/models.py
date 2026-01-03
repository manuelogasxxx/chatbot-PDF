#contains models for PostgreSQL<->SQLAlchemy


from datetime import datetime
from sqlalchemy import (
    String, Text, Integer, ForeignKey, DateTime,
    CheckConstraint, Table,Column
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from .base import Base

# ... clases User, Chat, Document, Message
# ... tabla chats_documents
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False
    )

    register_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        CheckConstraint("char_length(username) >= 4", name="ck_username_len"),
    )

    chats = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    fk_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    creation_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        CheckConstraint("char_length(title) >= 1", name="ck_title_len"),
    )

    user = relationship("User", back_populates="chats")

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.sent_date"
    )


    documents = relationship(
        "Document",
        secondary="chats_documents",
        back_populates="chats"
    )


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    file_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    file_route: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    fk_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    load_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    user = relationship("User", back_populates="documents")

    chats = relationship(
        "Chat",
        secondary="chats_documents",
        back_populates="documents"
    )

#tabla auxiliar
chats_documents = Table(
    "chats_documents",
    Base.metadata,
    Column(
        "fk_chat_id",
        Integer,
        ForeignKey("chats.chat_id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "fk_document_id",
        Integer,
        ForeignKey("documents.document_id", ondelete="CASCADE"),
        primary_key=True
    )
)

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    fk_chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.chat_id", ondelete="CASCADE"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(10), nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    sent_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="ck_message_role"
        ),
    )

    chat = relationship("Chat", back_populates="messages")


