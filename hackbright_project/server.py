from jinja2 import StrictUndefined
from datetime import datetime
from time import strptime
from flask import Flask, render_template, redirect, request, flash, session, jsonify, json, url_for
from flask_debugtoolbar import DebugToolbarExtension
# from twilio.rest import TwilioRestClient
from model import Ticket, Agent, Customer, Company, connect_to_db, db

app = Flask(__name__)
app.secret_key = "Hello world"

app.jinja_env.undefined = StrictUndefined

def process_tickets_to_display(tickets):
    """ 
    Gets the tickets to display from the database and 
    returns them in an iterable list
    """
    ticket_list = []

    for ticket in tickets:
        ticket_num = ticket.ticket_id 
        submission_time = ticket.time_submitted
        agent_assigned_to = Agent.query.filter(Agent.id == ticket.agent_id).first()
        agent_name = agent_assigned_to.name
        agent_id = ticket.agent_id
        ticket_tuple = (ticket_num, submission_time, agent_name, agent_id)
        ticket_list.append(ticket_tuple)

    return ticket_list

def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)

@app.route('/tickets', methods=["POST", "GET"])
def index():
    """
    Renders the home screen for the customer service app 

    Contains a table showing the tickets currently in the system

    """
    tickets = Ticket.query.order_by(Ticket.ticket_id).all()
    
    ticket_list = process_tickets_to_display(tickets)

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
    
@app.route('/companies/<int:company_id>')
def show_company_detail(company_id):
    """Shows indivisual company details"""
    company = Company.query.filter(Company.id == company_id).first()
    company_name = company.name
    company_location = company.location
    company_timezone = company.time_zone
    company_industry = company.industry
    company_tier = company.support_tier
    company_pilot = company.is_pilot
    company_tickets = Company.query.filter()

    return render_template("company_detail.html", company_name=company_name, company_location=company_location, 
        company_timezone=company_timezone, company_industry=company_industry, company_tier=company_tier,
        company_pilot=company_pilot)

@app.route('/tickets/<int:ticket_id>')
def show_ticket_detail(ticket_id):
    """Shows individual ticket details"""
    ticket = Ticket.query.filter(Ticket.ticket_id == ticket_id).first()
    selected_ticket_id = ticket_id
    ticket_text = ticket.ticket_content
    ticket_time = ticket.time_submitted
    ticket_agent = agent_assigned_to = Agent.query.filter(Agent.id == ticket.agent_id).first().name
    ticket_customer = Customer.query.filter(Customer.id == ticket.customer_id).first()
    customer_email = ticket_customer.email
    customer_name = ticket_customer.name
    customer_id = ticket_customer.id
    
    return render_template("individual_ticket.html", selected_ticket_id=selected_ticket_id, 
        ticket_text=ticket_text, ticket_time=ticket_time, ticket_agent=ticket_agent, 
        customer_email=customer_email, customer_name=customer_name, customer_id=customer_id)

@app.route('/user_detail/<int:customer_id>')
def show_user_detail(customer_id):
    """Shows details about a specific customer, including the customer's name, 
       email address, company, job title, and all of the tickets associated with the customer
    """
    customer = Customer.query.filter(Customer.id == customer_id).first()
    customer_name = customer.name
    customer_email = customer.email
    customer_phone = customer.phone_number
    customer_company = Customer.query.filter(Customer.company_id == Company.id).first()
    customer_company_name= customer_company.name
    customer_company_id = customer_company.id
    customer_job_title = customer.job_title
    customer_tickets = Ticket.query.filter(customer_id == Ticket.customer_id).all()

    customer_ticket_list = process_tickets_to_display(customer_tickets)



    #ADD A JOIN TO MODEL SO CAN GET ALL THE TICKETS FOR EACH CUSTOMER 
    
    return render_template("user_detail.html", customer_name=customer_name, 
        customer_email=customer_email, customer_phone=customer_phone, 
        customer_company_name=customer_company_name, customer_company_id=customer_company_id,
         customer_job_title=customer_job_title, customer_ticket_list=customer_ticket_list)


@app.route('/dashboard_data', methods=["GET"])
def get_tickets_to_display():
    """ Gets the tickets to display in the dashboard heatmap"""
    # ticket_list =[] #A list of objects to be returned in JSON 
    ticket_dict = {}

    ticket_list = []

    date_range = request.args.get("date-range")
    
    date_range = date_range.split('-')

    
    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    type(start_date)
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")

    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.time_submitted).all()
    
    for ticket in tickets_in_range:
        ticket_hour = ticket.time_submitted.hour
        ticket_weekday = ticket.time_submitted.weekday()
        weekday_hour = (ticket_weekday, ticket_hour)

        if weekday_hour not in ticket_dict:
            ticket_dict[weekday_hour] = 1
        else:
            ticket_dict[weekday_hour] += 1 

    for key in ticket_dict:
        ticket_details = {'day': key[0], 'hour': key[1], 'value': ticket_dict[key]}
        ticket_list.append(ticket_details)
              

    # for ticket in tickets_in_range:
    #     ticket_hour = ticket.time_submitted.hour
    #     ticket_weekday = ticket.time_submitted.weekday()



    return jsonify(data=ticket_list)

@app.route('/dashboard_response_time', methods=["POST"])
def get_response_times():
    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    type(start_date)
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")

    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.time_submitted).all()

@app.route('/dashboard_tickets_by_tier', methods=["POST"])
def get_tickets_by_tier():
    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    type(start_date)
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")

    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.time_submitted).all()
    
    #get hte customer id associated with the tickets 
    #get the 

@app.route('/dashboard')
def display_dashboard():
    """ Displays the graphs showing ticket metrics"""
    return render_template("dashboard.html")

@app.route('/agent_detail/<int:agent_id>')
def show_agent_detail(agent_id):
    """Shows details about the agent clicked on in the ticket view"""
    agent = Agent.query.filter(Agent.id == agent_id).first()
    agent_name = agent.name
    agent_tier = agent.tier
    agent_email = agent.email
    agent_phone_number = agent.phone_number

    agent_tickets = Ticket.query.filter(agent_id == Ticket.agent_id).all()

    agent_ticket_list = process_tickets_to_display(agent_tickets)

    return render_template("agent_detail.html", agent_name=agent_name, agent_tier=agent_tier,
        agent_email=agent_email, agent_phone_number=agent_phone_number, agent_ticket_list=agent_ticket_list)


# @app.route('/dashboard')
# def show_dashboard():
#     """Shows the ticket analytics dashboard"""

#     return render_template("dashboard.html")


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()