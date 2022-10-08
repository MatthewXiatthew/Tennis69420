from starlette.requests import Request
from starlette.responses import RedirectResponse

from database.models import User
from database.main import session
from authentication import login_user

from http import HTTPStatus

async def internal_register(request: Request):
    
    body = await request.form()

    reviewer_ = False
    if (body["reviewer"] == "reviewer"):
        reviewer_ = True
    elif (body["reviewer"] == "user"):
        reviewer_ = False

    if (session.query(User).filter_by(username = body["username"]).first()):
        return RedirectResponse("/register", HTTPStatus.FOUND)

    session.add(User(username=body["username"], password=body["password"], name=body["name"], reviewer=reviewer_))
    
    session.commit()
    
    return RedirectResponse("/signin", HTTPStatus.FOUND)
    
async def internal_signin(request: Request):
    
    body = await request.form()
    
    user = session.query(User).filter_by(username = body["username"]).first()
    
    if user is None or user.password != body["password"]:
        
        return RedirectResponse("/", HTTPStatus.FOUND)
    
    else:

        return login_user(RedirectResponse("/", HTTPStatus.FOUND), user.id_)