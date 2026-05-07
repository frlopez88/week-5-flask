from flask import Flask, jsonify, Blueprint, request
from psycopg2.extras import RealDictCursor
from database import get_connection

comments = Blueprint("comments", __name__)

@comments.route("", methods=["POST"])
def add_comment():
    try:
        data = request.get_json()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(""" 
                    insert into social_media.comments
                    (user_name, post_id, description)
                    values 
                    (%s, %s, %s)
                """, (data["user_name"], data["post_id"], data["description"]))

        conn.commit()
        conn.close()
        cur.close()
        return jsonify({"message": "Object Created"}), 201
    except Exception as e:
        return jsonify({"message": f"error {e}"}), 500

@comments.route("/<int:post_id>")
def count_likes(post_id):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
                        select  * from social_media.comments
                        where post_id = %s
                    """, (post_id, ))
        row = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(row) , 200
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500