""" 
This file seeds the database containing 4 tables: 
    -A table containing all of the tickets logged by customers
    -A table containing all of the customers who have logged tickets 
    -A table containing all of the companies who are customers
    -A table containing all of the agents responding to tickets 

"""
from model import Company
from model import Customer
from model import Agent 
from model import Ticket 

from model import connect_to_db, db
from server import app
from datetime import datetime

def load_companies():
    """ Load companies from companies.txt to database"""
    for row in open("companies.txt"):
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

        db.session.add(company)
    print "Got to here"
    db.session.commit()

def load_customers():
    """ Load customers from customers.txt to database"""
    for row in open("customers.txt"):
        row = row.strip()
        id, name, email, company_id, phone_number, job_title = row.split("|")

        customer = Customer(id=id.strip(), 
                            name=name.strip(),
                            email=email.strip(),
                            company_id=company_id.strip(),
                            phone_number=phone_number.strip(),
                            job_title=job_title.strip())
        db.session.add(customer)

    db.session.commit()


def load_agents():
    """ Load agents from agents.txt to database"""
    for row in open("agents.txt"):
        row = row.strip()
        id, name, password, email, tier= row.split("|")

        agent = Agent(id=id.strip(),
                      name=name.strip(),
                      password=password.strip(),
                      phone_number=phone_number.strip(),
                      email=email.strip(),
                      tier=int(tier.strip()))

        db.session.add(agent)

    db.session.commit()


def load_tickets():
    """ Load tickets from tickets.txt to database"""
    for row in open("tickets.txt"):
        id, customer_id, agent_id, time_submitted, channel_submitted, ticket_content, time_resolved, num_agent_touches, time_first_responded= row.split("|")

        ticket = Ticket(ticket_id=ticket_id.strip(),
                        customer_id=customer_id.strip(),
                        agent_id=agent_id.strip(),
                        time_submitted=datetime.strptime(time_submitted.strip(), '%m/%d/%y %H:%M'),
                        channel_submitted=channel_submitted.strip(),
                        ticket_content=ticket_content.strip(),
                        time_resolved=datetime.strptime(time_resolved.strip(), '%m/%d/%y %H:%M'),
                        num_agent_touches=num_agent_touches.strip(),
                        time_first_responded=datetime.strptime(time_first_responded.strip(), '%m/%d/%y %H:%M'))
                        
        db.session.add(ticket)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_customers()
    load_companies()
    load_agents()
    load_tickets()
