from sklearn import datasets, linear_model
from datetime import datetime
import numpy as np

SECONDS_PER_HOUR = 3600

def get_response_regression(tickets_in_range):
    ticket_response_list = []
    ticket_submit_list = []
    
    for ticket in tickets_in_range:
        ticket_submitted_hour = float(ticket.time_submitted.hour)
        ticket_submitted_minutes = float(ticket.time_submitted.minute)
        ticket_submitted = [ticket_submitted_hour + (ticket_submitted_minutes/60)]
        

        time_to_first_response = ticket.time_first_responded - ticket.time_submitted
        seconds_to_first_response = time_to_first_response.total_seconds()
        hours_to_first_response = seconds_to_first_response / SECONDS_PER_HOUR
        # print seconds_to_first_response
        # print hours_to_first_response
        
        ticket_submit_list.append(ticket_submitted)
        ticket_response_list.append(hours_to_first_response)
    

    ticket_responses = np.array(ticket_response_list, float)
    ticket_submissions = np.array(ticket_submit_list, float)

    index_half_responses = len(ticket_responses)/2
    index_half_submissions = len(ticket_submissions)/2
        #Get the data for the dependent variable, the response time, separated into training and testing sets 
    responses_train = ticket_responses[:-index_half_responses]
    
    responses_test = ticket_responses[index_half_responses:]
   

    #Get the data for the independent variable, the submission time, separated into training and testing sets
    submissions_train = ticket_submissions[:-index_half_submissions]
    submissions_test = ticket_submissions[index_half_submissions:]
    # print submissions_test

    model = linear_model.LinearRegression()
    test = model.fit(submissions_train, responses_train)
     
    # The coefficients
    print('Coefficients: \n', model.coef_)
    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((model.predict(submissions_test) - responses_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % model.score(submissions_test, responses_test))

    print type(submissions_test[0])


    scatter_list = []
    line_list = []
    data = {'scatter_points':scatter_list, 'line_points':line_list}
    for i in range(0, index_half_responses):
        data['scatter_points'].append([submissions_test[i][0], responses_test[i]])
        print "Scatter"
        print scatter_list
        data['line_points'].append([submissions_test[i][0], model.predict(responses_test[i]).tolist()])
        print "Line"
        print line_list

    print "Data"
    print data
    return data
