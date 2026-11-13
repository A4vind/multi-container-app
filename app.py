from flask import Flask
import mysql.connector, os

app = Flask(__name__)

@app.route("/")
def home():
    try:
        db = mysql.connector.connect(host="db", user="appuser",
             password=os.environ["DB_PASSWORD"], database="mydatabase")
        db.close()
        return "<h1>Docker Multi-Container App</h1><h2>Flask Running</h2><p style='color:green'>Connected to MySQL successfully!</p>"
    except Exception as e:
        return f"Database connection failed: {e}", 503

app.run(host="0.0.0.0", port=5000)
