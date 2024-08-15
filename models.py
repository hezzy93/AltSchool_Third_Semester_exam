from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    sex = Column(String, index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationship with movies
    movies = relationship("Movie", back_populates="owner", cascade="all, delete-orphan")
    # Relationship with comments
    comments = relationship("Comment", back_populates="owner", cascade="all, delete-orphan")

    # Relationship with ratings
    ratings = relationship("Rating", back_populates="owner", cascade="all, delete-orphan")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    director = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    year = Column(Integer, index=True)

    # Relationship with owner (User)
    owner = relationship("User", back_populates="movies")

    # Relationship with comments
    comments = relationship("Comment", back_populates="movie", cascade="all, delete-orphan")

    # Relationship with comments
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)  # Use lowercase 'comment'
    owner_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey('movies.id'))


    #Relationship with owner (User)
    owner = relationship("User", back_populates= "comments")
    # Relationship with movies
    movie = relationship("Movie", back_populates="comments")

# alembic revision --autogenerate -m "Add movie_id to ratings"
class Rating(Base):
    __tablename__ ="ratings"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey('movies.id'))

    #Relationship with owner (User)
    owner = relationship("User", back_populates= "ratings")

    #Relationship with movie
    movie = relationship("Movie", back_populates="ratings")