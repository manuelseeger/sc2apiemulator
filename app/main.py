import json, redis, time, os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
conn = redis.Redis("localhost")

class Player(BaseModel):
    id: int
    enabled: bool
    name: str
    race: str
    result: str

class Data(BaseModel):
    state: str
    menu_state: str
    additional_menu_state: str
    replay: bool
    players: list[Player]
    displaytime: int
    autotime: bool
    set_at: int = int(time.time())

class State(BaseModel):
    players: list
    replay: bool
    inGame: int = 0

def respond(data):
    return JSONResponse(content=data)

def getState():
    state = conn.get("state")
    if not state:
        return {"players": [], "replay": False, "inGame": 0}
    return json.loads(state)

def getData() -> Data:
    data = conn.get("data")
    if not data:
        default_data = Data(
            state="nogame",
            menu_state="ScreenHome/ScreenHome",
            additional_menu_state="None",
            replay=False,
            players=[
                Player(id=1, enabled=True, name="player1", race="Terr", result="Defeat"),
                Player(id=2, enabled=True, name="player2", race="Terr", result="Defeat"),
                Player(id=3, enabled=False, name="player3", race="Terr", result="Defeat"),
                Player(id=4, enabled=False, name="player4", race="Terr", result="Defeat"),
                Player(id=5, enabled=False, name="player5", race="Terr", result="Defeat"),
                Player(id=6, enabled=False, name="player6", race="Terr", result="Defeat"),
                Player(id=7, enabled=False, name="player7", race="Terr", result="Defeat"),
                Player(id=8, enabled=False, name="player8", race="Terr", result="Defeat"),
            ],
            displaytime=0,
            autotime=True,
            set_at=int(time.time())
        )
        return default_data
    return Data.parse_obj(json.loads(data))

def getPlayersFromData(data: Data):
    # Return only enabled players as dictionaries with updated result values
    players = []
    for player in data.players:
        if player.enabled:
            players.append(player.dict())
    return players

@app.get("/hello")
def read_root():
    return {"Hello": "World"}

@app.get("/ui")
def ui():
    data = getData()
    if data.state in ("nogame", "postgame"):
        activeScreens = [
            "ScreenBackgroundSC2/ScreenBackgroundSC2",
            data.menu_state,
            "ScreenNavigationSC2/ScreenNavigationSC2",
            "ScreenForegroundSC2/ScreenForegroundSC2",
        ]
        if data.additional_menu_state != "None":
            activeScreens.append(data.additional_menu_state)
        return respond({"activeScreens": activeScreens})
    if data.state == "loading":
        return respond({"activeScreens": ["ScreenLoading/ScreenLoading"]})
    if data.state == "ingame":
        return respond({"activeScreens": []})
    raise HTTPException(status_code=400, detail="Invalid state")

@app.get("/game")
def game():
    data = getData()
    state = getState()

    if data.autotime:
        displayTime = int(time.time()) - data.set_at
    else:
        displayTime = data.displaytime

    if not state.get("players"):
        state["players"] = getPlayersFromData(data)
        conn.set("state", json.dumps(state))

    if data.state in ("nogame", "postgame"):
        state["inGame"] = 0
        conn.set("state", json.dumps(state))
        return respond({"isReplay": False, "displayTime": displayTime, "players": []})

    state["replay"] = data.replay
    if data.state == "ingame" and state.get("inGame", 0) == 0:
        state["inGame"] = 1
        state["players"] = getPlayersFromData(data)
        conn.set("state", json.dumps(state))

    tmpPlayers = []
    for i, player in enumerate(state["players"]):
        p = player.copy()
        
        if data.state == "ingame" and not data.replay:
            p["result"] = "Undecided"
        p["id"] = i + 1
        tmpPlayers.append(p)

    return respond({"isReplay": state["replay"], "displayTime": displayTime, "players": tmpPlayers})

@app.post("/set")
def set_data(new_data: Data):
    new_data.set_at = int(time.time())
    conn.set("data", new_data.json())
    state = getState()
    state["players"] = getPlayersFromData(new_data)
    conn.set("state", json.dumps(state))
    return respond({"status": "ok"})

app.mount(
    "/", StaticFiles(directory=os.path.join(".", "public"), html=True), name="public"
)
