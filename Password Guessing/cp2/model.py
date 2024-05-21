import numpy
from sklearn.naive_bayes import GaussianNB

class NBClassifier:
    def __init__(self):
        self.clf = GaussianNB()

    def train(self, train_x, train_y):
        self.clf.fit(train_x, train_y)
    
    # input: text_x(np.array with shape(1,18)), the vectorized feature of a string password
    # output: the predicted class of the password (among 0,1,2,3,4,5,6, the exact meaning of each class is listed in a variable "guess_class_index" in pipeline.py)
    def predict(self, test_x):
        return self.clf.predict(test_x)
    
    # input: text_x(np.array with shape(1,18)), the vectorized feature of a string password
    # output: a np.array with shape(1,7), representing the probability of the password belonging to each class (among 0,1,2,3,4,5,6, the exact meaning of each class is listed in a variable "guess_class_index" in pipeline.py)
    def predict_proba(self, test_x):
        return numpy.array(self.clf.predict_proba(test_x))
