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
print('post submit', data)
    print(data)
    file = data['file']
    key = data['key']
    test_id1 = data['testId']
    roll_no = data['rollNo']
    image = io.imread(file)
    d=find_paper(image)
    ## Answers Read   
    s_id=d[75:345,15:305]
    t_id=d[75:345,340:435]

    q1=d[430:990,60:215] #1/2 part of q1
    q2=d[1000:1580,60:215] #2/2 part of q1

    q3=d[425:990,305:460] #1/2 part of q2
    q4=d[1000:1580,305:460] #2/2 part of q2

    q5=d[425:990,550:705] #1/2 part of q3
    q6=d[1000:1580,550:705] #2/2 part of q3

    q7=d[425:990,795:950] #1/2 part of q4
    q8=d[1000:1580,795:950] #2/2 part of q4

    q9=d[425:990,1030:1190] #1/2 part of q5
    q10=d[1000:1580,1030:1190] #2/2 part of q5

    def answers():
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
    def convert(list):
        s = [str(i) for i in list]
        res = int("".join(s))
        return(res)
    y=id_read(s_id)
    student_id=convert(y)
    x=id_read(t_id)
    test_id=convert(x)
    bubbled=answers()
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

