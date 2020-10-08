import requests
import os
from typing import Tuple

CLIENT_ID = "c128fe76-dc54-4daa-993c-1a13c1e82080"
"""
The client id (biit) provided by azure
"""

TENANT_ID = "4130bd39-7c53-419c-b1e5-8758d6d63f21"
"""
The tenant id (purdue) provided by azure
"""

REDIRECT_URI = "https://auth.expo.io/@stephend17/biit-mobile"
"""
The redirect url registered with azure. 
"""


def azure_refresh_token(refresh_token: str) -> Tuple[str, str]:
    """
    Refreshes a given refresh token and returns the
    new access token and refresh token

    Args:
        refresh_token (str): the refresh token provided by azure
                             when authenticating on the client.

    Returns:
        Tuple[str, str]: A tuple containing the new access token
                         and the new refresh token for the client
                         to use.

                         NOTE: if the request fails then
                         a tuple of 2 empty strings will be
                         returned. When this happens the client
                         will need to redo the entire oauth
                         process and obtain a new refresh token.

    """
    stage = os.getenv("STAGE")
    if stage is "dev":
        return ("AccessToken", "RefreshToken")

    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    payload = f"client_id={CLIENT_ID}&scope=https://graph.microsoft.com/User.Read&redirect_uri={REDIRECT_URI}&grant_type=refresh_token&refresh_token={refresh_token}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    rjson = response.json()

    if response.status_code != 200:
        return ("", "")

    return (rjson["access_token"], rjson["refresh_token"])
