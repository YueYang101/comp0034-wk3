from flask import current_app as app


@app.route('/')
def hello():
    return f"Hello!"

from paralympics.schemas import RegionSchema, EventSchema

# Flask-Marshmallow Schemas
regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()
events_schema = EventSchema(many=True)
event_schema = EventSchema()


# Use route and specify the HTTP method(s). If you do not specify the methods then it will default to GET.
@app.route('/something', methods=['GET', 'POST'])
def something():
    pass


# Use Flask shortcut methods for each HTTP method `.get`, `.post`, `.delete`, `.patch`, `.put`
@app.get('/something')
def something():
    pass

from paralympics import db
from paralympics.models import Region

@app.get("/regions")
def get_regions():
    """Returns a list of NOC region codes and their details in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_regions = db.session.execute(db.select(Region)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = regions_schema.dump(all_regions)
    # Return the data
    return result


from paralympics.models import Event

@app.get("/events/<event_id>")
def get_event(event_id):
    """ Returns the event with the given id JSON.

    :param event_id: The id of the event to return
    :param type event_id: int
    :returns: JSON
    """
    event = db.session.execute(
        db.select(Event).filter_by(id=event_id)
    ).scalar_one_or_none()
    return event_schema.dump(event)
