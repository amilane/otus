import os
import json

from flask import Flask, request
from sqlalchemy import  create_engine

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}
engine = create_engine(config['DATABASE_URI'], echo=True)

@app.route("/health")
def health():
    return '{"status": "ok"}'

@app.route("/version")
def version():
    return '{"version": "0.11"}'

@app.route("/")
def hello():
    return 'Hello world from ' + os.environ['HOSTNAME'] + '!'

@app.route("/config")
def configuration():
    return json.dumps(config)

@app.route('/db')
def db():
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select id, username from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# Add new user
@app.route('/user', methods=['POST'])
def add_user():
    id = request.json['id']
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']

    with engine.connect() as connection:
        connection.execute(f"insert into client(id, username, firstname, lastname, email, phone) values ({id}, '{username}', '{firstname}', '{lastname}', '{email}', '{phone}');")

    return f"new user {username} added"

# Get user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    rows = []
    with engine.connect() as connection:
        result = connection.execute(f"select * from client where id = {id};")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# Update user
@app.route('/user', methods=['PUT'])
def update_user():
    id = request.json['id']
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']

    with engine.connect() as connection:
        connection.execute(f"update client set username = '{username}', firstname = '{firstname}', lastname = '{lastname}', email = '{email}', phone = '{phone}' where id = {id};")
    return f"user {username} updated"

# Delete user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    with engine.connect() as connection:
        connection.execute(f"delete from client where id = {id};")

    return f"user {id} deleted"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
