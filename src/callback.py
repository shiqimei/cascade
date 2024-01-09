from flask import Blueprint, request, jsonify, redirect, url_for
import os
import requests
from src.database import create_connection, update_github_access_token, query_user

github_callback_blueprint = Blueprint('github_callback', __name__)

@github_callback_blueprint.route('/callback/github')
def callback():
    # Retrieve the code from the callback query parameters
    code = request.args.get('code')
    installation_id = request.args.get('installation_id')
    setup_action = request.args.get('setup_action') # install | update
    if not code:
        return jsonify({'error': 'Missing code parameter'}), 400

    # Exchange the code for an access token
    client_id = os.getenv('GITHUB_OAUTH_CLIENT_ID')
    client_secret = os.getenv('GITHUB_OAUTH_CLIENT_SECRET')
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', data=data, headers=headers)

    # Check if the request was successful
    if response.ok:
        # Parse the access token from the response
        resp_json = response.json()
        access_token = resp_json.get('access_token')
        # Handle the access token (e.g., fetch user info, authenticate user, etc.)
        # For the purpose of this example, we'll just return the token
        print('Referrer URL: ', request.url)
        if access_token:
            # Connect to the database and update the access token
            conn = create_connection()
            update_github_access_token(conn, 'shiqimei', access_token)

            if installation_id:
                # Redirect to the dashboard
                return redirect(url_for('dashboard'))
            else:
                # Redirect to installation page
                github_app_id = os.environ.get('GITHUB_APP_NAME')
                return redirect(f'https://github.com/apps/{github_app_id}/installations/select_target', 302)
        else:
            # Handle error response
            return jsonify(response.json()), response.status_code