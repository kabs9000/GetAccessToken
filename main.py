import requests
from web3.auto import w3
from eth_account.messages import encode_defunct
import json


def codeSignature():
        #x = get_raw_message(raw_message)
        private = "92cc6e72ebd50a893a9aeee2ddb5ad25921339334f8f943ae504272789853f60"
        raw_message = "Lunacia Kingdom\n\neyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXNzYWdlIjoiMjE5YjFhMzJhZmE1OWM2ZWU1NGNkMjc2ZGM4YzJmZTE1Zjk4ZTM3MyIsImlhdCI6MTY0MjI2OTgxMywiZXhwIjoxNjQyMjcwNzEzLCJpc3MiOiJBeGllSW5maW5pdHkifQ.qCy3yxxnBdKqnu8UrG-st3YpdSdO2LsCm86x69-cAxI"

        try:
            pk = bytearray.fromhex(private)
            message = encode_defunct(text=raw_message)
            hex_signature = w3.eth.account.sign_message(message, private_key=pk)



            url = 'https://www.w3schools.com/python/demopage.php'
            myobj = {'somekey': 'somevalue'}

            x = requests.post(url, data = myobj)

            sign = (hex_signature[4:5])

            new_sign = sign[0].hex() 
            return((new_sign)) 

        except:
                print("An error occurred in def codeSignature")

     

def printnew_sign():
    p = codeSignature
    return p
    

x= codeSignature()

print(x)