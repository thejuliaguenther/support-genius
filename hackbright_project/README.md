# SupportGenius

SupportGenius turns support tickets into valuable customer insights. Designed for customer success and support managers in data-driven organizations, SupportGenius leverages the power of machine learning to predict how customer and agent actions influence each other and identify similar customers. This, along with statistics such as the most common times that tickets are submitted, allows users to make smarter decisions about customer success and support strategy.  

## Technical Stack
PostgreSQL, Scikit-learn, NumPy, D3.js, Highcharts.js, Python fake-factory, Python, SQLAlchemy, Flask, JavaScript, jQuery, jQueryUI, AJAX, HTML/CSS, Bootstrap, Mashape Text-Processing API (Sentiment Analysis API)
 
## Data
This is an enterprise software application. In this demo, the data represents the support tickets from October 2015 for a fictitious company that sells to businesses. Thus, the data is reandomly created.
- Ticket contents were generated using Markov chains in Python creating new text snippets from separate positive and negative text files
- Agent names are members of Hackbright Cohort 12
- Company names were created using a [random company name generator](http://online-generator.com/name-generator/company-name-generator.php)
-Customer names were randomly generated using the [Python fake-factory library](https://pypi.python.org/pypi/fake-factory)
-Ticket submission, first response, and resolution times were randomly generated using Python fake-factory library 
-Agents were randomly assigned to tickets; customers were randomly assigned to companies, roles, and tickets; and companies were randomly assigned to different locations, support tiers, and industries. 

## Features
-D3.js: Ticket Data Graphs
**Heatmap of tickets per hour per day with the darkest boxes having the most tickets submitted
**Tickets by industry and tickets by support tier (Gold, Silver, or Bronze with Gold being the highest tier; represents the customer's purchased customer success plan) graphs 
-Highcharts.js: Scikit-learn Machine Learning Graphs
**Linear regression calculated using scikit-learn; shows the realationship between the time of day a ticket is submitted and the time it takes an agent to respond to the ticket
**Linear regression calculated using scikit-learn; shows the relationship between the number of agent touches (the number of times the agent reaches out to a customer) and the amount of time it takes to resolve the ticket
-jQuery UI: Cluster Information Box
**Provides a drilldown into the 
