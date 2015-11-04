# from django.utils.six import python_2_unicode_compatible
from django.db import models
from time import strptime

# Create your models here.

# @python_2_unicode_compatible
class Company(models.Model):
    
    # __tablename__ = "companies"

    # company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = models.AutoField(primary_key=True,)
    # company_name = db.Column(db.String(50), unique=True, nullable=True)
    name = models.CharField(max_length=50, blank=True,)
    # email_domain = db.Column(db.String(50), unique=True, nullable=True)
    domain = models.CharField(max_length=50, blank=True,)
    # location = db.Column(db.String(100), nullable=True)
    location = models.CharField(max_length=50, blank=True,)
    # time_zone = db.Column(db.String(100), nullable=True)
    time_zone = models.CharField(max_length=100, blank=True,)
    # industry = db.Column(db.String(50), nullable=True)
    industry = models.CharField(max_length=50, blank=True,)
    # support_tier = db.Column(db.String(10), nullable=True)
    support_tier = models.CharField(max_length=50, blank=True,)
    # is_pilot = db.Column(db.String(10), nullable=True)
    is_pilot = models.CharField(max_length=50, blank=True,)

    def __unicode__(self):
        return self.name, self.domain, self.location, self.time_zone, self.industry, self.support_tier, self.is_pilot

# @python_2_unicode_compatible
class Customer(models.Model):

    #customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = models.AutoField(primary_key=True,)
    #customer_name = db.Column(db.String(50), nullable=False)
    name = models.CharField(max_length=50,)
    #customer_email = db.Column(db.String(50), nullable=True)
    email = models.EmailField(max_length=50, blank=True,)
    #company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    company_id = models.ForeignKey(Company,)
    #customer_phone_number = db.Column(db.String(50), nullable=True)
    phone_number = models.CharField(max_length=50, blank=True,)
    #customer_job_title = db.Column(db.String(50), nullable=True)
    job_title = models.CharField(max_length=50, blank=True,)

    # #define relationship to company
    # company = db.relationship("Company",
    #                           backref=db.backref("customers", order_by=customer_id))

# @python_2_unicode_compatible
class Agent(models.Model):
    
    # __tablename__ = "agents"

    # agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = models.AutoField(primary_key=True,)
    # agent_name = db.Column(db.String(50), nullable=True)
    name = models.CharField(max_length=50, blank=True,)
    # agent_password = db.Column(db.String(50), nullable=True)
    password = models.CharField(max_length=50, blank=True,)
    # agent_email = db.Column(db.String(50), nullable=True)
    email = models.EmailField(max_length=50, blank=True,)
    # agent_tier = db.Column(db.Integer, nullable=True)
    tier = models.IntegerField(blank=True,)

    def __unicode__(self):
        return self.name, self.password


# @python_2_unicode_compatible
class Ticket(models.Model):
    
    # __tablename__ = "tickets"

    # ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = models.AutoField(primary_key=True,)
    # customer_id = db.Column(db.Integer(), db.ForeignKey('customers.customer_id'), nullable=False)
    customer_id = models.ForeignKey(Customer,)
    # agent_id = db.Column(db.Integer(), db.ForeignKey('agents.agent_id'), nullable=False)
    agent_id = models.ForeignKey(Agent,)
    # time_submitted = db.Column(db.DateTime())
    time_submitted = models.DateTimeField(default=strptime('01/01/15 12:00','%m/%d/%y %H:%M'),)
    # channel_submitted = db.Column(db.String(50), nullable=True)
    channel_submitted = models.CharField(max_length=50, blank=True,)
    # ticket_content = db.Column(db.String(), nullable=False)
    ticket_content = models.CharField(max_length=500,)
    # resolution_time = db.Column(db.DateTime())
    time_resolved = models.DateTimeField(default=strptime('01/01/15 12:00','%m/%d/%y %H:%M'),)
    # num_agent_touches = db.Column(db.Integer())
    num_agent_touches = models.IntegerField()
    # first_response_time = db.Column(db.DateTime())
    time_first_responded = models.DateTimeField(default=strptime('01/01/15 12:00','%m/%d/%y %H:%M'),)
 
    # #define relationship to customer
    # customer = db.relationship("Customer", 
    #                            backref=db.backref("tickets", order_by=ticket_id))
    # #define relationship to agent 
    # agent = db.relationship("Agent", 
