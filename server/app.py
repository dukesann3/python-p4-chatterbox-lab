from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all()
        message_list = []
        for message in all_messages:
            message_dict = message.to_dict()
            message_list.append(message_dict)

        response = make_response(
            message_list,
            200
        )

        return response

    elif request.method == 'POST':

        req_form = request.get_json()

        new_message = Message(
           body=req_form["body"],
           username=req_form["username"],
           created_at=request.form.get('created_at'),
           updated_at=request.form.get('updated_at')
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            message_dict,
            201
        )

        return response


@app.route('/messages/<int:id>',methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        req_form = request.get_json()
        for attr in req_form:
            setattr(message, attr, req_form[attr])
        
        db.session.add(message)
        db.session.commit()

        response = make_response(
            message.to_dict(),
            200
        )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.commit()

        response = make_response(
            {'message': 'Deleted message'},
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555)
