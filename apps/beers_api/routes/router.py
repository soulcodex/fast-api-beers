import os
import httpx
from urllib import parse
from fastapi import APIRouter
from typing import Text, List, Optional
from apps.beers_api.ui.beer import Beer, BeerCollection

beer_router = APIRouter(tags=['Beers'])


async def get_beers_from_punk_api(page: int, per_page: int, beer_name: Optional[Text] = None) -> List[Beer]:
    parameters = ''
    query_params = {}

    if beer_name:
        query_params['beer_name'] = beer_name.replace(' ', '_')

    if page > 0:
        query_params['page'] = page

    if per_page > 0:
        query_params['per_page'] = per_page

    if query_params.__len__() > 0:
        parameters = f'?{parse.urlencode(query_params)}'

    async with httpx.AsyncClient() as client:
        raw_beers = await client.get(f"{os.getenv('PUNK_API_BASE_URL')}/beers{parameters}")
        return [Beer(**beer) for beer in raw_beers.json()]


@beer_router.get('')
async def get_beers_listing(page: int = 1, per_page: int = 10) -> BeerCollection:
    beers = await get_beers_from_punk_api(page, per_page)
    return BeerCollection(items=beers, count=beers.__len__())


@beer_router.get("/{beer_name}")
async def search_beers_by_name(beer_name: Text) -> BeerCollection:
    beers = await get_beers_from_punk_api(-1, -1, beer_name)
    return BeerCollection(items=beers, count=beers.__len__())