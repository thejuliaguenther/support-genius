import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from model import Ticket, Agent, Customer, Company, connect_to_db, db

def get_data(tickets):
    industries = {'media':1, 'financial services':2, 'consulting':3, 'transportation':4,
    'technology':5, 'energy':6}
    
    support_tiers = {'Gold':1, 'Silver':2, 'Bronze':3}
    
    pilot = {'Yes':1, 'No':0}

    locations = {'San Diego, CA': 1, 'Boston, MA':2, 'Priceton, NJ': 3, 'New York, NY': 4,
                 'Ann Arbor, MI': 5, 'Eugene, OR': 6, 'Brooklyn, NY': 7, 'San Francisco, CA': 8,
                 'Los Angeles, CA': 9, 'Munich, Germany': 10, 'Berlin, Germany': 11, 'Detroit, MI': 12, 
                 'Redwood City, CA': 13, 'Seattle, WA': 14, 'London, UK': 15, 'Madison, WI': 16,
                 'Foster City, CA': 17, 'Chicago, IL': 18, 'Paris, France': 19, 'Syracuse, NY': 20,
                 'Fairfield, CT': 21 }

    agent_names = {'Xye Dagun': 1, 'Kayla Smith': 2, 'Stephanie Nguyen': 3, 'Christina Foran': 4,
              'Blake Gilmore': 5, 'Erica Johnson': 6, 'Brandi Day': 7, 'Julia Guenther': 8}

    feature_list = []

    for ticket in tickets:
        ticket_customer = Customer.query.filter(ticket.customer_id == Customer.id).first()
        ticket_company = Company.query.filter(Company.id == ticket_customer.company_id).first()
        ticket_agent = Agent.query.filter(ticket.agent_id == Agent.id).first()
        #Get the number corresponding to the industry that each ticket is in 
        industry = ticket_company.industry
        industry_number = industries[industry]
        
        support_tier = ticket_company.support_tier
        support_number = support_tiers[support_tier]
        
        is_pilot = ticket_company.is_pilot
        pilot_number = pilot[is_pilot]

        location = ticket_company.location
        location_number = locations[location]

        #text_score 

        ticket_agent = Agent.query.filter(Agent.id == ticket.agent_id).first()
        agent_name = ticket_agent.name
        agent_number = agent_names[agent_name] 
        print "Got to here!"
        feature_list.append([industry_number, support_number, pilot_number, location_number])
    
    feature_list_np = np.array(feature_list, float)

    bandwidth = estimate_bandwidth(feature_list_np, quantile=0.2)

    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(feature_list_np)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)


