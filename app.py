from flask import Flask, jsonify
from database import db_init
from routes.users import users

db_init()

app=Flask(__name__)
app.register_blueprint(users, url_prefix = "/users")


@app.route("/")
def get_home():
    return jsonify({"message": "Server Online"}) , 200


if __name__ == "__main__":
    app.run(debug=True)