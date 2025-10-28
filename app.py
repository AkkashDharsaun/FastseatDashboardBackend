from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "project@123"
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

# Upload config
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Blueprints
from  DashboardBackend.auth_routes import auth_bp
from DashboardBackend.college_routes import college_bp
from SeatCheckingBackend.Collegedatas import Datas_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(college_bp, url_prefix='/college')
app.register_blueprint(Datas_bp, url_prefix='/Datas')
# app.register_blueprint(departmentcls_bp, url_prefix="/department")
# app.register_blueprint(payment_bp, url_prefix="/payment")

if __name__ == "__main__":
    app.run(debug=True)

