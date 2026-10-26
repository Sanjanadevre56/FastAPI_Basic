from fastapi import FastAPI , Path , HTTPExeption , Query
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

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description='id of the patient in the db',example='P001')):
    #load all the patients
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPExeption(status_code=404 ,detail='patient not found')

# example = http://127.0.0.1:8000/student?name=Sanjana&age=20
# ... means required data 


@app.get('/sort')
def sort_patient(sort_by:str = Query(...,description='sort on the basis of w8 height or bmi') , order:str = Query('asc' , description='sort in asc or desc order')):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPExeption(status_code=400,detail=f'invalid field selected from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPExeption(status_code=400,detail='invalid order selected btw asc and desc')

    data=load_data()

    sort_order= True if order=='desc' else False

    sorted_data = sorted(data.values() ,key=lambda x:x.get(sort_by,0) , reverse=sort_order)
    
    return sorted_data

