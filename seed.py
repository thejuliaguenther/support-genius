""" 
This file seeds the database containing 4 tables: 
    -A table containing all of the tickets logged by customers
    -A table containing all of the customers who have logged tickets 
    -A table containing all of the companies who are customers
    -A table containing all of the agents responding to tickets 

"""
from model import Customer
from model import Company
from model import Agent 
from model import Ticket 

from model import connect_to_db, connect_to_db
from server import app
import datetime

def load_customers():
    """ Load customers from customers.txt to database"""
    for row in open("seed_data/customers.txt"):
        row = row.strip()
        customer_id, customer_name, customer_email, company_id, customer_phone_number, customer_job_title = ro

def load_companies():
    """ Load companies from companies.txt to database"""

def load_agents():
    """ Load agents from agents.txt to database"""

def load_tickets():
    """ Load tickets from tickets.txt to database"""