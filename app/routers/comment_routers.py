from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from app.db.config import SessionLocal
from app.db import comment
from app.schemas.comment_schemas import CommentResponse, RequestComment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.get("/")
async def get(db:Session=Depends(get_db)):
    try:
        _comments = comment.get_comment(db, 0, 100)
        return CommentResponse(code=200, status="ok", message="Success fetch data", result=_comments).dict(exclude_none=True)
    except:
        return CommentResponse(code=401, status="fail",message="Something was wrong")

@router.get("/left/to/approve")
async def get(db:Session=Depends(get_db)):
    try:
        _comments = comment.get_comment_left_to_approve(db)
        return CommentResponse(code=200, status="ok", message="Success fetch data", result=_comments).dict(exclude_none=True)
    except:
        return CommentResponse(code=401, status="fail",message="Something was wrong")

@router.get("/{post_id}")
async def get_comment(post_id, db:Session=Depends(get_db)):
    try:
        intId = int(post_id)
 
        _comment = comment.get_comment_by_post(db, intId)
 
        if _comment == []:
            return CommentResponse(code=401, status='fail', message='This post has not comments')
    
        return CommentResponse(code=200, status='ok', message='Success fetch comment', result=_comment).dict(exclude_none=True)
    except:
        return CommentResponse(code=401, status="fail",message="Can not get comments")

@router.post("/update/{comment_id}")
async def update_comment(request:RequestComment, comment_id, db:Session=Depends(get_db)):
    try:
        intId = int(comment_id)
        exist_comment = comment.get_comment_by_id(db, intId)
        if exist_comment == None:
            return CommentResponse(code=200, status="ok",message="Comment not found")

        _comment = comment.update_comment(db, request, intId)

        if _comment is None:
            return CommentResponse(
                code=404,
                status='Fail',
                message='Comment can not be updating',
                result=_comment
            )

        return CommentResponse(
            code=200,
            status="ok",
            message="Update successfully"
        )
    except:
        return CommentResponse(code=401, status="fail",message="Something was wrong")

@router.delete("/delete/{comment_id}")
async def update_comment(comment_id, db:Session=Depends(get_db)):
    try:
        exist_comment = comment.get_comment_by_id(db, comment_id)
        if exist_comment == None:
            return CommentResponse(code=200, status="ok",message="the comment does not exist")

        comment.remove_comment(db, comment_id)
        return CommentResponse(code=200, status="ok",message="success delete comment")
    except:
        return CommentResponse(code=401, status="fail",message="Something was wrong")

@router.post("/create")
async def create(request:RequestComment, db:Session=Depends(get_db)):
    try:
        _new_comment = comment.create_comment(db, request)
        if _new_comment is None:
            return  CommentResponse(code=404, status="fail", message="Comment can not be create")

        return CommentResponse(code=200, status="ok", message="Comment was create successfully", result=_new_comment).dict(exclude_none=True)
    except:
        return CommentResponse(code=404, status="fail", message="Something was wrong")
