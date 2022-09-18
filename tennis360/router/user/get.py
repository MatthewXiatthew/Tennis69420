from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from database.models import User, Post
from database.main import session
from authentication import delete_auth, get_user

from http import HTTPStatus

templates = Jinja2Templates(directory = "templates/user")

async def internal_signout(request: Request):
    
    return delete_auth(RedirectResponse("/", HTTPStatus.FOUND))

async def post(request: Request):
    
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    return templates.TemplateResponse("post.jinja2", {
        "request": request
    })
    
async def explore(request: Request):
    
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)

    return templates.TemplateResponse("explore.jinja2", {
        "request": request ,
        "posts": session.query(Post).filter_by(deleted=False).order_by(Post.time.desc()).all()
    })
    
async def view(request: Request):
    
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    

    post_id = request.path_params.get("post_id")
    post = session.query(Post).filter_by(id_ = post_id).first()
    
    if get_user(request).id_ != post.user.id_:
        
        return templates.TemplateResponse("view.jinja2", {
            "request": request,
            "post": post
        })
        
    else:

        return templates.TemplateResponse("userpost.jinja2", {
            "request": request,
            "post": post
        })
    
async def profile(request: Request):
        
    if not get_user(request):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    user_id = request.path_params.get("user_id")
    
    return templates.TemplateResponse("profile.jinja2", {
        "request": request,
        "user": session.query(User).filter_by(id_ = user_id).first()
    })
    
async def edit(request: Request):
    
    post_id = request.path_params.get("post_id")
    user = get_user(request)
    post = session.query(Post).filter_by(id_ = post_id).first()
    
    if not user:
        
        return RedirectResponse("/sign-in", HTTPStatus.FOUND)
    
    if user.id_ != post.user.id_:
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    return templates.TemplateResponse("edit.jinja2", {
        "request": request ,
        "post": post
    })