from sklearn import datasets, linear_model
from datetime import datetime
import numpy as np

SECONDS_PER_HOUR = 3600

def get_response_per_agent_touches(tickets_in_range):

    ticket_resolution_list = []
    ticket_touches_list = []

    for ticket in tickets_in_range:
        ticket_id = ticket.ticket_id
        time_to_resolution = ticket.time_resolved - ticket.time_first_responded
        seconds_to_resolution = time_to_resolution.total_seconds()
        hours_to_resolution = seconds_to_resolution / SECONDS_PER_HOUR

        ticket_resolution_list.append(hours_to_resolution)

        agent_touches = [float(ticket.num_agent_touches)]

        ticket_touches_list.append(agent_touches)


        ticket_resolutions = np.array(ticket_resolution_list, float)
        print ticket_resolutions
        ticket_touches = np.array(ticket_touches_list, float)
        print ticket_touches

        index_half_resolutions = len(ticket_resolutions)/2
        print index_half_resolutions
        index_half_touches = len(ticket_touches)/2
            #Get the data for the dependent variable, the response time, separated into training and testing sets 
        print index_half_touches

        resolutions_train = ticket_resolutions[:-index_half_resolutions]
        
        resolutions_test = ticket_resolutions[index_half_resolutions:]
       

        #Get the data for the independent variable, the submission time, separated into training and testing sets
        touches_train = ticket_touches[:-index_half_touches]
        touches_test = ticket_touches[index_half_touches:]
        # print submissions_test

        model = linear_model.LinearRegression()
        test = model.fit(touches_train, resolutions_train)
         
        # The coefficients
        print('Coefficients: \n', model.coef_)
        # The mean square error
        print("Residual sum of squares: %.2f"
              % np.mean((model.predict(touches_test) - resolutions_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % model.score(touches_test, resolutions_test))


    scatter_list = []
    line_list = []
    data = {'scatter_points':scatter_list, 'line_points':line_list}
    for i in range(0, index_half_resolutions):
        # data['scatter_points'].append([submissions_test[i][0], responses_test[i]])
        data['scatter_points'].append(resolutions_test[i])
        data['line_points'].append([touches_test[i][0], model.predict(touches_test[i][0]).tolist()])
        # print "Line"
        # print line_list


    print "DATA"
    print data
    return data