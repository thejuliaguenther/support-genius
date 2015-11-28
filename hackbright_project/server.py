from numpy import genfromtxt
import numpy as np
# import nlp
import random 
import sklearn
from nlp import process_text

# import nltk
# nltk.download()
from response_regression import get_response_regression
from agent_touches_regression import get_response_per_agent_touches
from meanshift_analysis import get_data, process_clusters, get_cluster_info

from datetime import date 
from jinja2 import StrictUndefined
import csv 
import requests
from datetime import datetime
from time import strptime
from flask import Flask, render_template, redirect, request, flash, session, jsonify, json, url_for
from flask_debugtoolbar import DebugToolbarExtension
# from twilio.rest import TwilioRestClient
from model import Ticket, Agent, Customer, Company, connect_to_db, db

#Things to import for kmeans
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
app.secret_key = "Hello world"

app.jinja_env.undefined = StrictUndefined

HOURS_PER_DAY = 24
SECONDS_PER_HOUR = 3600


def process_tickets_to_display(tickets):
    """ 
    Gets the tickets to display from the database and 
    returns them in an iterable list
    """

    #Pass in one ticket and make sure it returns the right thing
    ticket_list = []

    for ticket in tickets:
        ticket_num = ticket.ticket_id 
        submission_time = ticket.time_submitted
        agent_assigned_to = Agent.query.filter(Agent.id == ticket.agent_id).first()
        agent_name = agent_assigned_to.name
        agent_id = ticket.agent_id
        status = ticket.status
        ticket_tuple = (ticket_num, submission_time, agent_name, agent_id, status)
        ticket_list.append(ticket_tuple)

    return ticket_list

@app.route('/', methods=["POST", "GET"])
def index():
    """
    Renders the home screen for the customer service app 

    Contains a table showing the tickets currently in the system

    """
    tickets = Ticket.query.order_by(Ticket.ticket_id).all()
    
    ticket_list = process_tickets_to_display(tickets)

    return render_template("tickets.html", ticket_list=ticket_list)

@app.route('/companies/<int:company_id>')
def show_company_detail(company_id):
    """Shows indivisual company details"""
    company_tickets = []
    company = Company.query.filter(Company.id == company_id).first()
    company_name = company.name
    company_location = company.location
    company_timezone = company.time_zone
    company_industry = company.industry
    company_tier = company.support_tier
    company_pilot = company.is_pilot
    #get all customers with that company id
    company_customers = Customer.query.filter(Customer.company_id == company.id).all() 
    #lop through customers with that id, get the tickets associated with that customer
    for customer in company_customers:
        customer_tickets = Ticket.query.filter(Ticket.customer_id == customer.id).all()
        print customer_tickets
        customer_company_ticket_list = process_tickets_to_display(customer_tickets)
        print type(customer_company_ticket_list)
        # company_tickets.append(customer_company_ticket_list)
      
    # add tickets to a data structure to print out 
    # company_tickets = Ticket.query.get(Company.customer_id).all()

    return render_template("company_detail.html", company_name=company_name, company_location=company_location, 
        company_timezone=company_timezone, company_industry=company_industry, company_tier=company_tier,
        company_pilot=company_pilot, customer_company_ticket_list=customer_company_ticket_list)

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



    return jsonify(data=ticket_list)

@app.route('/dashboard_response_time.json', methods=["GET"])
def get_response_times():
    # date_range = "10/4/2015 00:00:00-10/10/2015 11:59:59"
    date_range = request.args.get("date-range")
    date_range = date_range.split('-')
    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")

    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.time_submitted).all()
    # tickets = tickets_in_range.filter( Ticket.ticket_id, Ticket.time_submitted, Ticket.time_first_responded).all()
    # ticket_responses = []

    data = get_response_regression(tickets_in_range)
    # print type(data['scatter_points'])
    # print type(data['line_points'])
    return jsonify(data=data)
    
    #return the scatterplots and line to pass to response 

@app.route('/dashboard_agent_touches.json', methods=["GET"])
def get_resolution_times():

    # date_range = "10/4/2015 00:00:00-10/10/2015 11:59:59"
    date_range = request.args.get("date-range")
    date_range = date_range.split('-')
    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")

    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.time_submitted).all()
    
    data = get_response_per_agent_touches(tickets_in_range)
    # print type(data['scatter_points'])
    # print type(data['line_points'])
    return jsonify(data=data)
    
@app.route('/nlp_route',  methods=["GET"])
def create_positive_and_negative_datasets():
    tickets = Ticket.query.all()
    data = process_text(tickets)
    
    return jsonify(data)


@app.route('/clustering.json', methods=["GET"])
def get_clusters():
    """
    This function uses meanshift to process the ticket \
    data into process_clusters
    """
    tickets = Ticket.query.all()
    data = process_clusters(tickets)
    # data = get_data(tickets)
    # data = process_clusters(ticket_clusters)
    return jsonify(data=data)

@app.route('/cluster_details.json', methods=["GET"])
def get_cluster_details():
    """
    This function takes the clusters created by the meanshift
    algorithm in get_clusters and processes the clusters
    to return details such as the average percent positive 
    of a positive ticket
    """
    tickets = Ticket.query.all()
    clusters = process_clusters(tickets)
    data = get_cluster_info(clusters);

    return jsonify(data=data)



@app.route('/customer_dashboard', methods=["GET"])
def render_clusters():
    return render_template("customer_dashboard.html")

@app.route('/tickets_by_tier.json', methods=["GET"])
def get_tickets_by_tier():
    # date_range = "10/4/2015 00:00:00-10/10/2015 11:59:59"
    date_range = request.args.get("date-range")
    date_range = date_range.split('-')

    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")
    
    customer_dict = {'Gold':0, 'Silver':0, 'Bronze':0}
    #Gets the customers who have submitted tickets in the specified date range
    customers_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.customer_id).all()
    #get the company and put company in a set 

    for ticket in customers_in_range:
        print ticket.ticket_id
        customer_id = ticket.customer_id
        customer = Customer.query.get(customer_id)
        company_id = customer.company_id
        company = Company.query.get(company_id)
        support_tier = company.support_tier
        print support_tier

        if support_tier == 'Gold':
            customer_dict['Gold'] +=1
        elif support_tier == 'Silver':
            customer_dict['Silver'] += 1
        else:
            customer_dict['Bronze'] += 1
    print customer_dict

    dict_list = []
    for key in customer_dict:
        data = {}
        data['support_tier'] = key
        data['count'] = customer_dict[key]
        dict_list.append(data)

    return jsonify({'data': dict_list})


@app.route('/tickets_by_industry.json', methods=["GET"])
def get_tickets_by_industry():
    # date_range = "10/4/2015 00:00:00-10/10/2015 11:59:59"
    date_range = request.args.get("date-range")
    date_range = date_range.split('-')

    start_date = date_range[0].encode('utf-8')
    end_date = date_range[1].encode('utf-8')
    start_date = datetime.strptime(start_date, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date, "%m/%d/%Y %H:%M:%S")
    
    industry_dict = {'Media':0, 'Financial Services':0, 'Consulting':0, 'Transportation':0, 
    'Technology':0, 'Energy':0}
    #Gets the customers who have submitted tickets in the specified date range
    tickets_in_range = Ticket.query.filter((Ticket.time_submitted > start_date) & (Ticket.time_submitted < end_date)).order_by(Ticket.customer_id).all()
    for ticket in tickets_in_range:
        customer_id = ticket.customer_id
        customer = Customer.query.get(customer_id)
        company_id = customer.company_id
        company = Company.query.get(company_id)
        industry = company.industry
        print industry

        if industry == 'media':
            industry_dict['Media'] +=1
        elif industry == 'financial services':
            industry_dict['Financial Services'] += 1
        elif industry == 'consulting':
            industry_dict['Consulting'] += 1
        elif industry == 'transportation':
            industry_dict['Transportation'] += 1
        elif industry == 'technology':
            industry_dict['Technology'] += 1
        else:
            industry_dict['Energy'] += 1

    dict_list = []
    for key in industry_dict:
        data = {}
        data['industry'] = key
        data['count'] = industry_dict[key]
        dict_list.append(data)

    print {'data': dict_list}

    return jsonify({'data': dict_list})


@app.route('/ticket_dashboard')
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


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()