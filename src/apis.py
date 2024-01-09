from flask import Blueprint, jsonify
from src.database import query_user, create_connection
from src.github import GitHubAppInstallations, GitHubUser
from flask_jwt_extended import jwt_required, get_jwt_identity

rest_apis_blueprint = Blueprint('rest_apis', __name__)

@rest_apis_blueprint.route('/api/github/user')
@jwt_required()
def get_github_user():
    try:
        with GitHubUser() as github_user:
            user = github_user.get_user()
            return jsonify({ "error": None, "data": {
                'username': user.name,
                'avatar': user.avatar_url,
                'bio': user.bio,
                'followers': user.followers,
                'following': user.following
            } }), 200
    except Exception as e:
        return jsonify({ "error": str(e), "data": None }), 500

@rest_apis_blueprint.route('/api/github/authorized_repos')
@jwt_required()
def get_github_app_authorized_repos():
    try:
        repos = []
        with GitHubAppInstallations() as installations:
            for installation in installations:
                for repo in installation.get_repos():
                    repos.append(repo.full_name)
        return jsonify({ 'error': None, 'data': repos }), 200
    except Exception as e:
        return jsonify({ 'error': str(e), 'data': None }), 500
