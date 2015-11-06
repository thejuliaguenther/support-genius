from jinja2 import StrictUndefined
from datetime import datetime
from time import strptime
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import Ticket, Agent, connect_to_db, db

app = Flask(__name__)
app.secret_key = "Hello world"

app.jinja_env.undefined = StrictUndefined

@app.route('/tickets', methods=["POST", "GET"])
def index():
    """
    Renders the home screen for the customer service app 

    Contains a table showing the tickets currently in the system

    """
    tickets = Ticket.query.order_by(Ticket.ticket_id).all()
    ticket_list = []

    for ticket in tickets:
        ticket_num = ticket.ticket_id 
        submission_time = ticket.time_submitted
        assigned_to = ticket.agent_id 
        ticket_tuple = (ticket_num, submission_time, assigned_to)
        ticket_list.append(ticket_tuple)

    return render_template("tickets.html", ticket_list=ticket_list)

@app.route('/login', methods=["GET"])
def show_login_form():
    """Shows login form."""
    
    return render_template("login.html")

@app.route('/process_login', methods=["POST"])
def process_login():
    """
    If the username or password is incorrect, flash a message informing the 
    user that the username or password is incorrect and allow them to login again
    """
    username = request.form.get("username")
    password = request.form.get("password")

    login = Agent.query.filter(Agent.email == username).first()

    if not login or login.password != password:
        flash("Username or password is incorrect")
        return redirect('/login')
    else:
        
        while username not in session.values():
            session['user_name'] = username
        return redirect('/tickets')
    

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
    # tickets = Ticket.query.order_by(Ticket.ticket_id).all()

    # tickets_by_time = {}

    # for ticket in tickets:
    #     ticket_submitted = strptime(ticket.time_submitted)
    #     ticket_day_of_week = ticket_submitted.weekday()
    #     ticket_hour_submitted = ticket_submitted.hour
        
    #     if ticket_hour_submitted not in tickets_by_time:
    #         tickets_by_time
        
    #     tickets_by_time.append({""})

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.debug = False
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()