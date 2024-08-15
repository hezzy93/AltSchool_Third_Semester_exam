# #Create Comment
# def create_comment(db: Session, comment: schema.CommentCreate):
#     db_comment = models.Comment(**comment.model_dump())
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment


# # # Endpoint to create a comment for a movie
# # @app.post("/movies/{movie_id}/comments/", response_model=schema.Comment)
# # def create_comment_for_movie(movie_id: int, owner_id: int, comment: schema.CommentCreate, db: Session = Depends(get_db)):
# #     return crud.create_comment(db=db, comment=comment, movie_id=movie_id, owner_id=owner_id)

# # # Endpoint to retrieve movies
# # @app.get("/movies/", response_model=dict)
# # def get_movies(db: Session = Depends(get_db), owner_id: schema.User =Depends(get_current_user), offset: int = 0, limit: int = 10):
# #     movies = crud.get_movies(db, owner_id=owner_id, offset=offset, limit=limit)
# #     return {"message": "success", "data": movies}


# # @app.post("/movies/", response_model=schema.Movie)
# # def create_movie(movie: schema.MovieCreate, db: Session = Depends(get_db)):
# #     return crud.create_movie(db=db, movie=movie)


# # Create Comment
# def create_comment(db: Session, comment: schema.CommentCreate, movie_id: int, owner_id: int):
#     db_comment = models.Comment(comment=comment.comment, movie_id=movie_id, owner_id=owner_id)
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment

# #Endpoint to update movies
# @app.put("/movies/{movie_id}", response_model=schema.Movie)
# def update_movie(movie_id: int, movie_update: schema.MovieUpdate, db: Session= Depends(get_db)):
#     updated_movie = crud.update_movie(db=db, movie_id=movie_id, movie_update=movie_update)
#     if updated_movie is None:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return updated_movie

# # Create Rating
# def create_rating(db: Session, rating: schema.RatingCreate):
#     db_rating = models.Rating(rating=rating.rating)
#     db.add(db_rating)
#     db.commit()
#     db.refresh(db_rating)
#     return db_rating