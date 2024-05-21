# Flask REST API Server with MySQL
> Client -> Gunicorn -> Flask --CRUD--> MySQL

## Overview
```markdown
# Description
- Flask를 사용한 간단한 REST API 데모 서버
- SQL 쿼리를 사용한 CRUD 작업

# Language
Python 3.9.18

# Python Package
Flask==2.3.3
mysql-connector-python==8.3.0
gunicorn==21.2.0

# Database
MySQL 8.2.0
```

## Dockerhub
- [hyukjun/flask-rest-api-amd64](https://hub.docker.com/repository/docker/hyukjun/flask-rest-api-amd64/general)

- [hyukjun/mysql-8.2.0-init-scheme-amd64](https://hub.docker.com/repository/docker/hyukjun/mysql-8.2.0-init-scheme-amd64/general)


## Usage (Kubernetes)
[README](k8s/README.md)

## Usage (Docker Container)
1. Install Docker Engine
    ```markdown
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```
    ```markdown
    # Add the repository to Apt sources:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```
    ```markdown
    # Install Docker Tools
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
    ```markdown
    # Manage Docker as a non-root user
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```
    - [Docker Engine - Install in Ubuntus OS](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
    - [Docker Engine - Post Installation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

2. Start MySQL Server

    ```markdown
    # Setup ENV
    export DBNAME=<DBNAME>
    export DBUSER=<USERNAME>
    export DBPASS=<USERPASSWORD>
    export DBROOTPASS=<ROOTPASSWORD>

    # Run MySQL Container
    docker run -d -p 3306:3306 \
    --env MYSQL_DATABASE=$DBNAME \
    --env MYSQL_ROOT_PASSWORD=$DBROOTPASS \
    --env MYSQL_USER=$DBUSER \
    --env MYSQL_PASSWORD=$DBPASS \
    hyukjun/mysql-8.2.0-init-scheme-amd64:1.0
    ```
3. Start Flask API Server

    ```markdown
    # Get MySQL Container IP Address
    export DBHOST=$(docker inspect <CONTAINERID> | grep -wi IPAddress | awk '{gsub("\"",""); gsub(",",""); print $2}' | head -n 1)

    # Run Flask API Server
    docker run -d -p 8000:8000 \
    --env MYSQL_DATABASE_HOST=$DBHOST \
    --env MYSQL_DATABASE_DB=$DBNAME \
    --env MYSQL_DATABASE_USER=$DBUSER \
    --env MYSQL_DATABASE_PASSWORD=$DBPASS \
    hyukjun/flask-rest-api-amd64:1.0

    # Call API Server
    curl localhost:8000/api/player
    ```

## Usage (Local)
```bash
# Run MySQL Container
# Setup ENV
export DBNAME=<DBNAME>
export DBUSER=<USERNAME>
export DBPASS=<USERPASSWORD>
export DBROOTPASS=<ROOTPASSWORD>

# Run MySQL Container
docker run -d -p 3306:3306 \
--env MYSQL_DATABASE=$DBNAME \
--env MYSQL_ROOT_PASSWORD=$DBROOTPASS \
--env MYSQL_USER=$DBUSER \
--env MYSQL_PASSWORD=$DBPASS \
hyukjun/mysql-8.2.0-init-scheme-amd64:1.0

# python 3.9 설치
brew install python@3.9

# 가상 환경 세팅 (python 3.9)
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# 로컬 구동시 사전에 환경변수 주입 필요
export MYSQL_DATABASE_HOST=
export MYSQL_DATABASE_DB=
export MYSQL_DATABASE_USER=
export MYSQL_DATABASE_PASSWORD=

# 로컬 구동
python main.py # 디버그 모드
gunicorn -c gunicorn_config.py main:app # 운영 모드
```

## 참고사항
### Docker 참고사항
```bash
# 빌드 및 실행
docker build -t IMAGE:TAG .

docker run -d -p 8000:8000 \
--env MYSQL_DATABASE_HOST=MYSQL_SERVER_ADDRESS \
--env MYSQL_DATABASE_DB=MYSQL_DB_NAME \
--env MYSQL_DATABASE_USER=MYSQL_USER_NAME \
--env MYSQL_DATABASE_PASSWORD=MYSQL_USER_PASSWD \
IMAGE:TAG

# linux/amd64 아키텍쳐로 빌드
docker build --platform linux/amd64 -t IMAGE:TAG
```

### Flask 참고사항

> OS의 세팅된 환경변수 읽어오기
```bash
import os
print(os.environ['HOME'])

# Returns `None` if the key doesn't exist
print(os.environ.get('KEY_THAT_MIGHT_EXIST'))

# Returns `default_value` if the key doesn't exist
print(os.environ.get('KEY_THAT_MIGHT_EXIST', default_value))

# Returns `default_value` if the key doesn't exist
print(os.getenv('KEY_THAT_MIGHT_EXIST', default_value))
```
> Flask의 request 메소드로 데이터 읽어오기
```bash
# query parameter
request.args.get('parameter')

# data from raw data
request.get_data()

# data from form data
request.form.get('value')
```

> gunicorn 구동 방법
```bash
# start server
gunicorn --config gunicorn_config.py MODULE:INSTANCE
```

### Python Package 참고사항
- [gunicorn 21.2.0](https://pypi.org/project/gunicorn/)

- [flask 2.3.3](https://flask.palletsprojects.com/en/2.3.x/)

- [mysql connector python 8.3.0](https://dev.mysql.com/doc/connector-python/en/)

- [*excute 사용시 변수 지정 방법 - 리스트, 튜플, 딕셔너리 방법 존재](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html)
