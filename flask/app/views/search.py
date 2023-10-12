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
	if request.method == 'GET':
		if dynamic_route.startswith("solr/blacklight-core/select"):
			headers = request.headers
			params = dict(request.args)

			if params.get("q"):
				params["df"] = "text"

				query = Query()
				params["q"] = query.get_query_expansion(params["q"])

				target_url = f"{SOLR_URL}/{dynamic_route.replace('select', 'search')}"
			else:
				target_url = f"{SOLR_URL}/{dynamic_route}"

			# Forward the GET request
			response = requests.get(target_url, headers=headers, params=params)

			return response.json()
		else:
			# Retrieve incoming headers and query parameters
			headers = request.headers
			params = request.args
			# Forward the GET request
			target_url = f"{SOLR_URL}/{dynamic_route}"
			response = requests.get(target_url, headers=headers, params=params)

			return response.json()
	elif request.method == 'POST':
		# Retrieve incoming JSON data and headers
		data = request.json
		headers = request.headers

		# Forward the POST request
		target_url = f"{SOLR_URL}/{dynamic_route}"
		response = requests.post(target_url, json=data, headers=headers)

		return response.json()

	elif request.method == 'PUT':
		# Retrieve incoming JSON data and headers
		data = request.json
		headers = request.headers

		# Forward the PUT request
		target_url = f"{SOLR_URL}/{dynamic_route}"
		response = requests.put(target_url, json=data, headers=headers)

		return response.json()

	elif request.method == 'DELETE':

		# Retrieve incoming headers
		headers = request.headers

		# Forward the DELETE request
		target_url = f"{SOLR_URL}/{dynamic_route}"
		response = requests.delete(target_url, headers=headers)

		return response.json()
