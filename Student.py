import requests
import json

def createAccessToken(url = "https://axieinfinity.com/graphql-server-v2/graphql"):

    payload = json.dumps({
    "operationName": "CreateAccessTokenWithSignature",
    "variables": {
        "input": {
        "mainnet": "ronin",
        "owner": "0x95c62f020c470f6b4d10f28de681c3307203b88b",
        
        #addresses are not real, only examples- please input your own

        "message": "Lunacia Kingdom\n\neyJhbGciOiJIUzI1NiIsInBDS86IkpXVCJ9.eyJtZXNzYWdlIjoiZGJlZTE1MDI0YzlmOGJjM2VkZWE3MDMxNjFmNmFmYWQyNDEyZDc0YiIsImlhdCI6MTY0MTE0MTg3MiwiZXhwIjoxNjQxMTQyNzcyLCJpc3MiOiJBeGllSW5maW5pdHkifQ.0zfZ9N1uaGa3zNAIazpqjlyPQ_n85Mkq1c6qYU6ysbc",
        "signature": "0xd6b17d64e76f2adda48a33b7c4a322f61e3e1d845d0492d3d3ad2d7c4efe42773954b065b1bb0008003163ccfa8cfb92815e162ffdf27f8fc42a6d5f4b23e7eb1b"
        }
    },
    "query": "mutation CreateAccessTokenWithSignature($input: SignatureInput!) {  createAccessTokenWithSignature(input: $input) {    newAccount    result    accessToken    __typename  }}"
    })
    headers = {
    'authority': 'graphql-gateway.axieinfinity.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(response.text)

x = createAccessToken()

print(x)