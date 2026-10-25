from fastapi import FastAPI
import json

app=FastAPI()

def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
        return data

@app.get('/')
def hello():
    return {'message':'Patient Management System'}

@app.get('/about')
def about():
    return {'message':'A Fully Functional Patient Management System To Manage Your Patient Data '}

@app.get('/view')
def view():
    data=load_data()
    return data