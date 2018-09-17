## IMPORTS ##
import json 					# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax
import sys 						# Sys: system-specific parameters and functions
import numpy as np 				# NumPy: the fundamental package for scientific computing with Python
import pandas as pd 			# Pandas: easy-to-use data structures and data analysis tools for Python

from sklearn.svm import SVC 	# scikit-learn: Simple and efficient tools for data mining and data analysis

## MAIN ##

# Loading samples to train classifier
samples = pd.read_csv('/usr/share/ladon/ripening-classifier/sample_data.csv', sep=",", index_col=0)

# Separating into labels for classifying and data
x = samples.drop('maturity', axis=1)  # Attributes
y = samples['maturity']               # Labels

# Preparing classifier
svclassifier = SVC(kernel='linear')  
svclassifier.fit(x, y)

# Preparing data
bMax = float(sys.argv[1])
aMax = float(sys.argv[2])
aMin = float(sys.argv[3])
lMedian = float(sys.argv[4])

toClassify = [bMax, aMax, aMin, lMedian]
toClassify = pd.DataFrame(toClassify).T

# Classifying data
classifiedData = svclassifier.predict(toClassify)

# Printing answer
print( json.dumps( classifiedData.tolist() ) )
sys.stdout.flush()

sys.exit()
