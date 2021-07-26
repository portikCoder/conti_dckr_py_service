import logging
import sqlite3
import typing
from contextlib import contextmanager
from http import HTTPStatus
from pprint import pprint
from typing import Any

from flask import Flask, request, Response
from flask_restx import Api, Resource, fields

from continental_docker_python_service_solution import init

# init - only logger
init()

app = Flask(__name__)
api = Api(app=app,
          version="1.0",
          title="Dockerized Flask API",
          description="Dockerized API solution dedicated for the Conti",
          prefix='/api',
          doc='/swagger-ui')

name_space = api.namespace('', description='All the endpoints here')
api.add_namespace(name_space)

# DB setup
db_conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
db_conn.execute('CREATE TABLE anytype (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'anytype BLOB not null, '
                'datatype TEXT)')

# pprint(db_conn.execute('PRAGMA table_info([anytype])').description)
db_conn.execute("INSERT INTO anytype VALUES (NULL, 'ham', 'str')")
# pprint(list(db_conn.execute('SELECT * FROM anytype')))
db_conn.commit()


# for making my life just a bit easier, but for sure, we have such a huge armada of db ORM frameworks, so therefore I would
#   really not re-implement the wheel with this shitty solution in prod, nor for my hobby projects
#   implementing a raw DB handler was just as bad when i realize everything is in 1 file (funfact: just like here :D)
#   but at least i was able to live again the feeling of the low level stuffs
# the flask db collaborator which i prefer is SQLAlchemy, and somewhat is interchangeable with the famous Django's default one
@contextmanager
def get_db_connection():
    db_conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    try:
        yield db_conn
        db_conn.commit()
    finally:
        db_conn.close()


# this is a utility, so should be inside the util.py
def get_specific_number_typename_of(input_: bytes) -> typing.Union[None, str]:
    def try_to_convert(val: bytes, to_type: type):
        try:
            logging.debug(f'Val is: {val}. Type is: {to_type}')
            if str(to_type(val)) == val.decode('utf-8'):
                return to_type.__name__
        except:
            return None
        return None

    return try_to_convert(input_, float) or try_to_convert(input_, int) or try_to_convert(input_, complex)


# this is a view, so should be inside the views.py
@name_space.route('/', methods=['GET', 'POST'])
@name_space.expect(
    name_space.model('rawinput', {'Anything, literally...': fields.String(description='json, or any other value',
                                                                          example="Json, Raw input - like: 1, 1.0, [1,2,3], "
                                                                                  "'stringy', b'some fancy binary'",
                                                                          required=True)}))
class AnyTypeHandler(Resource):
    @name_space.response(HTTPStatus.CREATED, 'The id of the element just created')
    def post(self):
        input_: Any = request.get_data()
        if not input_:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        numeric_input_type = str(get_specific_number_typename_of(input_))

        logging.debug(f'input for "{self.post}" is "{input}"')
        # TODO> SQL100: Possible SQL injection within String format. Found in 'f'INSERT INTO anytype VALUES (NULL, "{input}")''.
        with get_db_connection() as db_conn:
            pprint(list(db_conn.execute('SELECT * FROM anytype')))
            id_ = db_conn.execute('INSERT INTO anytype VALUES (?,?,?);', (None, input_, numeric_input_type)).lastrowid

        logging.debug(f'POST result is: {id_}')
        return Response(str(id_), status=HTTPStatus.CREATED, mimetype='application/json')

    @name_space.response(HTTPStatus.CREATED, 'Counts how many times a given input was posted before')
    def get(self):
        input_: Any = request.get_data()
        # in this case rather to make a `counter` column, as it would fasten up the things | but this way is easier to implement
        if not input_:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        with get_db_connection() as db_conn:
            result = db_conn.execute('SELECT COUNT(anytype) FROM anytype WHERE anytype==?', (input_,)).fetchone()[0]
        logging.debug(f'GET result is: {result}')
        return Response(str(result), status=HTTPStatus.OK, mimetype='application/json')


@name_space.route('/avg/<dtype>', methods=['GET'])
@name_space.param('dtype', 'The type of the input you wanna get the average value for '
                           '(there is no check if the input is type of a number)', example='int, float, ...')
@name_space.response(HTTPStatus.OK,
                     'Average value for a given specific number type. If there is no such type, or is not a number, returns 0')
class Avg(Resource):
    def get(self, dtype: str):
        logging.debug(f'Avg input requested of type: {dtype}')
        with get_db_connection() as db_conn:
            result = db_conn.execute('SELECT AVG(anytype) FROM anytype WHERE datatype is ?', (dtype,)).fetchone()[0]
        result = result if result else 0
        logging.debug(f'AVG result is: {result}')

        return Response(str(result))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    # i know, we all know, should use a WSGI server instead this dumb run
    app.run(host='0.0.0.0')
