import os
import httpx
from urllib import parse
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import Text, List, Optional
from apps.beers_api.security import get_api_key

app = FastAPI(
    version='1.0.0',
    title='Beers API',
    description='Beers API Documentation',
    docs_url=None,
    redoc_url='/docs'
)


class BeerVolume(BaseModel):
    value: float
    unit: Text


class Beer(BaseModel):
    id: int
    name: Text
    description: Text
    image_url: Text
    ph: float
    volume: BeerVolume


class BeerCollection(BaseModel):
    items: List[Beer]
    count: int


async def get_beers_from_punk_api(page: int, per_page: int, beer_name: Optional[Text] = None) -> List[Beer]:
    query_params = {'page': page, 'per_page': per_page}

    if beer_name:
        query_params['beer_name'] = beer_name.replace(' ', '_')

    query_parameters = parse.urlencode(query_params)

    async with httpx.AsyncClient() as client:
        raw_beers = await client.get(f"{os.getenv('PUNK_API_BASE_URL')}/beers?{query_parameters}")
        return [Beer(**beer) for beer in raw_beers.json()]


@app.get("/v1/beers")
async def get_beers_listing(page: int = 1, per_page: int = 10) -> BeerCollection:
    beers = await get_beers_from_punk_api(page, per_page)
    return BeerCollection(items=beers, count=beers.__len__())


@app.get("/v1/beers/{beer_name}")
async def get_beer_by_name(beer_name: Text) -> BeerCollection:
    beers = await get_beers_from_punk_api(1, 1, beer_name)
    return BeerCollection(items=beers, count=beers.__len__())


@app.get("/v1/secured/beers", dependencies=[Depends(get_api_key)])
async def get_beers_listing_secured(page: int = 1, per_page: int = 10) -> BeerCollection:
    beers = await get_beers_from_punk_api(page, per_page)
    return BeerCollection(items=beers, count=beers.__len__())
