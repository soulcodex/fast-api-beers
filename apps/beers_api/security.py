import os
from typing import Text
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader, APIKeyQuery

API_KEY_QUERY_NAME = '_token'
query_api_key = APIKeyQuery(name=API_KEY_QUERY_NAME, auto_error=False)


# Api key handler from query param
async def get_api_key(api_key_query: Text = Security(query_api_key)) -> Text:
    if api_key_query == os.getenv('API_KEY'):
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials."
    )
