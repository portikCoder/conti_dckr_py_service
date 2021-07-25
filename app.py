import logging
import sqlite3
from contextlib import contextmanager
from http import HTTPStatus
from pprint import pprint
from typing import Any
from flask import Flask, request, Response
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app=app,
          version="1.0",
          title="Name Recorder",
          description="Manage names of various users of the application")

name_space = api.namespace('names', description='Manage names')

db_conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
db_conn.execute('CREATE TABLE anytype (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'anytype BLOB not null, '
                'datatype BOOL not null DEFAULT False)')

# pprint(db_conn.execute('PRAGMA table_info([anytype])').description)
db_conn.execute("INSERT INTO anytype VALUES (NULL, 'ham', 'str')")
# pprint(list(db_conn.execute('SELECT * FROM anytype')))
db_conn.commit()


# for making my life just a bit easier, but for sure, we have such a huge armada of db ORM frameworks, so therefore I would
#   really not re-implement the wheel with this shitty solution in prod, nor for my hobby projects
#   implementing a raw DB handler was just as bad when i realize everything is in 1 file (funfact: just like here :D)
#   but at least i was able to live again the feeling of the low level stuffs
# the flask collaborator which i prefer is SQLAlchemy, and somewhat is interchangeable with the famous Django's one
@contextmanager
def get_db_connection():
    db_conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    try:
        yield db_conn
        db_conn.commit()
    finally:
        db_conn.close()


# this is a view, so should be inside the views.py
class AnyTypeHandler(Resource):
    def post(self):
        input: Any = request.get_data()
        if not input:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        is_input_type_int = True
        try:
            int(input)
        except:
            is_input_type_int = False

        logging.debug(f'input for "{self.post}" is "{input}"')
        # TODO> SQL100: Possible SQL injection within String format. Found in 'f'INSERT INTO anytype VALUES (NULL, "{input}")''.
        with get_db_connection() as db_conn:
            pprint(list(db_conn.execute('SELECT * FROM anytype')))
            id = db_conn.execute('INSERT INTO anytype VALUES (?,?,?);', (None, input, is_input_type_int)).lastrowid

        logging.debug(f'POST result is: {id}')
        return Response(str(id), status=HTTPStatus.OK, mimetype='application/json')

    def get(self):
        input: Any = request.get_data()
        # in this case rather to make a `counter` column, as it would fasten up the things | but this way is easier to implement
        if not input:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        with get_db_connection() as db_conn:
            result = db_conn.execute('SELECT COUNT(anytype) FROM anytype WHERE anytype==?', (input,)).fetchone()[0]
        logging.debug(f'GET result is: {result}')
        return Response(str(result), status=HTTPStatus.OK, mimetype='application/json')


api.add_resource(AnyTypeHandler, "/", )


# mixing ways of routing is not a wise step, just in some really special cases
# @app.route('/avg', methods=['GET'])
def avg(dummy_self_var=''):
    # the dummy_self_var is needed in order to trick and pretend to be as an instance method
    with get_db_connection() as db_conn:
        result = db_conn.execute('SELECT AVG(anytype) FROM anytype WHERE datatype==True').fetchone()[0]
    result = result if result else 0
    logging.debug(f'AVG result is: {result}')

    return Response(str(result))


# imitating that this function is a Resource :D
avg.view_class = Resource
avg.as_view = lambda x, y: avg

avg.view_class.methods = {'GET', }
avg.view_class.get = avg

api.add_resource(avg, '/asd')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    # i know, we all know, should use a WSGI server instead this dumb run
    app.run(debug=True, host='0.0.0.0')
    # app.run(host='0.0.0.0')
