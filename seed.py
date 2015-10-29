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
        customer_id, customer_name, customer_email, company_id, customer_phone_number, customer_job_title = row.split("|")

        customer = Customer(customer_id=customer_id, 
                            customer_name=customer_name,
                            customer_email=customer_email,
                            company_id=company_id,
                            customer_phone_number=customer_phone_number,
                            customer_job_title=customer_job_title)
        db.session.add(customer)

    db.commit()

def load_companies():
    """ Load companies from companies.txt to database"""
    for row in open("seed_data/companies.txt"):
        row = row.strip()
        company_id, email_domain, location, time_zone, industry, support_tier, is_pilot = row.split("|")

        company = Company(company_id=company_id, 
                          email_domain=email_domain,
                          location=location;
                          time_zone=time_zone,
                          industry=industry,
                          support_tier=support_tier,
                          is_pilot=is_pilot)

        db.session.add(company)

    db.session.commit()

def load_agents():
    """ Load agents from agents.txt to database"""
    for row in open("seed_data/agents.txt"):
        row = row.strip()
        agent_id, agent_password, agent_email, agent_tier= row.split("|")

        agent = Agent(agent_id=agent_id,
                      agent_password=agent_password,
                      agent_email=agent_email;
                      agent_tier=agent_tier)

        db.session.add(agent)

    db.session.commit()

def load_tickets():
    """ Load tickets from tickets.txt to database"""
    for row in open("seed_data/tickets.txt"):
        row = row.strip()
        ticket_id, customer_id, time_submitted, agent_id, num_agent_touches, resolution_time, first_response_time, channel_submitted, ticket_content= row.split("|")
        
        ticket = Ticket(ticket_id=ticket_id,
                        customer_id=customer_id,
                        agent_id=agent_id,
                        time_submitted=time_submitted,
                        agent_id=agent_id,
                        num_agent_touches=num_agent_touches,
                        resolution_time=resolution_time,
                        first_response_time=first_response_time,
                        channel_submitted=channel_submitted;
                        ticket_content=ticket_content)


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_customers()
    load_companies()
    load_agents()
    load_tickets()
