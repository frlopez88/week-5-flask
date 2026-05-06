import re

from flask import Flask, jsonify, Blueprint, request
from psycopg2.extras import RealDictCursor
from database import get_connection

users = Blueprint("users", __name__)

@users.route("/<string:user_name>")
def get_users(user_name):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
                        select  user_name, 
                                first_name, 
                                last_name 
                        from social_media.users
                        where user_name = %s
                    """, (user_name, ) )
        row = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(row) , 200
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500
    
@users.route("/", methods=["POST"])
def sign_up():
    try:
        data = request.get_json()

        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
                    insert into social_media.users
                        (user_name, first_name, last_name, birt_date, password, email)
                    values 
                        (%s, %s, %s, %s, %s, %s)
                    """, (data["user_name"],
                          data["first_name"], 
                          data["last_name"], 
                          data["birt_date"], 
                          data["password"], 
                          data["email"]) )
        
        conn.commit()
        conn.close()
        cur.close()
        return jsonify({"message" : "User Created"}), 201
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500
    
@users.route("/auth", methods=["POST"])
def auth_user():
    try:
        data = request.get_json()
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
                        select  user_name, 
                                first_name, 
                                last_name 
                        from social_media.users
                        where user_name = %s
                              and password = %s 
                    """, (data["user_name"], data["password"] ) )
        row = cur.fetchall()
        cur.close()
        conn.close()

        if len(row) == 1:
            return jsonify({"message": "User Auth"}) , 200
        else:
            return jsonify({"message": "Wrong Credentials"}) , 400
    except Exception as e:
        return jsonify({"message" : f"error {e}"}), 500