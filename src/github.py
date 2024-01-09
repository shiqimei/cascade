from github import Github, Auth
from flask_jwt_extended import get_jwt_identity
from src.database import create_connection, query_user

class GithubInstance:
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
