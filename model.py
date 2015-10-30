#This file creates the model for the databases used in this project
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_URI = "sqlite:///tickets.db"

db = SQLAlchemy()

class Customer(db.Model):
    
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(50), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    customer_phone_number = db.Column(db.String(50), nullable=True)
    customer_job_title = db.Column(db.String(50), nullable=True)

    #define relationship to company
    company = db.relationship("Company",
                              backref=db.backref("customers", order_by=customer_id))

class Company(db.Model):
    
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50), unique=True, nullable=True)
    email_domain = db.Column(db.String(50), unique=True, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    time_zone = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(50), nullable=True)
    support_tier = db.Column(db.String(10), nullable=True)
    is_pilot = db.Column(db.String(10), nullable=True)


class Agent(db.Model):
    
    __tablename__ = "agents"

    agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_name = db.Column(db.String(50), nullable=True)
    agent_password = db.Column(db.String(50), nullable=True)
    agent_email = db.Column(db.String(50), nullable=True)
    agent_tier = db.Column(db.Integer, nullable=True)


class Ticket(db.Model):
    
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.customer_id'), nullable=False)
    agent_id = db.Column(db.Integer(), db.ForeignKey('agents.agent_id'), nullable=False)
    time_submitted = db.Column(db.DateTime())
    channel_submitted = db.Column(db.String(50), nullable=True)
    ticket_content = db.Column(db.String(), nullable=False)
    resolution_time = db.Column(db.DateTime())
    num_agent_touches = db.Column(db.Integer())
    first_response_time = db.Column(db.DateTime())
 
    #define relationship to customer
    customer = db.relationship("Customer", 
                               backref=db.backref("tickets", order_by=ticket_id))
    #define relationship to agent 
    agent = db.relationship("Agent", 
                               backref=db.backref("tickets", order_by=ticket_id))
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hbproject'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

    if __name__ == "__main__":
        # As a convenience, if we run this module interactively, it will leave
        # you in a state of being able to work with the database directly.

        from server import app
        connect_to_db(app)
        print "Connected to DB."
