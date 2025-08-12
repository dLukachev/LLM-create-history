from fastapi import APIRouter, Request

from func.openrouter_service import OpenRouterService
from database.schema import StoryCreateRequest

start_story = APIRouter()

ors = OpenRouterService()

@start_story.post("/create_story")
async def create_story(request: StoryCreateRequest):
    promt = request.promt
    role = request.role

    if promt is None or role is None:
        return {"data": "Failed. Promt or role missing."}

    result = await ors.call(promt, role)

    return {"data": result}

@start_story.get("/clear_history")
def clear_history():
    result = ors.clear_history()
    return result