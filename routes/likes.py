import json

from flask import Flask, jsonify, Blueprint, request
from psycopg2.extras import RealDictCursor
from database import get_connection

likes = Blueprint("likes", __name__)

@likes.route("/", methods=["POST"])
def like_post():
    try:
        data = request.get_json()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(""" 
                    insert into social_media.likes
                    (user_name, post_id)
                    values 
                    (%s, %s)
                """, (data["user_name"], data["post_id"]))

        conn.commit()
        conn.close()
        cur.close()
        return jsonify({"message": "Object Created"}), 201
    except Exception as e:
        return jsonify({"message": f"error {e}"}), 500

@likes.route("/<int:post_id>/countlikes")
def count_likes(post_id):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
                        select  count(*) likes
                        from social_media.likes
                        where post_id = %s
                    """, (post_id, ))
        row = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(row) , 200
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500