from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, JWTManager)
from services.elastic_search import es

api = Namespace("User API", description="The User api endpoints")


class UserDbHandler(object):
    def __init__(self):
        pass

    def create_user(self, data):
        resp = es.index(index="endorse-users-index", doc_type="user", body=data, id=data["email"])
        return resp

    def get_all_users(self):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="endorse-users-index", doc_type="user", body=doc, scroll=scroll)
        except:
            return []

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

        return response["hits"]["hits"]

    def get_user_by_email(self, email):
        response = ""
        if es.indices.exists(index="endorse-users-index"):
            response = es.get(index="endorse-users-index", doc_type="user", id=email)
            print(response)

        # if response["hits"]["total"] > 0:
        #    for user in response["hits"]["hits"]:
        #        user["_source"].pop("password")

        return response

    def get_user_by_guid(self, guid):
        q = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"_id": guid}}
                    ]
                }
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="endorse-users-index", doc_type="user", body=q, scroll=scroll)
        except:
            return []

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

        return response["hits"]["hits"]


DbOps = UserDbHandler()


@api.route("/email/<email>")
class list_patient_by_email(Resource):
    def get(self, email):
        resp = DbOps.get_user_by_email(email)
        return resp, 200


@api.route("/guid/<guid>")
class list_patient_by_id(Resource):
    def get(self, guid):
        resp = DbOps.get_user_by_guid(guid)
        return resp, 200


@api.route("/")
class list_all_patients(Resource):
    def get(self):
        try:
            current_user = get_jwt_identity()
            print(current_user)
        except:
            return {"msg": "Missing authorization header"}, 400

        resp = DbOps.get_all_users()
        return resp, 200


@api.route("/login")
class login(Resource):
    def post(self):
        payload = request.get_json(force=True)

        if "email" not in payload or "password" not in payload:
            return {"msg": "email/password Missing"}, 400

        email = payload.get('email', None)
        password = payload.get('password', None)

        if not email:
            return jsonify({"msg": "Missing email parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        print(email)
        result = DbOps.get_user_by_email(email)

        print(result)

        if result["found"] != True:
            return {"msg": "User " + email + " doesn't exist"}, 400

        if check_password_hash(result["_source"]["password"], password) is False:
            return {"msg": "Wrong password"}, 400

        token_payload = {
            "email": email,
            "id": result["_id"],
            "name": result["_source"]["name"],
            "roles": result["_source"]["roles"],
            "image_url": result["_source"]["image_url"]
        }

        access_token = create_access_token(identity=token_payload)

        return {"access_token": access_token}, 200


@api.route("/register")
class register(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    def post(self):
        payload = request.get_json(force=True)

        if "password" not in payload or "email" not in payload:
            return {"msg": "username/password/email Missing"}, 400

        email = payload["email"]
        password = payload["password"]

        # Check if user already exists
        exists_already = DbOps.get_user_by_email(email)
        if len(exists_already) > 0:
            return {"msg": "User with email " + email + " already exists"}, 400

        # Hash the password
        password = generate_password_hash(password.encode())

        data = {
            "password": password,
            "email": email,
        }

        resp = DbOps.create_user(data)
        del data["password"]
        data["id"] = resp["_id"]
        return data, 201
