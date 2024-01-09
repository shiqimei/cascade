from github import Github, Auth, GithubIntegration
from flask_jwt_extended import get_jwt_identity
from src.database import create_connection, query_user
import os
import base64

class GitHubUser:
    """
    A context manager for creating and managing a Github instance with a user-specific access token.

    This class simplifies the process of connecting to the Github API using an access token
    associated with a specific user. The user's identity is determined using the JWT token
    in the current Flask request context. It retrieves the user's Github access token from the database
    and initializes a Github instance with it. This instance can then be used within a 'with' block
    to interact with the Github API. The Github instance is automatically closed when exiting the 'with' block.

    Attributes:
        userid (str): User ID obtained from the JWT token in the current request context.
        github (Github, optional): The Github instance initialized with the user's access token. 
            It's None until the context manager enters the 'with' block.

    Example usage:
        with GithubInstance() as github:
            # Use the github instance to interact with the Github API
            user_info = github.get_user().name
            # Perform other Github API operations
    """
    def __init__(self):
        self.userid = get_jwt_identity()
        self.github = None

    def __enter__(self):
        conn = create_connection()
        [_userid, _username, _jwt, github_access_token] = query_user(conn, self.userid)

        auth = Auth.Token(github_access_token)
        self.github = Github(auth=auth)
        return self.github

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.github.close()

class GitHubAppInstallations:
    """
    A context manager for creating and managing a Github instance with a GitHub App installation access token.

    This class simplifies the process of connecting to the Github API using an access token
    obtained from a GitHub App installation. It generates a JWT using the App's private key
    and uses it to obtain an installation access token. This instance can then be used within a 'with' block
    to interact with the Github API. The Github instance is automatically closed when exiting the 'with' block.

    Attributes:
        app_id (str): The ID of the GitHub App.
        private_key (str): The private key of the GitHub App.
        installation_id (str): The installation ID for which to get the access token.
        github (Github, optional): The Github instance initialized with the installation's access token. 
            It's None until the context manager enters the 'with' block.

    Example usage:
        with GitHubAppInstance(app_id, private_key, installation_id) as github:
            # Use the github instance to interact with the Github API
            user_info = github.get_user().name
            # Perform other Github API operations
    """

    def __init__(self):
        self.app_id = os.environ.get('GITHUB_APP_ID')

        private_key_base64 = os.getenv('GITHUB_APP_PRIVATE_KEY_BASE64')
        if private_key_base64 is None:
            raise ValueError('The GITHUB_APP_PRIVATE_KEY_BASE64 environment variable is not set')

        private_key = base64.b64decode(private_key_base64).decode('utf-8')
        self.private_key = private_key
        self.installations = []

    def __enter__(self):
        with GitHubUser() as github_user:
            installation_ids =[]
            for installation in github_user.get_user().get_installations():
                if str(installation.app_id) == os.environ.get('GITHUB_APP_ID'):
                    installation_ids.append(installation.id)
            if len(installation_ids) > 0:
                for installation_id in installation_ids:
                    integration = GithubIntegration(self.app_id, self.private_key)
                    self.installations.append(integration.get_app_installation(installation_id))
                return self.installations
            else:
                # TODO
                # Navigate to f'https://github.com/apps/{github_app_id}/installations/select_target'
                # if the app is not installed.
                raise ValueError('The GitHub App is not installed.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up the Github instance
        pass
