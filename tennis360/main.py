from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

from uvicorn import run

from router.guest.get import signin, register
from router.guest.post import internal_signin, internal_register
from router.user.get import internal_signout, post, explore, view, profile, edit
from router.user.post import internal_post, delete, internal_edit
from database.main import session
from database.models import User
from authentication import get_user

templates = Jinja2Templates(directory="templates")

async def home(request: Request):
    
    if request.cookies.get("logged-in"):

        return templates.TemplateResponse("/user/home.jinja2", {
            "request":request,
            "user" : session.query(User).filter_by(username = get_user(request).username).first()
        })
        
    return templates.TemplateResponse("/guest/home.jinja2", {
        "request": request
    })
    
async def not_found(request: Request, exc):
    
    return templates.TemplateResponse("/not_found.jinja2", {
        "request": request
    })
    
async def server_error(request: Request, exc):
    
    return templates.TemplateResponse("/server_error.jinja2", {
        "request": request
    })
    
exception_handlers = {
    404: not_found,
    500: server_error
}

app = Starlette(exception_handlers = exception_handlers, routes=[
    Route('/', home),
    Route("/signin", signin),
    Route("/register", register),
    Route("/internal/signin", internal_signin, methods=["POST"]),
    Route("/internal/register", internal_register, methods=["POST"]),
    Route("/internal/signout", internal_signout),
    Route("/post", post),
    Route("/internal/post", internal_post, methods=["POST"]),
    Route("/explore", explore),
    Route("/view/{post_id}", view),
    Route("/profile/{user_id}", profile),
    Route("/delete/{post_id}", delete),
    Route("/edit/{post_id}", edit),
    Route("/internal/edit/{post_id}", internal_edit, methods=["POST"]),  
])

app.mount("/static", app=StaticFiles(directory="static"), name="static")

run(app)
