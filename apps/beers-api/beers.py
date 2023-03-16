from fastapi import FastAPI

app = FastAPI(
    version='1.0.0',
    title='Beers API',
    description='Beers API Documentation',
    docs_url=None,
    redoc_url='/docs'
)

