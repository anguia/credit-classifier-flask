#! /usr/bin/python
import sys
import tensorflow as tf
import numpy as np
from numpy import genfromtxt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support

# Tensorflow convinience functions
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Constants
num_neurons = 124
num_classes = 2 

# Get a test 
dataset = genfromtxt(sys.argv[3], delimiter=',')
rows, cols = dataset.shape
 
x_width = cols-2
# assume the last 2 columns are the label

# Placeholder values
x = tf.placeholder(tf.float32, [None, x_width])

# Neural network with 5 hidden layers

# Fully connected layer 1:
w_fc1 = weight_variable([x_width, num_neurons])       # weights
b_fc1 = bias_variable([num_neurons])                  # biases
h_fc1 = tf.nn.relu(tf.matmul(x, w_fc1) + b_fc1)       # activation
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)          # dropout

# Fully connected layer 2:
w_fc2 = weight_variable([num_neurons, num_neurons])
b_fc2 = bias_variable([num_neurons])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

# Fully connected layer 3:
w_fc3 = weight_variable([num_neurons, num_neurons])
b_fc3 = bias_variable([num_neurons])
h_fc3 = tf.nn.relu(tf.matmul(h_fc2_drop, w_fc3) + b_fc3)
h_fc3_drop = tf.nn.dropout(h_fc3, keep_prob)

# Fully connected layer 4:
w_fc4 = weight_variable([num_neurons, num_neurons])
b_fc4 = bias_variable([num_neurons])
h_fc4 = tf.nn.relu(tf.matmul(h_fc3_drop, w_fc4) + b_fc4)
h_fc4_drop = tf.nn.dropout(h_fc4, keep_prob)

# Fully connected layer 5:
w_fc5 = weight_variable([num_neurons, num_neurons])
b_fc5 = bias_variable([num_neurons])
h_fc5 = tf.nn.relu(tf.matmul(h_fc4_drop, w_fc5) + b_fc5)
h_fc5_drop = tf.nn.dropout(h_fc5, keep_prob)

# Fully connected layer 6:
w_fc6 = weight_variable([num_neurons, num_neurons])
b_fc6 = bias_variable([num_neurons])
h_fc6 = tf.nn.relu(tf.matmul(h_fc5_drop, w_fc6) + b_fc6)
h_fc6_drop = tf.nn.dropout(h_fc6, keep_prob)

h_fcout_t = h_fc6_drop                                                                                               
# Readout layer
w_fc_out = weight_variable([num_neurons, num_classes])
b_fc_out = bias_variable([num_classes])

# The softmax function will make probabilties of Good vs Bad score at the output
y_ = tf.nn.softmax(tf.matmul(h_fcout_t, w_fc_out) + b_fc_out)
y = tf.placeholder(tf.float32, [None, num_classes])

# Define tf session
sess = tf.Session()
 
# Define saver for model
saver = tf.train.Saver()
#saver = tf.train.Saver([w_fc_out, b_fc_out])

# Restore model
restore_model = sys.argv[4]
saver.restore(sess, restore_model)

print ("restore model successful!!!")

# Evaluate the predicted values
start = int(sys.argv[1])
end = int(sys.argv[2])

feed_dict = {x:dataset[start:end, 0:59],keep_prob: 1.0 }
result = sess.run(y_, feed_dict)
print("---PredictionResult---")
print("Good:%f\tBad:%f" % (result[0,0], result[0,1]))

# Get the ground truth values
yT = np.argmax(dataset[901:1000, 59:61], axis=1)
# Evaluate the predicted values
y_p = tf.argmax(y_,1)
feed_dict={x: dataset[901:1000,0:59], y: dataset[901:1000,59:61], keep_prob: 1.0}
yP = sess.run(y_p, feed_dict)

# Metrics and confusion matrix
[precision, recall, f_score, _] = precision_recall_fscore_support(yT, yP, average='macro'    )
print("---Validation---")
print("precision:%f\trecall:%f\tf-score:%f" % (precision, recall, f_score))

conmat = confusion_matrix(yT, yP)
print("---ConfusionMatrix---")
print("P-Good-A-Good:%d\t P-Good-A-Bad:%d" % (conmat[0,0],conmat[0,1]))
print("P-Bad-A-Good:%d\t P-Bad-A-Bad:%d" % (conmat[1,0],conmat[1,1]))

