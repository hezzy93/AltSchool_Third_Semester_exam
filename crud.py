from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models
import schema
from sqlalchemy import func


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Create User
def create_user(db: Session, user: schema.UserCreate):
    hashed_password = pwd_context.hash(user.password.lower())
    db_user = models.User(
        email=user.email,
        last_name=user.last_name,
        first_name=user.first_name,
        sex=user.sex,
        user_name=user.user_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User by username
def get_user_by_username(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name.ilike(user_name)).first()




#Get User by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.ilike(email)).first()

#Get all users
def get_users(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.User).offset(offset).limit(limit).all()


#Create Movie
def create_movie(db: Session, movie: schema.MovieCreate,owner_id: int = None):
    db_movie = models.Movie(**movie.model_dump(),owner_id=owner_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

#Get movie by id
def get_movie_by_id(db: Session, movie_id: int):
    # Query the movie by id
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


#Delete user by id
def delete_user(db: Session, user_id: int):
    # Query the user to delete
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if db_user:
        # Delete the user
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        # Handle case where user is not found
        return {"error": "User not found"}
    

#Get all Movies
def get_movies(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(offset).limit(limit).all()


# #Get all Movies
# def get_movies(db: Session, owner_id: int = None, offset: int = 0, limit: int = 10):
#     return db.query(models.Movie).filter(models.Movie.owner_id == owner_id).offset(offset).limit(limit).all()
# def get_movies(db: Session, owner_id: int = None, offset: int = 0, limit: int = 10):
#     return db.query(models.Movie).filter(models.Movie.owner_id == owner_id). offset(offset).limit(limit).all()

# # CRUD function to get movies by owner_id
# def get_movies_by_id(db: Session, owner_id: int = None, offset: int = 0, limit: int = 10):
#     return db.query(models.Movie).filter(models.Movie.owner_id == owner_id).offset(offset).limit(limit).all()



#Get movie by id
def get_movie_by_id(db: Session, movie_id: int):
    # Query the movie by id
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

#Update movie by id
def update_movie(db: Session, movie_id: int, movie_update: schema.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        for key, value in movie_update.dict(exclude_unset=True).items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    return None

def delete_movie(db: Session, movie_id: int):
    # Query the movie to delete
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if db_movie:
        # Delete the movie
        db.delete(db_movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    else:
        # Handle case where movie is not found
        return {"error": "Movie not found"}
    
#Create Rating
def create_rating(db: Session, rating: schema.RatingCreate,owner_id: int = None, movie_id: int = None):
    db_rating = models.Rating(
        rating=rating.rating,  # Use the validated rating value
        owner_id=owner_id, 
        movie_id=movie_id)

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


# def create_rating(db: Session, rating: schema.RatingCreate, owner_id: int = None, movie_id: int = None):
#     # Create the new rating
#     db_rating = models.Rating(**rating.model_dump(), owner_id=owner_id, movie_id=movie_id)
#     db.add(db_rating)
#     db.commit()
#     db.refresh(db_rating)

#     # Update the movie's aggregate rating
#     movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
#     ratings = db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
    
#     if ratings:
#         total_ratings = sum(r.rating_value for r in ratings)
#         movie.aggregate_rating = total_ratings / len(ratings)
#         db.commit()
#         db.refresh(movie)
    
#     return db_rating



# # Get all ratings
# def get_ratings(db: Session, offset: int = 0, limit: int = 10):
#     return db.query(models.Rating).offset(offset).limit(limit).all()



# Get the cumulative rating (sum of ratings divided by 5) for a movie
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def get_cumulative_rating(db: Session, movie_id: int):
    # Query to get the movie and its ratings
    movie = db.query(models.Movie).options(joinedload(models.Movie.ratings)).filter(models.Movie.id == movie_id).first()

    if not movie:
        return None, None  # Movie not found

    # Calculate the cumulative rating
    sum_ratings = db.query(func.sum(models.Rating.rating)).filter(models.Rating.movie_id == movie_id).scalar()
    count_ratings = db.query(func.count(models.Rating.id)).filter(models.Rating.movie_id == movie_id).scalar()

    if count_ratings == 0:
        return movie.title, None  # No ratings available

    cumulative_rating = sum_ratings / (count_ratings * 5)
    return movie.title, round(cumulative_rating, 2)


#Create Comment
def create_comment(db: Session, comment: schema.CommentCreate,owner_id: int = None, movie_id: int = None):
    db_comment = models.Comment(**comment.model_dump(),owner_id=owner_id, movie_id=movie_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment



# Get all Comments for Movie
def get_all_comments(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Comment).offset(offset).limit(limit).all()

#Get comment by id
def get_comment_by_id(db: Session, comment_id: int):
    # Query the comment by id
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


#Update comment by id
def update_comment(db: Session, comment_id: int, comment_update: schema.CommentUpdate):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        for key, value in comment_update.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None


def delete_comment(db: Session, comment_id: int):
    # Query the comment to delete
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if db_comment:
        # Delete the comment
        db.delete(db_comment)
        db.commit()
        return {"message": "Comment deleted successfully"}
    else:
        # Handle case where comment is not found
        return {"error": "Comment not found"}