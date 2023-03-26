from fastapi import FastAPI
from apps.beers_api.routes.router import beer_router

app = FastAPI(
    version='1.0.0',
    title='Beers API',
    description='Beers API Documentation',
    docs_url=None,
    redoc_url='/docs'
)

app.include_router(prefix='/v1/beers', router=beer_router)
