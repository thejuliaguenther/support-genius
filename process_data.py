import pandas as pd 
import datetime
import numpy as np

from sklearn.cluster import KMeans
#This line reads in an excel file and converts it to a pandas DataFrame
data= pd.read_excel('ticket_contents.xls')

#This line gets all of the times that tickets were submitted 
times_submitted = data.iloc[:,[2]]

# print type(data)
#Total number of clusters = 24 * 7 = 168
# n_clusters = 168



