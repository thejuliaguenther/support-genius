from django.db import models

# Create your models here.
class Customer(models.Model):

    #customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = models.CharField(max_length=)
    #customer_name = db.Column(db.String(50), nullable=False)
    customer_name = models.CharField(max_length=50)
    #customer_email = db.Column(db.String(50), nullable=True)
    customer_email = models.CharField(max_length=50)
    #company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    company_id = models.ForeignKey(Company)
    #customer_phone_number = db.Column(db.String(50), nullable=True)
    customer_phone_number = models.CharField(max_length=50)
    #customer_job_title = db.Column(db.String(50), nullable=True)
    customer_job_title = models.CharField(max_length=50)

    # #define relationship to company
    # company = db.relationship("Company",
    #                           backref=db.backref("customers", order_by=customer_id))

class Company(models.Model):
    
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50), unique=True, nullable=True)
    email_domain = db.Column(db.String(50), unique=True, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    time_zone = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(50), nullable=True)
    support_tier = db.Column(db.String(10), nullable=True)
    is_pilot = db.Column(db.String(10), nullable=True)


class Agent(models.Model):
    
    __tablename__ = "agents"

    agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_name = db.Column(db.String(50), nullable=True)
    agent_password = db.Column(db.String(50), nullable=True)
    agent_email = db.Column(db.String(50), nullable=True)
    agent_tier = db.Column(db.Integer, nullable=True)


class Ticket(models.Model):
    
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
