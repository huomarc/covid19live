import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import State
from sqlalchemy.orm import Session
from covid import Covid

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory = "templates")

covid = Covid()


class StateRequest(BaseModel):
	state: str

def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
	"""
	Displays COVID-19 Live Data Homepage Dashboard
	"""
	#countries_list = covid.list_countries()
	countries = db.query(State).all()
	return templates.TemplateResponse("dashboard.html", {
		"request": request,
		"countries": countries
	})

def fetch_data(id: str):
	db = SessionLocal()

	country = db.query(State).filter(State.id == id).first()

	state_data = covid.get_status_by_country_name(country.state)

	country.id = state_data['id']
	
	country.state = state_data['country'].capitalize()
	
	country.confirmed = state_data['confirmed'] 
	
	country.active = state_data['active'] 
	
	country.deaths = state_data['deaths'] 
	
	country.recovered = state_data['recovered'] 

	db.add(country)
	db.commit()

@app.post("/state")
async def create_state(state_request: StateRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	Creates a new state and stores in database
	"""
	state = State()
	state.state = state_request.state
	
	db.add(state)
	db.commit()

	background_tasks.add_task(fetch_data, state.id)

	return {
		"code" : "success",
		"message" : "state created"
	}



#covid19 raw: https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv