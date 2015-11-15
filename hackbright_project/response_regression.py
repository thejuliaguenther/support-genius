# import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
import random 
import sklearn 
from sklearn import linear_model

#load the file from a csv into a numpy array 
ticket_responses = genfromtxt('responded_tickets.csv', delimiter=',')
ticket_submissions = genfromtxt('submitted_tickets.csv', delimiter=',')
#spilt the file into training and testing sets 
#linear regression 

#Get the data for the dependent variable, the response time, separated into training and testing sets 
responses_train = ticket_responses[:-150]
responses_test = ticket_responses[-150:]

#Get the data for the independent variable, the submission time, separated into training and testing sets
submissions_train = ticket_submissions[:-150]
submissions_test = ticket_submissions[-150:]

model = linear_model.LinearRegression()
model.fit(submissions_train, responses_train)

# The coefficients
print('Coefficients: \n', model.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((model.predict(submissions_test) - responses_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % model.score(submissions_test, responses_test))

# print ticket_responses

# np.random.seed(0)
# X = np.random.random(size=(20, 1))
# y = 3 * X.squeeze() + 2 + np.random.normal(size=20)

# # Fit a linear regression to it
# model = linear_model.LinearRegression(fit_intercept=True)
# model.fit(X, y)
# print ("Model coefficient: %.5f, and intercept: %.5f"
#        % (model.coef_, model.intercept_))

# # Plot the data and the model prediction
# X_test = np.linspace(0, 1, 100)[:, np.newaxis]
# y_test = model.predict(X_test)

# plt.plot(X.squeeze(), y, 'o')
# plt.plot(X_test.squeeze(), y_test);