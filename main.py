import os, json
import logging
from flask import Flask, request, jsonify
import mysql.connector

# Flask 인스턴스 생성
app = Flask(__name__)

# 데이터베이스 연결정보 세팅
MYSQL_DATABASE_USER = os.environ.get('MYSQL_DATABASE_USER')
MYSQL_DATABASE_PASSWORD = os.environ.get('MYSQL_DATABASE_PASSWORD')
MYSQL_DATABASE_DB = os.environ.get('MYSQL_DATABASE_DB')
MYSQL_DATABASE_HOST = os.environ.get('MYSQL_DATABASE_HOST')

# 데이터베이스의 테이블 이름
TABLE_NAME="player"

def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_DATABASE_HOST,
        database=MYSQL_DATABASE_DB,
        user=MYSQL_DATABASE_USER,
        password=MYSQL_DATABASE_PASSWORD
    )
    cursor = connection.cursor()
    return connection, cursor

# GET
@app.route("/api/player", methods=['GET'])
def get_player():
    try:
        connection, cursor = get_db_connection()
    except Exception as e:
        print(e)
        return "Failed to get DB Connection."
    try:
        select_query = f"""
            SELECT
                JSON_OBJECT (
                    'id', id,
                    'created', created,
                    'name', name,
                    'team', team,
                    'goal', goal
                )
            FROM {TABLE_NAME}
        """
        cursor.execute(select_query)
        data = cursor.fetchall()
        connection.close()
        return jsonify(data), 200
    except Exception as e:
         print(e)
         return "Fail to get player's info.", 400

@app.route("/api/player", methods=['POST'])
def create_player():
        try:
            connection, cursor = get_db_connection()
        except Exception as e:
            print(e)
            return "Get DB Connection Failed."
        try:
            body = request.get_data()
            data = json.loads(body)
            player_name = data['name']
            player_team = data['team']
            player_goal = data['goal']

            select_query = f"""
                SELECT name FROM {TABLE_NAME} 
                WHERE name = %s
                """
            # Check target exist, 변수는 리스트형으로 (혹은 튜플,딕셔너리)
            cursor.execute(select_query, [player_name])            
            result = cursor.fetchone()
            if result is not None:
                connection.close()
                return "Player already exist.", 400
            else:
                insert_query = f"""
                    INSERT INTO {TABLE_NAME}
                    (name, team, goal)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, [player_name, player_team, player_goal])
                connection.commit()
                connection.close()
                return "Completed to create player.", 201
        except Exception as e:
            print(e)
            return "bad request", 400

# PUT
@app.route("/api/player/<int:id>", methods=['PUT'])
def update_player(id):
    try:
        connection, cursor = get_db_connection()
    except Exception as e:
        print(e)
        return "Get DB Connection Failed."
    try:
        # Get Data
        body = request.get_data()
        data = json.loads(body)
        player_name = data['name']
        player_team = data['team']
        player_goal = data['goal']

        # Check target exist
        select_query = f"""
            SELECT id FROM {TABLE_NAME} 
            WHERE id=%s
        """
        cursor.execute(select_query, [id]
        )
        result = cursor.fetchone()

        if result is None:
            connection.close()
            return "Player don't exist.", 400
        else:
            update_query = f"""
                UPDATE player
                SET name=%(name)s, team=%(team)s, goal=%(goal)s
                WHERE id=%(id)s
            """
            cursor.execute(update_query, 
                           {
                            'name': player_name,
                            'team': player_team,
                            'goal': player_goal,
                            'id': id
                            }
                           )
            connection.commit()
            connection.close()
            return "Updated Player.", 200
    except Exception as e:
        print(e)
        return "bad request", 400

# DELETE
@app.route("/api/player/<int:id>", methods=['DELETE'])
def delete_player(id):
    try:
        connection, cursor = get_db_connection()
    except Exception as e:
        print(e)
        return "Get DB Connection Failed."
    try:

        # Check target exist
        select_query = f"""
            SELECT id FROM {TABLE_NAME}
            WHERE id=%s
        """
        cursor.execute(select_query, [id])
        result = cursor.fetchone()

        if result is None:
            connection.close()
            return "Player don't exist.", 400
        else:
            delete_query = f"""
                DELETE FROM {TABLE_NAME}
                WHERE id=%s
            """
            cursor.execute(delete_query, [id])
            connection.commit()
            connection.close()
            return "Deleted Player.", 200
    except Exception as e:
        print(e)
        return "bad request", 400

# Health Check 
@app.route('/healthz', methods=['GET'])
def healthz():
    return {"health": "ok"}, 200 # 200 Ok

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)