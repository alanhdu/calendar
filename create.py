from cal import app
from cal.schema import db, Event, User
from cal.fb import update_fb_events

with app.app_context():
    db.create_all()
    update_fb_events()
