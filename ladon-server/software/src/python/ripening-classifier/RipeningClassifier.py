## IMPORTS ##
import json
import sys
import numpy as np
import pandas as pd

from sklearn.svm import SVC

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

# Sending answer
print( json.dumps( classifiedData.tolist() ) )
sys.stdout.flush()

sys.exit()
