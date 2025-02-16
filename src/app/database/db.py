import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func

# Database setup using SQLAlchemy ORM
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Chat(Base):
    """Represents a chat session in the database."""
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)  # Optional title for the chat
    created_at = Column(DateTime, default=func.now())  # Timestamp when the chat is created
    deleted = Column(Boolean, default=False)  # Flag indicating if the chat is deleted
    last_message_at = Column(DateTime, default=func.now())  # Timestamp of the last message in the chat
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")  # Relationship with messages

class Message(Base):
    """Represents an individual message within a chat session."""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)  # Foreign key linking to a chat
    role = Column(String, nullable=False)  # Role of the message sender (e.g., 'user', 'model')
    prompt = Column(String, nullable=True)  # Optional prompt associated with the message
    content = Column(Text, nullable=False)  # Content of the message
    timestamp = Column(DateTime, default=func.now())  # Timestamp when the message is created
    chat = relationship("Chat", back_populates="messages")  # Relationship with the chat

# Create all tables in the database
Base.metadata.create_all(engine)

def create_new_chat():
    """Creates a new chat record in the database and returns its ID."""
    new_chat = Chat()
    session.add(new_chat)
    session.commit()
    return new_chat.id

def get_chat_title(chat_id):
    """Retrieves the title of a chat by its ID."""
    return session.query(Chat).filter_by(id=chat_id).first().title

def save_chat_title(chat_id, title):
    """Updates the title of a chat with the given ID."""
    chat = session.query(Chat).filter_by(id=chat_id).first()
    chat.title = title
    session.commit()

def save_message(chat_id, role, content, prompt=None):
    """Saves a new message to the specified chat."""
    new_message = Message(chat_id=chat_id, role=role, content=content, prompt=prompt)
    session.add(new_message)

    chat = session.query(Chat).filter_by(id=chat_id).first()
    chat.last_message_at = datetime.now()
    session.commit()

def delete_chat(chat_id):
    """Marks a chat as deleted without removing it from the database."""
    chat = session.query(Chat).filter_by(id=chat_id).first()
    chat.deleted = True
    session.commit()

def get_chats():
    """Retrieves all chats ordered by the last message timestamp in descending order."""
    return session.query(Chat).order_by(Chat.last_message_at.desc()).all()

def get_chat_messages(chat_id):
    """Retrieves all messages associated with a chat, ordered by their timestamp in ascending order."""
    return session.query(Message).filter_by(chat_id=chat_id).order_by(Message.timestamp.asc()).all()
