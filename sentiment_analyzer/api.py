from typing import Dict
from starlette.responses import JSONResponse
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .model import Model, get_model
import logging
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Sentiment Model API",
    description="A simple API that uses an NLP model to predict the sentiment of movie reviews",
    version="0.1",)
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Specify the location of static files (HTML, CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
# Define the root route
@app.get("/")
def root():
    # Return the welcome message
    return {"message": "Welcome to the Sentiment Model API!"}

@app.get("/predict-review")
async def predict_review_sentiment(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict")
async def predict_text(text: str):
    model = get_model()
    sentiment, confidence = model.predict(text)
    return JSONResponse(content={
        "sentiment":sentiment, "confidence":confidence
    })
# Define the prediction route for POST requests    
#@app.post("/predict-review")#, response_model=SentimentResponse
#async def predict(request: SentimentRequest, model: Model = Depends(get_model)):
#    sentiment, confidence = model.predict(request.text)
#    return JSONResponse(content={
#        "sentiment":sentiment, "confidence":confidence
#    })
    
if __name__ == "__main__":
    # Start the Flask server
    logger = logging.getLogger("uvicorn.error")
    logger.propagate = False
    uvicorn.run(app, host="127.0.0.1", port=8000)