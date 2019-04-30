# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:21:02 2019

@author: manulsl1
"""

import tensorflow as tf

# Create TensorFlow object called hello_constant
hello_constant = tf.constant('Hello World!')

with tf.Session() as sess:
    # Run the tf.constant operation in the session
    output = sess.run(hello_constant)
    print(output)