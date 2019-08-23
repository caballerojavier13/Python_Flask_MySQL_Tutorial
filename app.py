from flask import Flask, abort, jsonify, make_response, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'pyladies'

mysql = MySQL(app)


@app.route('/people', methods=['GET'])
def get_all_people():
    users = []
    mysql.get_db().autocommit(True)

    cursor = mysql.get_db().cursor()
    cursor.execute('Select * FROM people')
    query_users = cursor.fetchall()

    for u in query_users:
        users.append({
            'id': u[0],
            'name': u[1]
        })

    cursor.close()

    return jsonify({
        'users': users
    }), 200


@app.route('/people', methods=['POST'])
def create_person():
    body = request.json

    mysql.get_db().autocommit(True)

    cursor = mysql.get_db().cursor()

    cursor.execute("INSERT INTO people (people_mame) VALUES ('%s');" % body['name'])
    cursor.execute('Select * FROM people ORDER BY people_id DESC')
    new_row = cursor.fetchone()

    cursor.close()

    return jsonify({
        'user': {
            'id': new_row[0],
            'name': new_row[1]
        }
    }), 201


app.run(debug=True)
