# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example demonstrates how to generate a refresh token for the Google
Ads API.
This example is meant to be run from the command line and requires either a
client_secrets.json file or a client ID and client secret to be passed as
command line arguments. You can find your client ID and secret from the Google
API Console (https://console.developers.google.com) regardless of which
authentication flow you're using. If you're using the installed application
flow, you can create and download a client_secrets.json file from the API
console.
See the following for more information:
* Installed application flow:
  https://developers.google.com/google-ads/api/docs/client-libs/python/installed-app-flow
* Web application flow:
  https://developers.google.com/google-ads/api/docs/client-libs/python/web-app-flow
"""

import argparse
from google_auth_oauthlib.flow import InstalledAppFlow

# The scope for the Google Ads API.
_SCOPE = "https://www.googleapis.com/auth/adwords"
# The address of the localhost server that will receive the authorization code.
_LOCALHOST = "127.0.0.1"


def main(
    client_secrets_path, client_id, client_secret, scopes, port, headless
):
    """The main method, starts the authorization flow."""
    # Use the client_secrets.json file to identify the application requesting
    # access.
    if client_secrets_path:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_path, scopes=scopes
        )
    # Otherwise, use the client ID and secret to identify the application.
    elif client_id and client_secret:
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://accounts.google.com/o/oauth2/token",
                }
            },
            scopes=scopes,
        )
    else:
        raise ValueError(
            "Please specify either a client secrets file or a client ID and "
            "secret."
        )

    # Note that from_client_config will not know what redirect URI to use, so
    # some versions of google_auth_oauthlib will print a warning. This is
    # intended behavior and the warning can be safely ignored.
    if not headless:
        flow.run_local_server(host=_LOCALHOST, port=port)
    else:
        print(
            "Please visit this URL to authorize this application: "
            f"{flow.authorization_url()[0]}"
        )
        # After the user authorizes, the authorization server will redirect the
        # user to the configured redirect URI. The authorization code is in the
        # "code" query parameter.
        code = input("Enter the authorization code: ")
        flow.fetch_token(code=code)

    # The credentials property of the flow object contains the access and
    # refresh tokens.
    credentials = flow.credentials
    refresh_token = credentials.refresh_token

    print(f"\nYour refresh token is: {refresh_token}\n")
    print(
        "Add your refresh token to your client library configuration file "
        "or environment variables to be able to make API calls."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a refresh token for the Google Ads API."
    )
    # The following arguments are required if a client_secrets.json file is not
    # specified.
    parser.add_argument(
        "--client_id",
        type=str,
        required=False,
        help="The client ID of your application.",
    )
    parser.add_argument(
        "--client_secret",
        type=str,
        required=False,
        help="The client secret of your application.",
    )
    # The following argument is required if a client ID and secret are not
    # specified.
    parser.add_argument(
        "--client_secrets_path",
        type=str,
        required=False,
        default=None,
        help="The path to your client secrets JSON file.",
    )
    parser.add_argument(
        "--scopes",
        type=str,
        nargs="+",
        required=False,
        default=[_SCOPE],
        help="The scopes to request during the authorization flow.",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=False,
        default=8080,
        help="The port on which to run the local server.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="A flag that specifies if the authorization flow should be "
        "run in headless mode. In this mode, you will have to copy an "
        "authorization URL from the console and paste it into a browser. "
        "After authorizing, you will then have to copy the authorization code "
        "from the browser and paste it back into the console.",
    )
    args = parser.parse_args()

    main(
        args.client_secrets_path,
        args.client_id,
        args.client_secret,
        args.scopes,
        args.port,
        args.headless,
    )