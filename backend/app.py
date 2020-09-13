from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})

@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/restaurants", methods=['GET'])
def get_restaurants():
	minRating = request.args.get('minRating')
	if minRating is not None:
		return create_response({"restaurants": db.getByMinRating('restaurants', int(minRating))})
	return create_response({"restaurants": db.get('restaurants')})
		
@app.route("/restaurants/<id>", methods=['GET'])
def get_restaurant(id):
  restaurant = db.getById('restaurants', int(id))
  if restaurant is None:
    return create_resopnse(status=404, message="No restaurant with this id exists")
  return create_response(restaurant)

@app.route("/restaurants/<id>", methods=['DELETE'])
def delete_restaurant(id):
    if db.getById('restaurants', int(id)) is None:
        return create_response(status=404, message="No restaurant with this id exists")
    db.deleteById('restaurants', int(id))
    return create_response(message="Restaurant deleted")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
