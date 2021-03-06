import datetime as dt
import json
from os.path import join

from sqlalchemy_searchable import make_searchable
import pytest

from config import BASEDIR


@pytest.yield_fixture(scope="session")
def app(request):
    from cal import app
    with app.app_context():
        yield app

@pytest.yield_fixture(scope="session")
def db(app, request):
    from cal import db

    db.init_app(app)
    db.configure_mappers()
    db.create_all()
    make_searchable()

    yield db

    db.session.close()  # prevent py.test from hanging
    db.drop_all()


@pytest.fixture(scope="session")
def User(app, db):
    from cal import User

    db.session.add_all([User(id=1, name="Cthulhu", fb_id=1),
                        User(id=2, name="Monty Python", fb_id=2),
                        User(id=3, name="Sauron", fb_id=3)])
    db.session.commit()

    return User


@pytest.fixture(scope="session")
def Event(app, db, User):
    from cal import Event

    start = dt.datetime(2015, 3, 14)  # Saturday
    day = dt.timedelta(days=1)

    with open(join(BASEDIR, "tests/events.json")) as fin:
        events = json.load(fin)

    for event in events:
        event["start"] = start + day * event["start"]
        if "end" in event:
            event["end"] = start + day * event["end"]
        event["description"] = ""
        db.session.add(Event(**event))

    db.session.commit()

    return Event
