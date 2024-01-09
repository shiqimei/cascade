from flask import Blueprint, jsonify
from src.database import query_user, create_connection
from src.github import GithubInstance
from flask_jwt_extended import jwt_required, get_jwt_identity

rest_apis_blueprint = Blueprint('rest_apis', __name__)

@rest_apis_blueprint.route('/api/github/user')
@jwt_required()
def get_github_user():
    try:
        with GithubInstance() as github:
            user = github.get_user()
            return jsonify({ "error": None, "data": {
                'username': user.name,
                'avatar': user.avatar_url,
                'bio': user.bio,
                'followers': user.followers,
                'following': user.following
            } }), 200
    except Exception as e:
        return jsonify({ "error": str(e), "data": None }), 500

@rest_apis_blueprint.route('/api/github/orgs')
@jwt_required()
def get_github_orgs():
    try:
        orgs = []
        with GithubInstance() as github:
            for org in github.get_user().get_followers():
                print('org', org)
                orgs.append(org.login)
        return jsonify({ "error": None, "data": { "orgs": orgs } }), 200

    except Exception as e:
        return jsonify({ "error": str(e), "data": None }), 500
