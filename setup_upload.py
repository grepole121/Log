# Setup uploading to dropbox. Only run once

import dropbox

APP_KEY = "j3ttnh3r69s7kz3"
APP_SECRET = "ntb0ntwd2jp7jam"

auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
    dbx.users_get_current_account()
    print("Successfully set up client!")

with open("access_token.py", "w") as conf:
    conf.write(f"access_token = \042{dbx._oauth2_access_token}\042")





