from flask import Flask, jsonify, Blueprint, request
from psycopg2.extras import RealDictCursor
from database import get_connection

posts = Blueprint("posts", __name__)

@posts.route("/", methods=["POST"])
def create_post():
    try:
        conn = get_connection()
        cur = conn.cursor()
        data = request.get_json()
        cur.execute("""
                        insert into social_media.posts
                        (description, user_name)
                        values
                        (%s, %s)

                    """, (data["description"], data["user_name"]) )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify ({"message": "Object Created"}), 201

    except Exception as e:
        return jsonify({"message":f" error: {e}"}), 500
    
@posts.route("/")
def get_posts():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
                        select  *
                        from social_media.posts
                    """)
        row = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(row) , 200
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500