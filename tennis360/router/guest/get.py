from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from http import HTTPStatus

templates = Jinja2Templates(directory="templates/guest")

async def signin(request: Request):
    
    if request.cookies.get("logged-in"):
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    return templates.TemplateResponse("signin.jinja2", {
        "request": request
    })
    
async def register(request: Request):
    
    if request.cookies.get("logged-in"):
        
        return RedirectResponse("/", HTTPStatus.FOUND)    
    
    return templates.TemplateResponse("register.jinja2", {
        "request": request
    })