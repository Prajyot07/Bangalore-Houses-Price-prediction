from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
import util
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your allowed origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Update with allowed HTTP methods
    allow_headers=["*"],  # Update with allowed headers if needed
)

@app.get('/get_location_names')
async def get_location_names():
    try:
        locations = util.get_location_names()
        return JSONResponse(content={'locations': locations})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/predict_home_price')
async def predict_home_price(total_sqft: float = Form(...), location: str = Form(...), bhk: int = Form(...), bath: int = Form(...)):
    try:
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return JSONResponse(content={'estimated_price': estimated_price})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting FastAPI Server For Home Price Prediction...")
    util.load_saved_artifacts()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
