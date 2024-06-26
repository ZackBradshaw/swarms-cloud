import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client


# Load environment variables
load_dotenv()

# HTTP Bearer
http_bearer = HTTPBearer()


def is_token_valid(
    token: str = None,
    #    supabase: Client = supabase_client_init
) -> bool:
    """
    Check if a token is valid by querying the Supabase database.

    Args:
        token (str): The token to be checked.
        supabase (Client): The Supabase client object.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    # Supabase client
    supabase = create_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
    )

    try:
        # Query the Supabase database to check if the token exists in the 'keys' column of the 'swarms_cloud_api_key' table
        response = (
            supabase.table("swarms_cloud_api_keys")
            .select("key")
            .filter("key", "eq", token)
            .execute()
        )
        return response["data"] is not None and len(response["data"]) > 0
    except Exception as error:
        print(f"Error checking token validity: {error}")
        return False


def fetch_api_key_info(
    token: str = None,
    # supabase: Client = supabase_client_init
):
    """
    Fetch the id and user_id of an API key from the Supabase database.

    Args:
        token (str): The API key to be checked.
        supabase (Client): The Supabase client object.

    Returns:
        dict: A dictionary containing the id and user_id if the API key is valid, None otherwise.
    """
    # Supabase client
    supabase = create_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
    )
    # Query the Supabase database to check if the token exists in the 'keys' column of the 'swarms_cloud_api_key' table
    try:
        response = (
            supabase.table("swarms_cloud_api_keys")
            .select("id", "user_id", "key")
            .filter("key", "eq", token)
            .execute()
        )
        if response["data"] is not None and len(response["data"]) > 0:
            return response["data"][0]  # return the first matching row
        else:
            return None
    except Exception as error:
        print(f"Error fetching API key info: {error}")
        return None


def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    """
    Authenticates the user based on the provided credentials.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.

    Returns:
        str: The authentication token.

    Raises:
        HTTPException: If the token is invalid.
    """
    token = credentials.credentials
    token = token.split("Bearer ")[1]
    token = token.strip()
    print(token)
    valid = is_token_valid(token)
    print(valid)
    if not is_token_valid(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please authenticate with a valid token at https://swarms.world/dashboard",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def verify_token(req: Request):
    token = req.headers["Authorization"]
    # Here your code for verifying the token or whatever you use
    token = token.split("Bearer ")[1]
    token = token.strip()
    valid = is_token_valid(token)
    if valid is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
