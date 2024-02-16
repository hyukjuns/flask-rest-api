### Database Inited MySQL
데이터베이스 스키마를 사용해서 데이터베이스를 셋업한 MySQL 도커 이미지 생성 

### Usage
```
# 이미지 빌드
docker build -t <IMAGE>:<TAG> .

# 이미지 실행
docker run -d -p 3306:3306 \
--env MYSQL_DATABASE=<DATABASE_NAME> \
--env MYSQL_ROOT_PASSWORD=<ROOT_PASSWORD> \
--env MYSQL_USER=<DATABASE_USER_NAME> \
--env MYSQL_PASSWORD=<DATABASE_USER_PASSWORD> \
<IMAGE>:<TAG>
```

### 참고내용

- 데이터베이스 초기 셋업 방법
    
    MySQL 도커 이미지에 이미 준비된 DB 초기화를 위한 Entrypoint 경로에 .sql 파일을 옮겨 놓음 `ADD scheme.sql /docker-entrypoint-initdb.d`
- scheme.sql 에 대한 설명

    빌드된 MySQL 이미지 실행시 `MYSQL_DATABASE` 환경변수에 의해 생겨난 초기 데이터베이스를 셋업 하기 위한 SQL 쿼리 스크립트 로서 해당 데이터베이스 내에 `player` 테이블과 그안에 데모 데이터를 `Insert` 함

- MySQL 환경변수 용도와 주입시기 설명

    모든 환경변수는 이미지 빌드 시 주입하지 않고, 실행시에 유동적으로 변경해서 사용하도록 함. 즉, 도커 실행시 flag로 환경변수 주입 방식 채택
    - `MYSQL_DATABASE` -> 초기 데이터베이스 생성
    - `MYSQL_ROOT_PASSWORD` -> 루트 패스워드 (필수)
    - `MYSQL_USER` -> App 에서 사용할 데이터베이스 유저
    - `MYSQL_PASSWORD` -> App 에서 사용할 데이터베이스 유저의 패스워드

### SQL 쿼리 참고
```
# SELECT
SELECT * FROM table;

# INSERT
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);

# ALTER
ALTER TABLE tablename MODIFY columnname INTEGER;

# DELETE
DELETE FROM table WHERE key = value;

# UPDATE
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```