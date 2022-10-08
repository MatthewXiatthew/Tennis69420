from starlette.requests import Request
from starlette.responses import RedirectResponse

from database.models import User, Post
from database.main import session
from authentication import get_user

from http import HTTPStatus
from frame import upload
    
async def internal_post(request: Request):
    
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    body = await request.form()
    
    session.add(newpost := Post(title=body["title"], text=body["text"], user=get_user(request)))

    session.commit()

    with open(f"/Users/matthewxia/Documents/Coding/Tennis69420/tennis360/videos/{newpost.id_}.mov", "wb") as f:
        f.write(await body["video"].read())

    newpost.link = await upload(newpost.id_)

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
    
    body = await request.form()
    
    post.title = body["title"]
    post.text = body["text"]
    
    session.commit()    
    
    return RedirectResponse("/explore", HTTPStatus.FOUND)