# Python api server

Client -> Gunicorn -> Flask --CRUD--> MySQL

### Prerequisite - MySQL
- MySQL 8.2.0
- Setup
    1. 데이터베이스 셋업
        - 환경변수 주입
        - 스키마 초기화
    2. 이미지 빌드 후 실행
        - ```docker run -d -p 3306:3306 IMAGE```

### Required Environment Variable
- 데이터베이스 Profile 정보
    ```
    MYSQL_DATABASE_USER
    MYSQL_DATABASE_PASSWORD
    MYSQL_DATABASE_DB
    MYSQL_DATABASE_HOST
    ```
### Dockerfile - Production
- Setup
    1. Dockerfile에 DB를 위한 환경변수 세팅
    2. 이미지 빌드 후 실행
        - ```docker build -t REPO/NAME:TAG . ```
        - ```docker run -d -p HOST:CONTAINER IMAGE```

### Docker-Compose - Dev
- Setup
    1. Compose 파일에 DB를 위한 환경변수 세팅
    2. 이미지 빌드 후 실행
        - ```docker compose up -d --build```

### Local - Dev
- Setup
    1. Application을 실행할 Shell에 DB를 위한 환경변수 세팅 (export)
    2. Shell에서 실행
        - ```python app.py```

### Flask
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
gunicorn --config gunicorn_config.py app:app
```