from django.shortcuts import render
from django.http import HttpResponse

import json

import tensorflow as tf
import tensorflow.keras.layers as tfl 
import numpy as np
import cv2

from myapp.models import Car
from myapp.models import Prediction


def modelPreperation():
    try:
        return tf.keras.models.load_model("/home/mednoun/Programming/hackathons/nasaSpaceAppsChallenge/tuto/Simple-RESTful-API-with-Django/myapi/myapp/public/AI_model")
    except Exception as e:
        print(e)
    
def makePrediction(image):
    resize_and_rescale_224 = tf.keras.Sequential([
            tfl.experimental.preprocessing.Resizing(224, 224),
            tfl.experimental.preprocessing.Rescaling(1./255)
    ])
    try:
        path="/home/mednoun/Programming/hackathons/nasaSpaceAppsChallenge/tuto/Simple-RESTful-API-with-Django/myapi/myapp/public/images"+image
        img = np.array(resize_and_rescale_224(cv2.imread(path,cv2.IMREAD_UNCHANGED))).reshape((1,224,224,3))
        new_model = modelPreperation()
        feat=new_model.predict(img)
        pred = 0 if feat[0][0]<0.5 else 1
        return (path, pred)
    except Exception as e:
        print(e)

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

def get_prediction(request, pred):
    if request.method == 'GET':
        try:
            prediction = Prediction.objects.get(id=pred)
            response = json.dumps([
                { 
                
                'Path': prediction.path, 
                'Pred': prediction.prediction, 
                'coor':
                    {
                        'long':prediction.long, 
                        'lati':prediction.lat
                    }

                }
            ])
        except:
            response = json.dumps([{ 'Error': 'No car with that name'}])
    return HttpResponse(response, content_type='text/json')

def get_car(request, car_name):
    if request.method == 'GET':
        try:
            car = Car.objects.get(name=car_name)
            response = json.dumps([{ 'Car': car.name, 'Top Speed': car.top_speed}])
        except:
            response = json.dumps([{ 'Error': 'No car with that name'}])
    return HttpResponse(response, content_type='text/json')

def put_prediction():
    pathe,pred=makePrediction("0_03.jpeg")
    obj = Prediction(path=pathe, prediction = pred, long=np.random.rand()*10, lat=np.random.rand()*10)
    try:
        obj.save()
        print("saved successfuly ")
    except:
        print("not saved")


