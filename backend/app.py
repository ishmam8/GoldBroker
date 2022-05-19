from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)                                                  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:applytoPGADMIN@localhost/gold_tracker'
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/ 
db = SQLAlchemy(app)
CORS(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    NID = db.Column(db.String(250)) 
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event: {self.description, self.NID, self.email}"
    
    def __init__(self, description, NID, email):     
        self.description = description
        self.NID = NID
        self.email = email

def format_event(event):
    return {
        "id": event.id,
        "description": event.description,
        "NID": event.NID,
        "email": event.email,
        "created_at": event.created_at
    }


@app.route('/')
def hello():
    return "Hey"

#create an event for each users
@app.route('/event', methods = ['POST'])
def create_event():
    description = request.json['description']
    NID = request.json['NID']
    email = request.json['email']
    event = Event(description,NID,email)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

#get all the user events
@app.route('/event', methods = ['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

#get single event
@app.route('/event/<id>', methods = ['GET'])
def get_event(id):
    if request.method == 'GET':
        event = Event.query.filter_by(id=id).one()
        formatted_event = format_event(event)
        return {'event': formatted_event}

#delete an event
@app.route('/event/<id>', methods = ['DELETE'])
def delete_event(id):
    if request.method == 'DELETE':
        event = Event.query.filter_by(id=id).one()
        db.session.delete(event)
        db.session.commit()
        return f'Event{id: {id}}deleted!'

#update an event
@app.route('/event/<id>', methods = ['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    email = request.json['email']
    event.update(dict(email = email, created_at = datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}

if __name__ == '__main__':
    app.run()