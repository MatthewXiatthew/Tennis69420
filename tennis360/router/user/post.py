from starlette.requests import Request
from starlette.responses import RedirectResponse

from helper import body_as_json
from database.models import User, Post
from database.main import session
from authentication import get_user

from http import HTTPStatus
    
async def internal_post(request: Request):
    
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    body = await body_as_json(request, ["title", "text"])
    
    title_ = body.get("title")
    text_ = body.get("text")
    
    session.add(Post(title=title_, text=text_, user=get_user(request)))
    
    session.commit()
    
    return RedirectResponse("/explore", HTTPStatus.FOUND)

async def delete(request: Request):
    
    user = get_user(request)

    if user is None:

        return RedirectResponse("/sign-in", HTTPStatus.FOUND)
        
    id_ = request.path_params.get("post_id")

    post = session.query(Post).filter_by(id_ = id_).first()
    
    
    
    if user.id_ != post.user.id_:

        return RedirectResponse("/", HTTPStatus.FOUND)
    
    post.deleted = True

    session.commit()
    
    return RedirectResponse("/explore", HTTPStatus.FOUND)

async def internal_edit(request: Request):
    
    user = get_user(request)
    post = session.query(Post).filter_by(id_=request.path_params.get("post_id")).first()
    
    if user is None:
        
        return RedirectResponse("/sign-in", HTTPStatus.FOUND)
    
    if user.id_ != post.user.id_:

        return RedirectResponse("/", HTTPStatus.FOUND)
    
    body = await body_as_json(request, ["title", "text"])
    
    post.title = body.get("title")
    post.text = body.get("text")
    
    session.commit()    
    
    return RedirectResponse("/explore", HTTPStatus.FOUND)