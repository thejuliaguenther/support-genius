import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from model import Ticket, Agent, Customer, Company, connect_to_db, db


#Locations are listed with city and state or country as this is how they are listed in the database
locations = {'San Francisco, CA': 1, 'Redwood City, CA': 2, 'Foster City, CA': 3, 'Los Angeles, CA': 4,
                 'San Diego, CA': 5, 'Eugene, OR': 6, 'Seattle, WA': 7, 'Madison, WI': 8, 'Chicago, IL': 9, 
                 'Ann Arbor, MI': 10, 'Detroit, MI': 11, 'Syracuse, NY': 12, 'New York, NY': 13, 'Brooklyn, NY': 14, 
                 'Fairfield, CT': 15, 'Priceton, NJ': 16, 'Boston, MA': 17,  'London, UK': 18, 'Paris, France': 19,
                 'Munich, Germany': 20, 'Berlin, Germany': 21 }

def get_data(tickets):
    industries = {'media':1, 'financial services':2, 'consulting':3, 'transportation':4,
    'technology':5, 'energy':6}
    
    support_tiers = {'Gold':1, 'Silver':2, 'Bronze':3}
    
    pilot = {'Yes':1, 'No':0}

    agent_names = {'Xye Dagun': [0,1], 'Kayla Smith': [0,1], 'Stephanie Nguyen': [0,1], 'Christina Foran': [0,1],
              'Blake Gilmore': [0,1], 'Erica Johnson': [0,1], 'Brandi Day': [0,1], 'Julia Guenther': [0,1]}

    sentiment_numbers = {'neg': 1, 'neutral': 2, 'pos': 3}

    feature_list = []
    ticket_list = []
    sentiment_list = []
    # certainty_list = []
    positive_list = []
    negative_list = []
    pilot_list = []
    location_list = []
    industry_list = []

    for ticket in tickets:
        ticket_customer = Customer.query.filter(ticket.customer_id == Customer.id).first()
        ticket_company = Company.query.filter(Company.id == ticket_customer.company_id).first()
        ticket_agent = Agent.query.filter(ticket.agent_id == Agent.id).first()
        #Get the number corresponding to the industry that each ticket is in 
        industry = str(ticket_company.industry)
        industry_number = industries[industry]
        industry_list.append(industry_number)
        
        support_tier = str(ticket_company.support_tier)
        support_number = support_tiers[support_tier]
        
        is_pilot = str(ticket_company.is_pilot)
        pilot_number = pilot[is_pilot]
        pilot_list.append(pilot_number)

        location = str(ticket_company.location)
        location_number = locations[location]
        location_list.append(location_number)

        ticket_list.append(ticket.ticket_id)

        sentiment = str(ticket.ticket_sentiment)
        sentiment_number = sentiment_numbers[sentiment]
        sentiment_list.append(sentiment_number) 

        # percent_certainty = ticket.percent_certainty
        # certainty_list.append(percent_certainty)
        percent_positive = ticket.percent_positive
        positive_list.append(percent_positive)

        percent_negative = ticket.percent_negative
        negative_list.append(percent_negative)


        ticket_agent = Agent.query.filter(Agent.id == ticket.agent_id).first()
        agent_name = ticket_agent.name
        agents_on_ticket = []
        for x in agent_names:
            if x == agent_name:
                agents_on_ticket.append(1)
            else:
                agents_on_ticket.append(0)
        features_per_ticket = []
        features_per_ticket.extend([industry_number, support_number, pilot_number, location_number])
        features_per_ticket.extend(agents_on_ticket)
        features_per_ticket.append(sentiment_number)

        feature_list.append(features_per_ticket)
    
    feature_list_np = np.array(feature_list, float)

    bandwidth = estimate_bandwidth(feature_list_np, quantile=0.2)

    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(feature_list_np)
    labels = ms.labels_


    # make a label_count_dict, to osee distribution
    label_count_dict = {}
    for lab in list(labels):
        label_count_dict[lab] = label_count_dict.get(lab, 0) + 1


    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)


    processed_clusters = zip(labels, ticket_list, sentiment_list, positive_list, negative_list, pilot_list, location_list, industry_list)
  
    return processed_clusters

def get_cluster_info(cluster_tickets):
        """
        This function computes valuable statistics about each cluster, such as the 
        average positive rating, the average negative rating, the most common location
        from which a ticket has been sent, and the total percentage of tickets that were 
        pilots
        """

        cluster_info = {}
        cluster_names = cluster_tickets.keys()
        positive_list = []
        negative_list = []

        for key in cluster_names:
           
            pos_pilot_count = 0
            neg_pilot_count = 0
            pos_location_counts = { '1': 0, '2': 0, '3': 0, '3': 0, '4': 0, '5': 0, 
                               '6': 0, '7': 0, '8': 0, '7': 0, '8': 0, '9': 0, '10': 0, 
                               '11': 0, '12': 0, '13': 0, '14': 0,  '15': 0, '16': 0,'17': 0, 
                               '18': 0, '19': 0, '20': 0, '21': 0 }
            
            neg_location_counts = { '1': 0, '2': 0, '3': 0, '3': 0, '4': 0, '5': 0, 
                               '6': 0, '7': 0, '8': 0, '7': 0, '8': 0, '9': 0, '10': 0, 
                               '11': 0, '12': 0, '13': 0, '14': 0,  '15': 0, '16': 0,'17': 0, 
                               '18': 0, '19': 0, '20': 0, '21': 0 }

            pos_industry_counts = { '1': 0, '2': 0, '3': 0, '3': 0, '4': 0, '5': 0, 
                               '6': 0}

            neg_industry_counts = { '1': 0, '2': 0, '3': 0, '3': 0, '4': 0, '5': 0, 
                               '6': 0}
            # industry_counts = { '1': 0, '2': 0, '3': 0, '3': 0, '4': 0, '5': 0, 
            #                    '6': 0}

            curr_cluster = cluster_tickets[key] #gets the cluster 
            for i in range(len(curr_cluster['pos'])):
                print curr_cluster['pos'][i][1]
                positive_list.append(curr_cluster['pos'][i][1])
                if curr_cluster['pos'][i][3] == 1:
                    pos_pilot_count += 1
                pos_ticket_location = curr_cluster['pos'][i][5]
                pos_location_counts[str(pos_ticket_location)] += 1
                
                pos_ticket_industry = curr_cluster['pos'][i][6]
                pos_industry_counts[str(pos_ticket_industry)] += 1
            for j in range(len(curr_cluster['neg'])):
                negative_list.append(curr_cluster['neg'][j][2])
                if curr_cluster['neg'][i][3] == 1:
                    neg_pilot_count += 1
                neg_ticket_location = curr_cluster['neg'][i][5]
                neg_location_counts[str(neg_ticket_location)] += 1

                neg_ticket_industry = curr_cluster['neg'][i][6]
                neg_industry_counts[str(neg_ticket_industry)] += 1
            
            cluster_average_positive = (reduce(lambda x,y: x+y, positive_list))/ len(positive_list)
            cluster_average_negative = (reduce(lambda x,y: x+y, negative_list))/ len(negative_list)
            
            percent_positive_pilots = pos_pilot_count/float(len(positive_list))
            percent_negative_pilots = neg_pilot_count/float(len(negative_list))



            print key 
            print "Pos locations"
            print pos_location_counts
            top_pos_location = get_top_location(pos_location_counts)
            print " "
            print key
            print "Neg locations"
            print neg_location_counts
            top_neg_location = get_top_location(neg_location_counts)

            top_pos_industry = get_top_industry(pos_industry_counts)
            top_neg_industry = get_top_industry(neg_industry_counts)


            cluster_info[key] = {'percent_positive': round((cluster_average_positive * 100), 1),'percent_negative': round((cluster_average_negative * 100), 1), 
            # 'pos_pilot_count': pos_pilot_count, 'neg_pilot_count': neg_pilot_count, 'percent_positive_pilots': percent_positive_pilots, 
            'percent_negative_pilots': round((percent_negative_pilots *100), 1), 'top_pos_location': top_pos_location[1],'top_neg_location': top_neg_location[1], 
            'max_pos_location_count': top_pos_location[0], 'max_neg_location_count': top_neg_location[0], 'top_pos_industry_count': top_pos_industry[0],
            'top_neg_industry_count':top_neg_industry[0], 'top_neg_industry': top_neg_industry[1], 'top_pos_industry': top_pos_industry[1]}

        return cluster_info



def get_top_location(location_list):
    location_names = {'1': 'San Francisco, CA', '2': 'Redwood City, CA', '3': 'Foster City, CA', '4':'Los Angeles, CA',
                 '5':'San Diego, CA', '6':'Eugene, OR', '7':'Seattle, WA','8':'Madison, WI', '9':'Chicago, IL', 
                 '10': 'Ann Arbor, MI', '11':'Detroit, MI', '12':'Syracuse, NY', '13':'New York, NY', '14':'Brooklyn, NY', 
                 '15':'Fairfield, CT', '16':'Priceton, NJ', '17': 'Boston, MA', '18': 'London, UK', '19': 'Paris, France',
                 '20':'Munich, Germany', '21':'Berlin, Germany' }
    print "Location list"
    print location_list
    max_count = 0
    max_location = ""
    for location in location_list:
        if location_list[location] > max_count:
            max_count = location_list[location]
            print "MAX COUNT"
            print max_count
            max_location = location
    print "MAX"
    print max_location
    max_location_name = location_names[str(max_location)]
    return (max_count, max_location_name)

def get_top_industry(industry_list):
    industry_names = {'1': 'media', '2': 'financial services', '3': 'consulting', '4': 'transportation',
             '5': 'technology', '6': 'energy'}
    max_count = 0
    max_industry = ""
    for industry in industry_list:
        if industry_list[industry] > max_count:
            max_count = industry_list[industry]
            print max_count
            max_industry = industry
    max_industry_name = industry_names[str(max_industry)]
    return (max_count, max_industry_name)


def process_clusters(tickets):
    """
    This function gets the number of positive, negative, and neutral tickets 
    in each cluster and returns a dictionary containing the number of positive, 
    negative, and neutral tickets in each cluster
    """
    ticket_details = get_data(tickets)

    cluster_1 = {'neg':[], 'neutral':[], 'pos':[]}
    cluster_2 = {'neg':[], 'neutral':[], 'pos':[]}
    cluster_3 = {'neg':[], 'neutral':[], 'pos':[]}
 
    cluster_list = []

    cluster_data = {}
    cluster_labels = {}

    cluster_stuff = []

    for ticket in ticket_details:
        cluster_label = ticket[0]
        ticket_id = ticket[1]
        sentiment = ticket[2]
        percent_positive = ticket[3]
        percent_negative = ticket[4]
        is_pilot = ticket[5]
        ticket_location = ticket[6]
        ticket_industry = ticket[7]
 
        ticket_values = []

        
        cluster_stuff.append(cluster_label)

        if cluster_label == 0:
            if sentiment == 1:
                cluster_1['neg'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            elif sentiment == 2:
                cluster_1['neutral'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            else:
                cluster_1['pos'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location,ticket_industry])
        elif cluster_label == 1:
            if sentiment == 1:
                cluster_2['neg'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            elif sentiment == 2:
                cluster_2['neutral'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            else:
                cluster_2['pos'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
        elif cluster_label == 2:
            if sentiment == 1:
                cluster_3['neg'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            elif sentiment == 2:
                cluster_3['neutral'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
            else:
                cluster_3['pos'].append([ticket_id, percent_positive, percent_negative, is_pilot, sentiment, ticket_location, ticket_industry])
       
    
    
    cluster_labels = {'cluster1':cluster_1,'cluster2':cluster_2, 'cluster3':cluster_3}
    
    return cluster_labels
    
    

    





