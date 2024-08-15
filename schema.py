from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from typing import List, TYPE_CHECKING

# Conditional import to avoid circular import issues
if TYPE_CHECKING:
    from models import Comment

#User Schema
class UserBase(BaseModel):
    last_name: str
    first_name: str
    user_name: str
    email: str
    sex: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SignupResponse(BaseModel):
    message: str
    user: User

#Movie Schema   
class MovieBase(BaseModel):
    title: str
    director: str
    year : int

    model_config = ConfigDict(from_attributes=True)

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    owner_id: int
    comments: List["Comment"] = []  # Use string annotation for forward reference
    rating: List["Rating"] = []

    model_config = ConfigDict(from_attributes=True)

class MovieUpdate(MovieBase):
    pass

    model_config = ConfigDict(from_attributes=True)

# Comment Schema
class CommentBase(BaseModel):
    comment: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    comment: str
    movie_id: int
    owner_id: int

class CommentUpdate(CommentBase):
    pass


    model_config = ConfigDict(from_attributes=True)

# Rating Schema
class RatingBase(BaseModel):
    rating: int

    @field_validator('rating')
    def validate_rating(cls, value):
        if not (0 <= value <= 5):
            raise ValueError('Rating must be between 0 and 5')
        return value

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
# Rebuild models to handle forward references
Movie.model_rebuild()
Comment.model_rebuild()