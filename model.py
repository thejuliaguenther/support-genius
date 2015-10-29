#This file creates the model for the databases used in this project


db = SQLAlchemy()

class Customer (Model.db):
    
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(50), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    customer_phone_number = db.Column(db.String(50), nullable=True)
    customer_job_title = db.Column(db.String(50), nullable=True)

class Company (Model.db):
    
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_domain = db.Column(db.String(50), unique=True, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    time_zone = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(50), nullable=True)
    support_tier = db.Column(db.String(10), nullable=True)
    is_pilot = db.Column(db.String(10), nullable=True)

class Agent (Model.db):
    
    __tablename__ = "agents"

    agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_password = db.Column(db.String(50), nullable=True)
    agent_email = db.Column(db.String(50), nullable=True)
    agent_tier = db.Column(db.String(10), nullable=True)

class Ticket (Model.db):
    
    __tablename__ = "tickets"

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.customer_id'), nullable=False)
    #company_id = db.Column(db.Integer(), db.ForeignKey('companies.commpany_id'), nullable=False)
    agent_id = db.Column(db.Integer(), db.ForeignKey('agents.agent_id'), nullable=False)
    time_submitted = db.Column(db.DateTime())
    channel_submitted = db.Column(db.String(50), nullable=True)
    ticket_content = db.Column(db.String(), nullable=False)
    resolution_minutes = db.Column(db.Integer())
    num_agent_touches = db.Column(db.Integer())
    first_response_time_minutes = db.Column(db.Integer())


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hbproject'
    db.app = app
    db.init_app(app)

    if __name__ == "__main__":
        # As a convenience, if we run this module interactively, it will leave
        # you in a state of being able to work with the database directly.

        from server import app
        connect_to_db(app)
        print "Connected to DB."
