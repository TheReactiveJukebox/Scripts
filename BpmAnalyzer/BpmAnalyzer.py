import logging

import constants
from oauthtool import implicit_flow


def _authorize():
    # Start OAuth2 implicit flow
    auth_response = implicit_flow(constants.authorizeUrl, constants.clientId)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    return auth_response["access_token"]

access_token = _authorize()

print(access_token)