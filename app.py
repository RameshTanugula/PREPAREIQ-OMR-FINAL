#!/usr/bin/env python
# coding: utf-8

# In[11]:


from flask import Flask, jsonify, request
import cv2
import numpy as np
import pandas as pd
from uuid import uuid4
from utils1 import find_paper,id_read,read_answer
import matplotlib.pyplot as plt
from skimage import io
import json
app = Flask(__name__)

# @app.route('/home')
# def hello_world():
# 	print("working main route")
# 	return 'Hello World!'

@app.route("/index")
def index():
    return _test("My Test Data")

def _test(argument):
    return "TEST: %s" % argument

@app.route('/', methods=['GET', 'POST'])
def submit_omr():
    data = request.get_json()
    print(data)
    file = data['file']
    key = data['key']
    test_id1 = data['testId']
    roll_no = data['rollNo']
    image = io.imread(file)
    d=find_paper(image)
    ## Answers Read   
    s_id=d[195:450,35:305]
    t_id=d[195:450,355:435]
    q1=d[520:645,90:195]
    q2=d[695:820,90:195]
    q3=d[875:1000,90:195]
    q4=d[1050:1175,90:195]
    q5=d[520:645,275:385]
    q6=d[695:820,275:385]
    q7=d[870:995,275:385]
    q8=d[1050:1175,275:385]
    q9=d[520:645,460:570]
    q10=d[695:820,460:570]
    q11=d[870:995,460:570]
    q12=d[1045:1170,460:570]
    q13=d[520:645,645:755]
    q14=d[695:820,645:755]
    q15=d[870:995,645:755]
    q16=d[1045:1170,645:755]
    q17=d[520:645,830:940]
    q18=d[695:820,830:940]
    q19=d[870:995,830:940]
    q20=d[1045:1170,830:940]
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
        s11=read_answer(q11)
        s12=read_answer(q12)
        s13=read_answer(q13)
        s14=read_answer(q14)
        s15=read_answer(q15)
        s16=read_answer(q16)
        s17=read_answer(q17)
        s18=read_answer(q18)
        s19=read_answer(q19)
        s20=read_answer(q20)
        final=s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11+s12+s13+s14+s15+s16+s17+s18+s19+s20
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

if __name__ == '__main__':
    app.run()
