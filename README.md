SC2 Api Emulator
================

SC2 client api emulator for testing purposes.

Originally developed by Oliver Leigh https://github.com/leigholiver/sc2apiemulator

Run with Docker
```
docker pull manuelseeger/sc2apiemulator
docker run -d --rm -p6119:6119 --name sc2apiemulator manuelseeger/sc2apiemulator
```

Visit http://localhost:6119/ to configure the API simulator responses.

You can then use the http://localhost:6119/ui and http://localhost:6119/game endpoints as if it were the SC2 API.

Note: 6119 is the port SC2 uses. Use a different port if you want to run the simulator while SC2 is running as well. 


## Develop

Run redis and install the fastapi standard tools to run / develop locally:
```
redis-server
pip install -r requirements.txt
pip install fastapi[standard]
cd app
PORT=6119 fastapi run
```

## Background

The SC2 game client comes with an API which serves the state of the game client. It gives information such as which menu selection is currently shown or whether there is a game or replay running. The original announcement from Blizzard is lost with the old Battle.net forums, but can be found in this archive: 
https://web.archive.org/web/20160818015235/https://us.battle.net/forums/en/sc2/topic/20748195420

The API does not disclose any information about the live game other than the matchup and game timer. It is meant to automate streamer profiles with tools like OBS.

----

## Original Readme

Run:
`docker pull leigholiver/sc2api`
`docker run -d --rm -p6120:80 --name sc2api leigholiver/sc2api`

Point your browser at `http://localhost:6120/` to configure the API responses 

You can then use the `http://localhost:6120/ui` and `http://localhost:6120/game` endpoints as if it were the SC2 API