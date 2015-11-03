""" 
This file seeds the database containing 4 tables: 
    -A table containing all of the tickets logged by customers
    -A table containing all of the customers who have logged tickets 
    -A table containing all of the companies who are customers
    -A table containing all of the agents responding to tickets 

"""
from ticket_systems.models import Customer
from ticket_systems.models import Company
from ticket_systems.models import Agent 
from ticket_systems.models import Ticket 

from datetime import datetime


def load_customers():
    """ Load customers from customers.txt to database"""
    for row in open("seed_data/customers.txt"):
        row = row.strip()
        customer_id, customer_name, customer_email, company_id, customer_phone_number, customer_job_title = row.split("|")

        customer = Customer(customer_id=customer_id.strip(), 
                            customer_name=customer_name.strip(),
                            customer_email=customer_email.strip(),
                            company_id=company_id.strip(),
                            customer_phone_number=customer_phone_number.strip(),
                            customer_job_title=customer_job_title.strip())
        customer.save()


def load_companies():
    """ Load companies from companies.txt to database"""
    for row in open("seed_data/companies.txt"):
        row = row.strip()
        company_id, company_name, email_domain, location, time_zone, industry, support_tier, is_pilot = row.split("|")

        company = Company(company_id=company_id.strip(),
                          company_name=company_name.strip(), 
                          email_domain=email_domain.strip(),
                          location=location.strip(),
                          time_zone=time_zone.strip(),
                          industry=industry.strip(),
                          support_tier=support_tier.strip(),
                          is_pilot=is_pilot.strip())
        company.save()


def load_agents():
    """ Load agents from agents.txt to database"""
    for row in open("seed_data/agents.txt"):
        row = row.strip()
        agent_name, agent_password, agent_email, agent_tier= row.split("|")

        agent = Agent(agent_name=agent_name.strip(),
                      agent_password=agent_password.strip(),
                      agent_email=agent_email.strip(),
                      agent_tier=int(agent_tier.strip()))

        agent.save()


def load_tickets():
    """ Load tickets from tickets.txt to database"""
    for row in open("seed_data/tickets.txt"):
        
        ticket_id, customer_id, time_submitted, agent_id, num_agent_touches, resolution_time, first_response_time, channel_submitted, ticket_content= row.split("|")


        ticket = Ticket(ticket_id=ticket_id.strip(),
                        customer_id=customer_id.strip(),
                        time_submitted=datetime.strptime(time_submitted.strip(), '%m/%d/%y %H:%M'),
                        agent_id=agent_id.strip(),
                        num_agent_touches=num_agent_touches.strip(),
                        resolution_time=datetime.strptime(resolution_time.strip(), '%m/%d/%y %H:%M'),
                        first_response_time=datetime.strptime(first_response_time.strip(), '%m/%d/%y %H:%M'),
                        channel_submitted=channel_submitted.strip(),
                        ticket_content=ticket_content.strip())
        
        ticket.save()
