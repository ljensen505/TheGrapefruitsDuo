from asyncio import gather

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import MainController
from app.models.tgd import TheGrapefruitsDuo
from app.routers.contact import router as contact_router
from app.routers.events import router as event_router
from app.routers.group import router as group_router
from app.routers.musicians import router as musician_router
from app.scripts.version import get_version

app = FastAPI(
    title="The Grapefruits Duo API",
    description="API for The Grapefruits Duo website",
    version=get_version(),
)
app.include_router(musician_router)
app.include_router(group_router)
app.include_router(contact_router)
app.include_router(event_router)

controller = MainController()

origins = [
    "http://localhost:3000",
    "https://thegrapefruitsduo.com",
    "https://www.thegrapefruitsduo.com",
    "https://tgd.lucasjensen.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def root() -> TheGrapefruitsDuo:
    musicians, events, group = await gather(
        controller.get_musicians(),
        controller.get_events(),
        controller.get_group(),
    )
    return TheGrapefruitsDuo(
        version=get_version(),
        group=group,
        musicians=musicians,
        events=events,
    )
