from fastapi import FastAPI
from routers import tabs

app = FastAPI(title='Tabu Book API')

#routes
app.include_router(tabs.router)

@app.get('/') 
def home():
    return {'message': 'api running'}
