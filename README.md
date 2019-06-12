## 605 sentry oauth client 

### Overview
This repository contains client code for 605 sentry oauth server. At this moment, it implements implicit-grant-type flow. You can integrate the code into your project or use it as a reference model.

### How to 

```
import sys

from oauth.sentry import SentryClient

server_url = 'https://sentry.605.tv'
client_id = '< Registered application id >'
auth_url = 'https://sentry.605.tv/oauth/authorize'
redirect_url = '< Your online application url for redirect>'
scopes = ['public']
state = 'xyz'


def main():
    with SentryClient(server_url, client_id, auth_url, redirect_url) as sentry:
        access_token = sentry.get_access_token(
            'username', 'password')
    print(access_token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
