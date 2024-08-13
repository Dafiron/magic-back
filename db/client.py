from pymongo import MongoClient
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

sql_pass = os.getenv("db_sql_password")
sql_user = os.getenv("db_sql_user")
sql_host = os.getenv("db_sql_host")
sql_port = os.getenv("db_sql_port")
sql_database =os.getenv("db_sql_database")
mongodb_user = os.getenv("db_mongo_user")
mongodb_pass = os.getenv("db_mongo_password")


# conexion en local Mongodb
#db_client = MongoClient().local

# conexion en remota Mongodb
db_client = MongoClient(
    f"mongodb+srv://{mongodb_user}:{mongodb_pass}@cluster0.miq7mbw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    ).user_db.oath

def get_sql_connection():
    config = {
    "host": sql_host,
    "port": int(sql_port),
    "database": sql_database,
    "user":sql_user,
    "password":sql_pass
    }
    connection = mysql.connector.connect(**config)
    return connection

