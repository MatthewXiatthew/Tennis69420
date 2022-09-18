from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from database.main import session
from database.models import User

from jwt.api_jwt import decode, encode
from http import HTTPStatus

def login_user(response: Response, id):

    user = session.query(User).filter_by(id_ = id).first()

    response.set_cookie("logged-in", encode({"username" : user.username}, "secret", algorithm = "HS256"))
    
    return response
    
def delete_auth(response: Response):
    
    response.delete_cookie("logged-in")
    
    return response

def get_user(request: Request):
    
    try:
    
        username_ = decode(request.cookies.get("logged-in"), "secret", algorithms=["HS256"])
        
        return session.query(User).filter_by(username=username_.get("username")).first()
    
    except:
        
        return None
