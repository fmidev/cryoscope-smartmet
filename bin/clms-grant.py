#!/usr/bin/env python3
import json
import jwt
import time
import requests

# Load saved key from filesystem
service_key = json.load(open('/home/ubuntu/.clms-key', 'rb'))

private_key = service_key['private_key'].encode('utf-8')

claim_set = {
    "iss": service_key['client_id'],
    "sub": service_key['user_id'],
    "aud": service_key['token_uri'],
    "iat": int(time.time()),
    "exp": int(time.time() + (60 * 60)),
}
grant = jwt.encode(claim_set, private_key, algorithm='RS256')
result = requests.post(
        service_key["token_uri"],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": grant,
        },
)

access_token_info_json = result.json()
access_token = access_token_info_json.get('access_token')
print(grant)
