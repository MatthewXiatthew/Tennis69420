from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from database.main import engine

Base = declarative_base(engine)

class User(Base):
    
    __tablename__ = "User"
    
    id_ = Column("id_", Integer, primary_key = True)
    username = Column("username", String, nullable = False, unique = True)
    name = Column("name", String, nullable = False)
    password = Column("password", String, nullable = False)
    reviewer = Column("reviewer", Boolean, default = False)
    posts = relationship("Post", back_populates="user")
    
    def get_id(self):
        
        return self.id_
    
class Post(Base):
    
    __tablename__ = "Post"
    
    id_ = Column("id_", Integer, primary_key=True)
    userid = Column("userid", Integer, ForeignKey(User.id_), nullable=False)
    title = Column("title", String, nullable = False)
    text = Column("text", String, nullable=False)
    deleted = Column("deleted", Boolean, default=False, nullable=False)
    time = Column("time", DateTime, nullable=False, server_default=now())
    link = Column("link", String, nullable=False, default = "")
    user = relationship("User", back_populates="posts")
    
    
Base.metadata.create_all(engine)