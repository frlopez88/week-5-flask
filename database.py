import psycopg2 , os 
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port =os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        sslmode = os.getenv("DB_SSLMODE")
    )

    return conn

def db_init():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""

create schema if not exists social_media;

create table if not exists social_media.users (
    user_name varchar(50) primary key,
    first_name varchar(100),
    last_name varchar(100),
    birt_date date,
    password varchar(20),
    email varchar(50) unique
);

create table if not exists social_media.posts(
    post_id serial primary key,
    description varchar(150),
    user_name varchar(50) references social_media.users(user_name),
    creation_date timestamp default current_timestamp
);

create table if not exists social_media.comments (
    comment_id serial primary key,
    user_name varchar(50) references social_media.users(user_name),
    post_id int references social_media.posts(post_id),
    description varchar(100)
);

create table if not exists social_media.likes (
    like_id serial primary key,
    user_name varchar(50) references social_media.users(user_name),
    post_id int references social_media.posts(post_id)
);

    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database Ready! ✅")