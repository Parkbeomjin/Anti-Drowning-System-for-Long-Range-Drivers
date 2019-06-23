# -*- coding: utf-8 -*- 
import os
import cv2
import timeit
import numpy as np
import tensorflow as tf
from imutils.video import FPS
import imutils
import time
import urllib.request
import urllib
#import urlopen
import json

NUM = 0 #yawn
NUM2 = 0
COUNT = 0 #closeeye
COUNT2 = 0

camera = cv2.VideoCapture(0)

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
               in tf.gfile.GFile('./final_output_labels.txt')]

def grabVideoFeed():
    grabbed, frame = camera.read()
    return frame if grabbed else None

def initialSetup():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    start_time = timeit.default_timer()

    # This takes 2-5 seconds to run
    # Unpersists graph from file
    with tf.gfile.FastGFile('./final_output_graph.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

def sendNotification(token, channel,message):
    data = {
      "body" : message,
      "message_type" : "text/plain:"
    }
    req = urllib.request.Request('http://api.pushetta.com/api/pushes/eyes_detected/'.format(channel))
    #req = urllib2.Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel))
    
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {0}'.format(token))

    response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))
    #response = urllib2.urlopen(req, json.dumps(data).encode('utf-8'))


initialSetup()
with tf.Session() as sess:
    start_time = timeit.default_timer()

    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    

    fps = FPS().start()

    while True:
        frame = grabVideoFeed()
        
        if frame is None:
            raise SystemError('Issue grabbing the frame')

        frame = cv2.resize(frame, (299, 299), interpolation=cv2.INTER_CUBIC)
        #frame = cv2.resize(frame, None, interpolation=cv2.INTER_CUBIC)
        
        cv2.imshow('Eyes_detect', frame)

        # adhere to TS graph input structure
        numpy_frame = np.asarray(frame)
        numpy_frame = cv2.normalize(numpy_frame.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
        numpy_final = np.expand_dims(numpy_frame, axis=0)

        start_time = timeit.default_timer()

        # This takes 2-5 seconds as well
        predictions = sess.run(softmax_tensor, {'Mul:0': numpy_final})

        

        start_time = timeit.default_timer()

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %f)' % (human_string, score))
            if  human_string == "closeeye" and score > 0.8: 
                COUNT = COUNT + 1   
                if  COUNT == 10:
                    print('close eye detected')
                    print(COUNT) 
                    sendNotification("1358a81a376ef686a0bb9ba7a931f3315730f65b","Sleep detected!!!","Sleep detected!!!") #푸시 알림 보내기
                    COUNT = 0
                elif human_string == "openeye" and score > 0.8:
                    COUNT2 = COUNT2 + 1
                    if COUNT2 == 10:
                        COUNT = 0
                        COUNT2 = 0
            elif human_string == "closeeye" and score < 0.8:
                print('close eye not detected') 
            elif human_string == "yawn" and score > 0.8:
                NUM = NUM + 1
                if NUM == 10:
                    print('yawn detected')  
                    print(NUM) 
                    sendNotification("1358a81a376ef686a0bb9ba7a931f3315730f65b","Sleep detected!!!","Sleep detected!!!")
                    NUM = 0 
                elif human_string == "openeye" and score > 0.8:
                    NUM2 = NUM2 + 1
                    if NUM2 == 10:
                        NUM = 0
                        NUM2 = 0
            elif human_string == "yawn" and score < 0.8:
                print('yawn not detected') 

        print ('********* Session Ended *********')

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
        fps.update()

             
fps.stop()
camera.release()
cv2.destroyAllWindows()
