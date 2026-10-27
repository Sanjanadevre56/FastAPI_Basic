from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated , Literal

app=FastAPI()
# Patient is a pydantic object
class Patient(BaseModel):
    id:Annotated[str,Field(...,description="id of the patient",examples=["P001"])]
    name:Annotated[str,Field(...,description="name of the patient")]
    city:Annotated[str,Field(...,description="city where the patient live")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description="height of the patient in mtrs")]
    weight:Annotated[float,Field(...,gt=0,description="weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'


def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patient.json",'w')as f:
        json.dump(data,f)


@app.get('/')
def hello():
    return {'message':'Patient Management System'}

@app.get('/about')
def about():
    return {'message':'A Fully Functional Patient Management System To Manage Your Patient Data '}

#view patient data
@app.get('/view')
def view():
    data=load_data()
    return data

#view patient data with patient id 
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description='id of the patient in the db',examples='P001')):
    #load all the patients
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404 ,detail='patient not found')

# example = http://127.0.0.1:8000/student?name=Sanjana&age=20
# ... means required data 

# sort the data
@app.get('/sort')
def sort_patient(sort_by:str = Query(...,description='sort on the basis of w8 height or bmi') , order:str = Query('asc' , description='sort in asc or desc order')):
    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field selected from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid order selected btw asc and desc')

    data=load_data()

    sort_order= True if order=='desc' else False

    sorted_data = sorted(data.values() ,key=lambda x:x.get(sort_by,0) , reverse=sort_order)
    
    return sorted_data

@app.post('/create')
def create_patient(patient : Patient):

    #Load the existing data
    data=load_data()

    #Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient already exists")

    #new patient add to databse 
    #model_dump() converts pydantic obj to dict
    data[patient.id]=patient.model_dump(exclude=[id])

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

