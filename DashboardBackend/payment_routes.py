from flask import Blueprint, render_template
import razorpay

payment_bp = Blueprint("payment", __name__)

RAZORPAY_KEY_ID = "YOUR_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_KEY_SECRET"

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@payment_bp.route("/payment")
def payment_page():
    return render_template("payment.html")
