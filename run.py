from flask import Flask, render_template, request
from datetime import datetime
from mongoengine import connect, Document, StringField, IntField, FloatField, DateTimeField
from pymongo import MongoClient

app= Flask(__name__)
app.config['SECRET_KEY']='wanderlust'

connect('ecgdata')

client=MongoClient()
db=client.ecgdata

class ecgMonitor(Document):
    value=FloatField()
    name=StringField()
    age=IntField()
    sample_number=IntField()
    result=IntField()
    record_date= DateTimeField()
    

def resultDecide(heartCheck):
    print(heartCheck)
    if heartCheck==4:
        condition="Normal"
    elif heartCheck==6:
        condition="bad"
    else:
        condition="worse"
    return condition

@app.route('/')
def hello_world():
    db_datas=ecgMonitor.objects
    return render_template('index.html', datas=db_datas, dateHere=datetime.now())

@app.route('/api/postdata', methods=['POST'])
def data_post_handler():
    post_data=request.json
    current_date=datetime.now()
    print(current_date)
    db_cursor = ecgMonitor(value=float(post_data.get('value')),
     name=str(post_data.get('name')), 
     age=int(post_data.get('age')), 
     sample_number=int(post_data.get('sample_number')), 
     result=int(post_data.get('result')), record_date=current_date )
    db_cursor.save()
    return "Data saved"
    

    #result=int(post_data.get('result')),



if __name__=='__main__':
    app.run(debug=True)