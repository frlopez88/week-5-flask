from flask import Flask, jsonify
from flask_cors import CORS
from database import db_init
from routes.users import users
from routes.posts import posts
from routes.likes import likes
from routes.comments import comments

db_init()

app=Flask(__name__, static_folder = "dist", static_url_path="")
CORS(app, origins="*")
app.register_blueprint(users, url_prefix = "/users")
app.register_blueprint(posts, url_prefix = "/posts")
app.register_blueprint(likes, url_prefix = "/likes")
app.register_blueprint(comments, url_prefix = "/comments")

@app.route("/")
@app.route("/<path:path>")
def serve_front_end():
    return app.send_static_file("index.html")

@app.route("/health")
def get_health():
    return jsonify({"message": "Server Online"}) , 200


if __name__ == "__main__":
    app.run(debug=True)