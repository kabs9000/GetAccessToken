from inspect import signature
import requests
import json
#import yaml
from web3.auto import w3
from eth_account.messages import encode_defunct
import objectpath

#from Scholar import Scholar

class Student(object):

	def __init__(self, ronin_address, private_key):
		"""
		Init the class variables, we need a ronin address and its private key
		:param ronin_address: The ronin address
		:param private_key: Private key belonging to the ronin account
		"""
		#with open("secret.yaml") as file:
		#	config = yaml.safe_load(file)

		#self.config = config
		self.ronin_address = ronin_address
		self.private_key = private_key
		self.url = "https://graphql-gateway.axieinfinity.com/graphql"
		self.message = self.createRandomMessage()
		self.morphMessage = self.morphAxie()


	#	for scholar in config['scholars']:
	#		if config['scholars'][scholar]['ronin_address'] == ronin_address:
	#			self.payout_percentage = config['scholars'][scholar]['payout_percentage']
	#			self.personal_ronin = config['scholars'][scholar]['personal_ronin']
	##			self.name = scholar
	#			break
	#		else:
	#			self.payout_percentage = 0
	#			self.personal_ronin = None

	def printPrivate(self):
		
		private = self.private_key
		return(private)

	def createRandomMessage (self):            #this works well
			try:
				payload = json.dumps({
				"operationName": "CreateRandomMessage",
				"variables": {},
				"query": "mutation CreateRandomMessage {\n  createRandomMessage\n}\n"
				})
				headers = {
				'Content-Type': 'application/json'
				}

				response = requests.request("POST", self.url, headers=headers, data=payload)
				try:
					json_data = json.loads(response.text)
				except ValueError as e:
					return e
				return (json_data['data']['createRandomMessage']).replace("\n", "\n")

			except: print("error in createRandomMessage") 
	
	def morphAxie(self) :
			try:

				axieId = self.getAxieList()

				morphSig = self.createMorphSignature()

				ronin = "0x"+self.ronin_address
				
				payload = json.dumps({
				"operationName": "MorphAxie",
				"variables": {"axieId": axieId, "owner": ronin, "signature":morphSig},
				"query": "mutation MorphAxie($axieId: ID!, $owner: String!, $signature: String!) {\n  morphAxie(axieId: $axieId, owner: $owner, signature: $signature)\n}\n"
				})
				
				headers = {
				'Content-Type': 'application/json'
				}

				response = requests.request("POST", self.url, headers=headers, data=payload)
				try:
					json_data = json.loads(response.text)
				except ValueError as e:
					return e
				return (json_data)

			except: print("error in morphaxieRandomMessage") 
	def createMorphSignature (self):
			private_key= self.private_key
			axieId = self.getAxieList()
			ronin = "0x"+self.ronin_address
			try:
				pk = bytearray.fromhex(private_key)
				
				payload = "axie_id="+ axieId +"&owner="+ ronin
				message = encode_defunct(text=payload)
				hex_signature = w3.eth.account.sign_message(message, private_key=pk)

				#print(hex_signature)

				#url = 'https://www.w3schools.com/python/demopage.php'
				#myobj = {'somekey': 'somevalue'}

				#x = requests.post(url, data = myobj)
				sign = (hex_signature[4:5])
				new_sign = sign[0].hex()

				return(new_sign)
			except:
				
				print("error in morphSignature")

	def createSignature(self):
			private_key= self.private_key
			     #this bit works
			#raw_message= "Lunacia Kingdom/neyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXNzYWdlIjoiN2RkZDkxYTFiNWZhZDIyYmIwNzJiYWU1ZTk1N2JkYzRhZGJkMjUyOCIsImlhdCI6MTY0MTkxNzAyNywiZXhwIjoxNjQxOTE3OTI3LCJpc3MiOiJBeGllSW5maW5pdHkifQ.UZOVHel2gEGckMG63N5jtJZ1P2LPPvJF7vnL0Pa26Jc"
			#private_key= "92cc6e72ebd50a893a9aeee2ddb5ad25921339334f8f943ae504272789853f60"
			try:
				pk = bytearray.fromhex(private_key)
				message = encode_defunct(text=self.message)
				hex_signature = w3.eth.account.sign_message(message, private_key=pk)

				#print(hex_signature)

				#url = 'https://www.w3schools.com/python/demopage.php'
				myobj = {'somekey': 'somevalue'}

				#x = requests.post(url, data = myobj)
				sign = (hex_signature[4:5])
				new_sign = sign[0].hex()

				return(new_sign)
			except:
				
				print("error in createSignature")


	def createAccessToken(self):
		url = "https://axieinfinity.com/graphql-server-v2/graphql"
		ronin = "0x" + self.ronin_address
		sig = self.createSignature()
		payload = json.dumps({
		"operationName": "CreateAccessTokenWithSignature",
		"variables": {
			"input": {
            "mainnet": "ronin",
            "owner": ronin,
            "message": self.message,
            "signature": sig,
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
		print(sig)
		try:
					json_data = json.loads(response.text)
					token = json_data['data']['createAccessTokenWithSignature']['accessToken']
		except ValueError as e:
					return e
		return (str(json_data['data']['createAccessTokenWithSignature']['accessToken']), json_data, sig)
	def getAxieList(self):
		ronin = "0x"+ self.ronin_address

		try:

			payload = json.dumps({
			"operationName": "GetAxieBriefList",
			"variables": {
				"from": 0,
				"size": 24,
				"sort": "PriceAsc",
				"auctionType": "All",
				"owner": ronin,
				"criteria": {}
			},
			"query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
			})
			headers = {
			'Content-Type': 'application/json'
			}

			response = requests.request("POST", self.url, headers=headers, data=payload)
			r = json.loads(response.text)
			tree = objectpath.Tree(r)
			result = tree.execute("$.data.axies.results[@.stage is 1].id")
			object = ""
			for object in result:
				return(object)

			return(object)

		except print:("error in getAxieList")

	def loopMorphAxie(self):
		pass


	
		


		

	

#input format is Scholar1 = Student("95c62f020c470f6b6510f28de681c3307203b88b", "92cc6e72ebd57653a9aeee2ddb5ad25921339334f8f943ae504272789853f60")
# ronin:95c62f020c4787657810f28de681c3307203b88b - ronin, 0x92cc6e72ebd50a893a9aeee2ddb678987339334f8f943ae504272789853f60 - 0x
#addresses are not real, only examples- please input your own

Scholar1 = Student("95c62f020c470d734d10f28de681c3307203b88b", "92cc6e72ebd50a893a9aeee2dd83fhhsy5921339334f8f943ae504272789853f60")


#xxx = Scholar1.createRandomMessage()
#xxx = Scholar1.createAccessToken()
#xxx = Scholar1.morphAxie()
#xxx = Scholar1.createSignature()
#xxx = Scholar1.createMorphSignature()
xxx = Scholar1.morphAxie()
#getAxieList = Scholar1.getAxieList()



print(xxx)





