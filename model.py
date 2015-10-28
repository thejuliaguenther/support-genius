#This file creates the model for the databases used in this project


db = SQLAlchemy()

class Customers (Model.db):
    
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(50), nullable=True)
    customer_email_domain = db.Column(db.String(50), nullable=True)
    customer_phone_number = db.Column(db.String(50), nullable=True)
    customer_job_title = db.Column(db.String(50), nullable=True)


class Tickets (Model.db):
    
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Companies (Model.db):
    
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Agents (Model.db):
    
    __tablename__ = "agents"

    agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)