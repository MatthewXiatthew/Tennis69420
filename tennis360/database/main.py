from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import Session

engine = create_engine("sqlite:///database.sqlite3")

session = Session(engine)