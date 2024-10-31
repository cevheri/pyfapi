# async def query_params(q: str | None = None, page: int = 0, limit: int = 10, sort: str = "+_id") -> dict:
#     """
#     Query parameters for list and filter operations.
#
#     Parameters:
#     -----------
#     q: str
#         Query string to filter the results.
#     page: int
#         Offset for the page.
#     limit: int
#         Limit for the page.
#     sort: str
#         Sort order for the results. Default is descending order.
#
#     Returns:
#     --------
#     dict:
#         Query parameters.
#     """
#     return {
#         "q": q,
#         "page": page,
#         "size": limit,
#         "sort": sort
#     }
import json
from typing import Dict, Any

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class QueryParams(BaseModel):
    """
    Query parameters for list and filter operations.

    Examples:
    ---------
    - q: {"username":"john_doe1"}
    - q: {"age": {"$gte": 25}}
    - q: {"$or": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - q: {"$and": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - q: {"$nor": [{"username": "john_doe1"}, {"age": {"$gte": 25}}]}
    - q: {"username": {"$in": ["john_doe1", "john_doe2"]}}
    - q: {"username": {"$nin": ["john_doe1", "john_doe2"]}}

    Parameters:
    -----------
    q: str
        Query string to filter the results.

    page: int
        Offset for the page.

    limit: int
        Limit for the page.

    sort: str
        Sort order for the results. Default is descending order.

    Returns:
    --------
    dict:
        Query parameters.
    """

    q: str | None = Field(default=None, title="Query string to filter the results", min_length=3, max_length=1000,
                          alias="q")
    offset: int = Field(default=0, title="Offset for the page", description="Offset for the page", examples=[0],
                        ge=0, alias="page")
    limit: int = 10
    sort: str = "+_id"

    class Config:
        json_schema_extra = {
            "example": {
                "q": '{"username":"john_doe1"}',
                "page": 0,
                "limit": 10,
                "sort": "+_id"
            }
        }

    # mongodb query string validation - q does not allow data manipulation
    @field_validator("q")
    @classmethod
    def validate_query(cls, q: str):
        """
        Validate the query string to prevent data manipulation.
        :param q: query string
        """
        if not q:
            return

        allowed_operators = {"$eq", "$gt", "$gte", "$in", "$lt", "$lte", "$ne", "$nin", "$or", "$and", "$nor"}
        obj = json.loads(q)

        def check_allowed_keys(query: Dict[str, Any]):
            for k, v in query.items():
                if k.startswith("$") and k not in allowed_operators:
                    raise HTTPException(status_code=400, detail=f"Unauthorized query operator: {k}")
                if isinstance(v, dict):
                    check_allowed_keys(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            check_allowed_keys(item)

        check_allowed_keys(obj)
        return q
