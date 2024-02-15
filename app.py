import os, json
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST')
mysql = MySQL()
mysql.init_app(app)

# GET, POST
@app.route("/api/player", methods=['GET', 'POST'])
def create_or_get_player():
    if request.method == 'GET':
        # Get DB and Fetch data
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                JSON_OBJECT(
                    'id', id,
                    'created', created,
                    'name', name,
                    'team', team,
                    'goal', goal
                    )
            FROM player
        """)
        data = cursor.fetchall()
        conn.close()
        return jsonify(data), 200
    elif request.method == 'POST':
        try:
            # Get Data
            data = request.get_data()
            data = json.loads(data)
            new_name = data['name']
            new_team = data['team']
            new_goal = data['goal']

            # Get DB Connection
            conn = mysql.connect()
            cursor = conn.cursor()

            # Check target exist
            cursor.execute(f"""
                SELECT name FROM player WHERE name=%s
            """, (new_name)
            )
            result = cursor.fetchone()
            if result is not None:
                conn.close()
                return "Player already exist !!!", 400
            else:
                cursor.execute(f"""
                    INSERT INTO player
                    (name, team, goal)
                    VALUES (%s, %s, %s)
                """, ({new_name}, {new_team}, {new_goal}))
                conn.commit()
                conn.close()
                return "Created plater !!!", 200
        except Exception as e:
            print(e)
            return "bad request", 400
    else:
        return "bad request", 400

# PUT
@app.route("/api/player", methods=['PUT'])
def update_player():
    try:
        # Get Data
        data = request.get_data()
        data = json.loads(data)
        name = data['name']
        team = data['team']
        goal = data['goal']

        # Get DB Connection
        conn = mysql.connect()
        cursor = conn.cursor()

        # Check target exist
        cursor.execute(f"""
            SELECT name FROM player WHERE name=%s
        """, (name)
        )
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return "Player don't exist !!!", 400
        else:
            cursor.execute(f"""
                UPDATE player
                SET team=%s, goal=%s
                WHERE name=%s
            """, ({team},{goal},{name}))
            conn.commit()
            conn.close()
            return "Updated Player !!!", 200
    except Exception as e:
        print(e)
        return "bad request", 400

# DELETE
@app.route("/api/player/delete", methods=['DELETE'])
def delete_player():
    try:
        # Get Data
        target_name = request.args.get('name')

        # Get DB Connection
        conn = mysql.connect()
        cursor = conn.cursor()

        # Check target exist
        cursor.execute(f"""
            SELECT name FROM player WHERE name=%s
        """, (target_name)
        )
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return "Player don't exist !!!", 400
        else:
            cursor.execute(f"""
                DELETE FROM player WHERE name=%s
            """, (target_name)
            )
            conn.commit()
            conn.close()
            return "Deleted Player !!!", 200
    except Exception as e:
        print(e)
        return "bad request", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)