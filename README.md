# Flask REST API Server
> Client -> Gunicorn -> Flask --CRUD--> MySQL
- Flask를 사용한 간단한 REST API 서버 개발
- ORM은 사용하지 않았으며, SQL 쿼리를 사용해서 데이터베이스에 CRUD 연산을 수행
- 로컬 구동 및 Docker Container 빌드
- 사전에 [mysql](./mysql/) 컨테이너 구동 필요

### Dockerhub
[hyukjun/flask-rest-api](https://hub.docker.com/repository/docker/hyukjun/flask-rest-api/general)

### 개발 환경 및 버전
```markdown
# Language
Python 3.9.18

# Python Package
Flask==2.3.3
mysql-connector-python==8.3.0
gunicorn==21.2.0
```

### 로컬 개발 세팅
```bash
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

### 앞으로 해야할 일
- kubernetes 환경에 맞게 구성
- docker-compose 구성
- CICD 붙히기
