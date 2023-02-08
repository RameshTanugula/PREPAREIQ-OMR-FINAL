#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
import pandas as pd
from uuid import uuid4
from utils1 import find_paper,id_read,read_answer
import matplotlib.pyplot as plt
from skimage import io
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '1'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

@app.route('/submit', methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def submit_omr():
    data = request.get_json()
    print(data)
    file = data['file']
    key = data['key']
    test_id1 = data['testId']
    roll_no = data['rollNo']
    image = io.imread(file)
    d=find_paper(image)
    def answers():
        q1=d[310:750,50:180]
        q2=d[750:1190,50:180]
        q3=d[310:750,255:380]
        q4=d[750:1190,255:380]
        q5=d[310:750,455:585]
        q6=d[750:1190,455:585]
        q7=d[310:750,660:790]
        q8=d[750:1190,660:790]
        q9=d[310:750,860:990]
        q10=d[750:1190,860:995]

        s1=read_answer(q1) 
        s2=read_answer(q2)
        s3=read_answer(q3) 
        s4=read_answer(q4) 
        s5=read_answer(q5)
        s6=read_answer(q6)
        s7=read_answer(q7)
        s8=read_answer(q8)
        s9=read_answer(q9)
        s10=read_answer(q10)
        final=s1+s2+s3+s4+s5+s6+s7+s8+s9+s10
        return final
    def s_id_reader():
        std_1=d[55:260,10:35]
        std_2=d[55:260,35:60]
        std_3=d[55:260,60:85]
        std_4=d[55:260,85:110]
        std_5=d[55:260,110:135]
        std_6=d[55:260,135:160]
        std_7=d[55:260,160:185]
        std_8=d[55:260,185:210]
        std_9=d[55:260,210:235]
        std_10=d[55:260,235:260]

        st_1=id_read(std_1) 
        st_2=id_read(std_2)
        st_3=id_read(std_3)
        st_4=id_read(std_4)
        st_5=id_read(std_5)
        st_6=id_read(std_6)
        st_7=id_read(std_7)
        st_8=id_read(std_8)
        st_9=id_read(std_9)
        st_10=id_read(std_10)
        student_Id=st_1+st_2+st_3+st_4+st_5+st_6+st_7+st_8+st_9+st_10
        return student_Id
    def t_id_reader():
        t_id_1=d[55:260,280:305]
        t_id_2=d[55:260,310:335]
        t_id_3=d[55:260,340:365]
        t_1=id_read(t_id_1) 
        t_2=id_read(t_id_2)
        t_3=id_read(t_id_3)
        t_Id=t_1+t_2+t_3
        return t_Id 
    bubbled = None
    student_id = None
    test_id = None

    try:
        bubbled = answers()
    except ValueError:
        print("Bubbled answers are not found")

    try:
        student_id = s_id_reader()
    except ValueError:
        print("student_id is not found")

    try:
        test_id = t_id_reader()
    except ValueError:
        print("test_id is not found")
    
    marks = 0
    for i in range(len(key)):
        if key[i] == 0:
            marks += 1
        elif key[i] == bubbled[i]:
            marks += 1
    total=marks
    none_count = len([x for x in bubbled if x is None])
    worng=100-total-none_count
    k=(student_id==roll_no)
    h=(test_id==test_id1)
    return {"Rollno_matched":k,"TestId_matched":h,"Answered":bubbled,"Key":key,"Total_marks":total,"Total_worng":worng,"Count_None_values":none_count}
#     return jsonify({"message":"successful"})

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=80)

