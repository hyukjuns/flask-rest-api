### tasks
1. Docker 환경을 위한 개발
2. Kubernetes 환경을 위한 개발
3. 개발/운영 환경별 세팅
4. ORM은 사용하지 않는다.

# Flask REST API Server
Client -> Gunicorn -> Flask --CRUD--> MySQL

### 개발 환경 및 버전
```
Python 3.9.18
Flask==2.3.3
mysql-connector-python==8.3.0
gunicorn==21.2.0
```

### Local Setup
```
# python 3.9 설치
brew install python@3.9
➜ python3.9 --version
Python 3.9.18

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
gunicorn -c gunicorn_config.py main:app

로컬 구동시 환경변수 주입
export MYSQL_DATABASE_HOST=
export MYSQL_DATABASE_DB=
export MYSQL_DATABASE_USER=
export MYSQL_DATABASE_PASSWORD=

```

### Docker 참고사항
```
# Build for local(m1 mac) and Run
docker build -t IMAGE:TAG
docker run -d -p 8000:8000 \
--env MYSQL_DATABASE_HOST= \
--env MYSQL_DATABASE_DB= \
--env MYSQL_DATABASE_USER= \
--env MYSQL_DATABASE_PASSWORD= \
apitest:0.1

# Build for Production (AKS)
docker build --platform linux/amd64 -t REGISTRY/IMAGE:TAG

# Push Container Registry
docker login REGISTRY
docker push REGISTRY/IMAGE:TAG
```

### Flask 참고사항
- get env from os
```
import os
print(os.environ['HOME'])

# Returns `None` if the key doesn't exist
print(os.environ.get('KEY_THAT_MIGHT_EXIST'))

# Returns `default_value` if the key doesn't exist
print(os.environ.get('KEY_THAT_MIGHT_EXIST', default_value))

# Returns `default_value` if the key doesn't exist
print(os.getenv('KEY_THAT_MIGHT_EXIST', default_value))
```

- flask request
```
# query parameter
request.args.get('parameter')

# data from raw data
request.get_data()

# data from form data
request.form.get('value')
```

- gunicron up
```
# start server
gunicorn --config gunicorn_config.py MODULE:INSTANCE
```

### Package 참고
gunicorn 21.2.0
https://pypi.org/project/gunicorn/

flask 2.3.3
https://flask.palletsprojects.com/en/2.3.x/

mysql connector python 8.3.0
https://dev.mysql.com/doc/connector-python/en/
*excute 사용시 변수 지정 방법 - 리스트, 튜플, 딕셔너리 방법 존재
https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html