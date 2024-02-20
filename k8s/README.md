### 환경변수
pod 구동 시 secret으로 주입
- mysql
k create secret generic mysql-context --from-env-file=mysql.env -n api

- api 서버