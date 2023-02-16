# QuickFIX examples for python developers

## Installing Requirements
```
pip install -r requirements.txt
```

## Run Project

### With Docker
```sh
cd ./docker
docker-compose up --build
```

### Without Docker
Please modify file path in `initiator/client.cfg` from `SocketConnectHost=acceptor` to `SocketConnectHost=127.0.0.1`

```sh
cd ./acceptor
python server.py server.cfg
```

```sh
cd ./initiator
python client.py client.cfg
```
