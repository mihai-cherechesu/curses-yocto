from flask import Flask, request, Response, json
from werkzeug.exceptions import BadRequest, NotFound

from db import Database

app = Flask(__name__)
db = Database()

@app.route("/api/submarine", methods=["GET"])
def get_submarine():
    global db
    return Response(json.dumps(db.get_submarine()), status=200, mimetype='application/json')

@app.route("/api/submarine/move", methods=["POST"])
def move_submarine():
    global db
    try:
        db.move_submarine(request.get_json())
        db.flush_state()
    except BadRequest:
        return Response(status=400)

    return Response(status=201)

@app.route("/api/fish", methods=["GET"])
def get_fishes():
    global db
    return Response(json.dumps(db.get_fishes()), status=200, mimetype='application/json')

@app.route("/api/fish/add", methods=["POST"])
def add_fish():
    global db
    try:
        db.add_fish(request.get_json())
        db.flush_state()
    except BadRequest:
        return Response(status=400)

    return Response(status=201)

@app.route("/api/artifact", methods=["GET"])
def get_artifact():
    global db
    return Response(json.dumps(db.get_artifact()), status=200, mimetype='application/json')

@app.route("/api/artifact/update", methods=["POST"])
def update_artifact():
    global db
    try:
        db.update_artifact(request.get_json())
        db.flush_state()
    except BadRequest:
        return Response(status=400)

    return Response(status=201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)