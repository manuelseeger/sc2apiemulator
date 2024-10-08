SC2 Api Emulator
================

SC2 client api emulator for testing purposes.

Run locally
```
pip install -r requirements.txt
cd app
fastapi run
```
or with Docker
```
docker pull manuelseeger/sc2apiemulator
docker run -d --rm -p6119:6119 --name sc2apiemulator manuelseeger/sc2apiemulator
```

Visit http://localhost:6119/ to configure the API simulator responses. 

Note: 6119 is the port SC2 uses. Use a different port if you want to run the simulator while SC2 is running as well. 

----

## Original Readme

Run:
`docker pull leigholiver/sc2api`
`docker run -d --rm -p6120:80 --name sc2api leigholiver/sc2api`

Point your browser at `http://localhost:6120/` to configure the API responses 

You can then use the `http://localhost:6120/ui` and `http://localhost:6120/game` endpoints as if it were the SC2 API