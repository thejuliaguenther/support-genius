from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "Hello world"

app.jinja_env.undefined = StrictUndefined

@app.route('/tickets', methods=["POST", "GET"])
def index():
    """
    Renders the home screen for the customer service app 

    Contains a table showing the tickets currently in the system

    """

    return render_template("tickets.html")

@app.route('/login')
def show_login_form():
    """Shows login form."""
    return render_template("login.html")

@app.route('/tickets/<int:ticket_id>')
def show_ticket_detail():
    """Shows individual ticket details"""

    return render_template("individual_ticket.html")

@app.route('/user_detail/<int:user_id>')
def show_user_detail():
    """Shows details about a specific customer"""

    return render_template("user_detail.html")

@app.route('/dashboard')
def show_dashboard():
    """Shows the ticket analytics dashboard"""

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()