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
        id, name, email, company_id, phone_number, job_title = row.split("|")

        customer = Customer(id=id.strip(), 
                            name=name.strip(),
                            email=email.strip(),
                            company_id=company_id.strip(),
                            phone_number=phone_number.strip(),
                            job_title=job_title.strip())
        customer.save()


def load_companies():
    """ Load companies from companies.txt to database"""
    for row in open("seed_data/companies.txt"):
        row = row.strip()
        id, name, domain, location, time_zone, industry, support_tier, is_pilot = row.split("|")

        company = Company(id=id.strip(),
                          name=name.strip(), 
                          domain=domain.strip(),
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
        id, name, password, email, tier= row.split("|")

        agent = Agent(name=name.strip(),
                      password=password.strip(),
                      email=email.strip(),
                      tier=int(tier.strip()))

        agent.save()


def load_tickets():
    """ Load tickets from tickets.txt to database"""
    for row in open("seed_data/tickets.txt"):
        
        ticket_id, customer_id, agent_id, time_submitted, channel_submitted, ticket_content, time_resolved, num_agent_touches, time_first_responded = row.split("|")


        ticket = Ticket(ticket_id=ticket_id.strip(),
                        customer_id=customer_id.strip(),
                        agent_id=agent_id.strip(),
                        time_submitted=datetime.strptime(time_submitted.strip(), '%m/%d/%y %H:%M'),
                        channel_submitted=channel_submitted.strip(),
                        ticket_content=ticket_content.strip(),
                        time_resolved=datetime.strptime(time_resolved.strip(), '%m/%d/%y %H:%M'),
                        num_agent_touches=num_agent_touches.strip(),
                        time_first_responded=datetime.strptime(time_first_responded.strip(), '%m/%d/%y %H:%M'),
                        
        ticket.save()
