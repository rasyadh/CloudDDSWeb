from flask import jsonify, json
import requests

class keystone():

	url = 'http://10.14.36.107:5000/v3/auth/tokens/'
	headers = {'Content-Type' : 'application/json'}
	contentJSON = {}
	responsepacket = {}
	token = ""
	data = {}
	domain = {}
	user = {}
	password = {}
	identity = {}
	auth = {}
	methods = []
	json_data = ""
	resp = ""
	returnvalue = {}
	returnJSON = ""


	def _init_(self):
		self.token = 190997

	def myRequest(self):
		# make a json object for keystone authentication
		# all in-commented value are default by keystone parameter
		self.domain['name'] = 'default'
		self.user['name'] = 'master' #username
		self.user['domain'] = self.domain
		self.user['password'] = 'master' #password
		self.password['user'] = self.user
		self.methods = ["password"]
		self.identity['methods'] = self.methods
		self.identity['password'] = self.password
		self.auth['identity'] = self.identity
		self.data['auth'] = self.auth

		self.json_data = json.dumps(self.data)

		r = requests.post(self.url, data=self.json_data, headers=self.headers)

		self.contentJSON = json.loads(r.text)
		
		#print(r.headers)

		if r.status_code == 201:
			self.responsepacket['x-token'] = r.headers['X-Subject-Token']
		else :
			self.responsepacket['x-token'] = ""
		
		self.responsepacket['content'] = self.contentJSON

		self.returnJSON = json.dumps(self.responsepacket)

		return str(self.returnJSON)

	def getUrl(self, servicename):
		respJSON = json.loads(self.myRequest())
		self.returnvalue['status'] = False
		self.returnvalue['url'] = "Can't get the requested service url"
		self.returnvalue['x-token'] = respJSON['x-token']

		self.contentJSON = respJSON['content']

		for catalog in self.contentJSON['token']['catalog']:
			if servicename == catalog['name']:
				self.returnvalue['status'] = True
				self.returnvalue['url'] = catalog['endpoints'][0]['url']

		self.returnJSON = json.dumps(self.returnvalue)

		#print("check")

		return str(self.returnJSON)