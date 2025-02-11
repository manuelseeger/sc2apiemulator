from typing import Optional
import redis, time, os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from enum import Enum

app = FastAPI()
conn = redis.Redis("localhost")

class Screen(str, Enum):
    loading = "ScreenLoading/ScreenLoading"
    score = "ScreenScore/ScreenScore"
    home = "ScreenHome/ScreenHome"
    background = "ScreenBackgroundSC2/ScreenBackgroundSC2"
    foreground = "ScreenForegroundSC2/ScreenForegroundSC2"
    navigation = "ScreenNavigationSC2/ScreenNavigationSC2"
    userprofile = "ScreenUserProfile/ScreenUserProfile"
    multiplayer = "ScreenMultiplayer/ScreenMultiplayer"
    single = "ScreenSingle/ScreenSingle"
    collection = "ScreenCollection/ScreenCollection"
    coopcampaign = "ScreenCoopCampaign/ScreenCoopCampaign"
    custom = "ScreenCustom/ScreenCustom"
    replay = "ScreenReplay/ScreenReplay"
    battlelobby = "ScreenBattleLobby/ScreenBattleLobby"

class State(str, Enum):
    nogame = "nogame"
    ingame = "ingame"
    loading = "loading"
    postgame = "postgame"

class Race(str, Enum):
    terran = "Terr"
    protoss = "Prot"
    zerg = "Zerg"
    random = "random"

class Result(str, Enum):
    win = "Victory"
    loss = "Defeat"
    undecided = "Undecided"
    tie = "Tie"

class Player(BaseModel):
    id: int
    name: str
    type: str = "user"
    race: Race
    result: Result

class GameInfo(BaseModel):
    isReplay: bool
    displayTime: int
    players: list[Player]

class UIInfo(BaseModel):
    activeScreens: set[Screen]

class Data(BaseModel):
    state: State = State.nogame
    menu_state: str = Screen.home.value
    additional_menu_state: Optional[str] = None
    replay: bool = False
    players: list[Player] = []
    displaytime: int = 0
    autotime: bool = True
    set_at: int = int(time.time())

def getData() -> Data:
    data = conn.get("data")
    if not data:
        return Data()
    return Data.model_validate_json(data)

@app.get("/ui")
def ui() -> UIInfo:
    data = getData()
    
        
    if data.state == "loading":
        return UIInfo(activeScreens=[Screen.loading])
    if data.state == "ingame":
        return UIInfo(activeScreens=[])
    
    activeScreens = [
        Screen.background.value,
        data.menu_state,
        Screen.navigation.value,
        Screen.foreground.value,
    ]
    if data.additional_menu_state is not None:
        activeScreens.append(data.additional_menu_state)

    return UIInfo(activeScreens=activeScreens)
    

@app.get("/game")
def game() -> GameInfo:
    data = getData()
    if data.autotime:
        displayTime = int(time.time()) - data.set_at
    else:
        displayTime = data.displaytime

    if data.state != "ingame":
        return GameInfo(isReplay=False, displayTime=0, players=[])

    for i, player in enumerate(data.players):
        if not data.replay:
            player.result = Result.undecided.value
        player.id = i + 1

    return GameInfo(isReplay=data.replay, displayTime=displayTime, players=data.players)

@app.post("/set")
def set_data(new_data: Data):
    new_data.set_at = int(time.time())
    conn.set("data", new_data.model_dump_json())
    return {"status": "ok"}

class DisableCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if isinstance(response, Response):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

app.add_middleware(DisableCacheMiddleware)

app.mount(
    "/", StaticFiles(directory=os.path.join(".", "public"), html=True), name="public"
)
