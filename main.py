from fastapi import Depends, FastAPI, HTTPException
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import authenticate_user, create_access_token, get_current_user
import crud, models, schema
from database import SessionLocal, engine, Base, get_db
from crud import pwd_context
from logger import get_logger

logger = get_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()


# Endpoint to signup/ User registration
@app.post("/users_Signup/", response_model=schema.SignupResponse, tags=["Signup"])
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    logger.info('Creating user...')
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"User with {user.email} already exists.")
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, user_name=user.user_name)
    if db_user:
        logger.warning(f"User with {user.user_name} already exists.")
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info('User successfully created.')
    created_user = crud.create_user(db=db, user=user)
    return {"message": "Account created successfully", 
            "user": created_user}
    


#Endpoint to login/ User login
@app.post("/users_Login/", tags=["Login"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Generating authentication token...")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_name})
    logger.info(f"Token generated for {user.user_name}")
    return {"access_token": access_token, "token_type": "bearer", "message": "Successful login"}


# Endpoint to GET all users
@app.get("/users/", response_model=List[schema.User], tags=["Users"])
def get_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users

# Endpoint to GET a user by username
@app.get("/users/username/{username}", response_model=schema.User, tags=["Users"])
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Username not found")
    return db_user

#Endpoint to GET a user by email
@app.get("/users/{email/{email}}", response_model=schema.User, tags=["Users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint to DELETE a user by Id
@app.delete("/users/{user_id}", response_model=dict, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = crud.delete_user(db, user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# Endpoint to get a movie by id | View a movie added (public access)
@app.get("/movies/{movie_id}", response_model=schema.Movie, tags=["Movies"])
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


#Endpoint to create movies | Add a movie (authenticated access)
@app.post('/movies/', tags=["Movies"])
def create_movie(payload: schema.MovieCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie = crud.create_movie(
        db, 
        payload,
        owner_id=user.id
    )
    return {'message': 'success', 'data': movie}

# Endpoint to retrieve all movies | View all movies (public access)
@app.get("/movies/", response_model=List[schema.Movie], tags=["Movies"])
def get_movies(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    movies = crud.get_movies(db, offset=offset, limit=limit)
    return movies

#Endpoint to update movies | Edit a movie (only by the user who listed it)
@app.put("/movies/{movie_id}", tags=["Movies"])
def update_movie(movie_id: int, payload: schema.MovieUpdate, user: schema.User= Depends (get_current_user), db: Session = Depends(get_db)):
    updated_movie = crud.update_movie(
        db=db,
        movie_id= movie_id,
        movie_update=payload
        )
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {'message': 'success', 'data':updated_movie}

# Endpoint to delete a movie | Delete a movie (only by the user who listed it)
@app.delete("/movies/{movie_id}", response_model=dict, tags=["Movies"])
def delete_movie(movie_id: int, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = crud.delete_movie(db=db, movie_id=movie_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


#Endpoint to create rating | Rate a movie (authenticated access)
@app.post('/ratings', tags=["Ratings"])
def create_rating_for_movie(movie_id: int, payload: schema.RatingCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
            # Check if the movie exists
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie id not found")
# Create the rating
    rating = crud.create_rating(
        db, 
        payload,
        owner_id=user.id,
        movie_id=movie_id
    )
    return {'message': 'success', 'data': rating}


# Endpoint to retrieve ratings | Get ratings for a movie (public access)
# @app.get("/ratings/", response_model=List[schema.Rating], tags=["Ratings"])
# def get_ratings(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
#     return crud.get_ratings(db, offset=offset, limit=limit)

from fastapi import HTTPException

# Endpoint to retrieve the cumulative rating for a movie (public access)
@app.get("/ratings/cumulative/", tags=["Ratings"])
def get_cumulative_rating(movie_id: int, db: Session = Depends(get_db)):
    movie_title, cumulative_rating = crud.get_cumulative_rating(db, movie_id=movie_id)
    
    if cumulative_rating is None:
        raise HTTPException(status_code=404, detail="Movie not found or no ratings available")
    
    return {"movie_id": movie_id, "movie_title": movie_title, "rating": cumulative_rating}


#Endpoint to create comment | Add a comment to a movie (authenticated access)
@app.post('/comments', tags=["Comments"])
def create_comment_for_movie(movie_id: int, payload: schema.CommentCreate, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Check if the movie exists
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie id not found")
# Create the comment
    comment = crud.create_comment(
        db, 
        payload,
        owner_id=user.id,
        movie_id=movie_id
    )
    return {'message': 'success', 'data': comment}

# Endpoint to retrieve comment by comment_id | View comments for a movie (public access)
@app.get("/comments/{comment_id}/", response_model=schema.Comment, tags=["Comments"])
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment_by_id(db=db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

# Endpoint to retrieve all comments
@app.get("/comments/", response_model=List[schema.Comment], tags=["Comments"])
def get_comments(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    comments = crud.get_all_comments(db, offset=offset, limit=limit)
    return comments

#Endpoint to update comments | Add comment to a comment i.e nested comments (authenticated access)
@app.put("/comments/{comment_id}", tags=["Comments"])
def update_comment(comment_id: int, payload: schema.CommentUpdate, user: schema.User= Depends (get_current_user), db: Session = Depends(get_db)):
    updated_comment = crud.update_comment(
        db=db,
        comment_id=comment_id,
        comment_update=payload
        )
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_comment





# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}



# # Endpoint to delete a movie
# @app.delete("/comments/{comment_id}", response_model=dict, tags=["Comments"])
# def delete_comment(movie_id: int, user: schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     result = crud.delete_comment(db, comment_id)
#     if "error" in result:
#         raise HTTPException(status_code=404, detail=result["error"])
#     return result