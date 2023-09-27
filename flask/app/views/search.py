import json
import requests
from flask import Blueprint, Response, request
from flask_cors import CORS

from app.query import Query

search = Blueprint('search', __name__)
CORS(search)

SOLR_URL = "http://3.132.90.207:8983"


@search.route("/", methods=["GET"])
def semantic_search2():
	return Response(f"Solr Search Engine", 200)


@search.route("/search", methods=["GET"])
def semantic_search():
	query = Query()
	q = request.args.get('q')
	return json.dumps(query.get_query_expansion(q))


@search.route('/<path:dynamic_route>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_all(dynamic_route):
	print(dynamic_route, request.args)
	params = "?"
	for key in request.args:
		if params != "?":
			params += "&"
		params += key + "=" + request.args.get(key)
	print(f"{SOLR_URL}/{dynamic_route}{params}")
	response = requests.get(f"{SOLR_URL}/{dynamic_route}{params}")
	if response.status_code == 200:
		print("sucessfully fetched the data with parameters provided")
		print(json.dumps(response.json()))
	else:
		print(f"Hello person, there's a {response.status_code} error with your request")
	return Response(f"Handling {dynamic_route}", 200)
