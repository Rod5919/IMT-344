# -*- coding: utf-8 -*-
"""Ejercicio2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HoXD_63B_gfFalGgQk59w9nvwHEHLFy5

# Problem 2

# Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import cv2
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# %matplotlib inline
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"


"""# Creating dataset"""

m_files = ["with_mask/"+str(x)+"-with-mask.jpg" for x in range(1,479)]
# m_files
nm_files = ["without_mask/"+str(x)+".jpg" for x in range(1,479)]
nm_files

data_path = 'observations/experiements/data/'

X = m_files + nm_files

X = [data_path+x for x in X]
images = [cv2.imread(x, cv2.COLOR_BGR2GRAY) for x in X]
images

out = list(np.ones(478))
out = out + list(np.zeros(478))
out

df = pd.DataFrame(zip(images,out), columns=['x','y'])

X = df['x']
y = df['y']

X.shape
y.shape
print(y)
pd.Series(y).value_counts()
classes = [0, 1]
nclasses = len(classes)

"""## Training"""

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=9, test_size=0.2)
#scaling the features
X_train_scaled = X_train/255.0
X_test_scaled = X_test/255.0

clf = LogisticRegression(penalty='none', 
                         tol=0.1, solver='saga',
                         multi_class='multinomial')

clf.fit(X_train_scaled, y_train)

#to check the shape of the coefficient matrix
clf.coef_.shape

scale = np.max(np.abs(clf.coef_))

p = plt.figure(figsize=(25, 2.5));

for i in range(nclasses):
    p = plt.subplot(1, nclasses, i + 1)
    p = plt.imshow(clf.coef_[i].reshape(28, 28),
                  cmap=plt.cm.RdBu, vmin=-scale, vmax=scale);
    p = plt.axis('off')
    p = plt.title('Class %i' % i);

"""# Accuracy"""

print('Accuracy: %.2f' % accuracy_score(y_test, pred))

"""# Predict"""

num = 0 #@param {type:"slider", min:0, max:55, step:1}

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.title({0:'Sin barbijo', 1:'Con barbijo'}[clf.predict(frame)])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()