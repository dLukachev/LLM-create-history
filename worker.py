from func.generate_story import generate_story_task
from func.continue_story import continue_story_task
from utils.arq import REDIS_SETTINGS

class WorkerSettings:
    functions = [generate_story_task, continue_story_task]
    redis_settings = REDIS_SETTINGS