from flask import Blueprint, jsonify
from firebase_setup import db

Datas_bp = Blueprint("Datas", __name__)

@Datas_bp.route("/collegesData", methods=["GET"])
def get_colleges():
    ref = db.reference("colleges")
    data = ref.get()

    if not data:
        return jsonify([])

    # Convert dict -> list and return
    colleges = list(data.values())
    return jsonify(colleges)
