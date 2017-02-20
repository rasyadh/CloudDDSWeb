from flask import jsonify, json
from keystone import keystone as keystoneapi
import requests

class nova():

	headers = {}
	post_data = {}
	get_param = {}
	urlJSON = ""
	headJSON = ""
	contJSON = {}
	respJSON = ""
	keypair = {}

	def _init_(self):
		self.token = 190997 #not important

	def getUrl(self):
		# make a json object for keystone authentication
		# all in-commented value are default by keystone parameter
		keystone = keystoneapi()
		self.urlJSON = keystone.getUrl('nova')

		return str(self.urlJSON)

	def flavorList(self,flavorid):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		if flavorid == 0:
			self.urlJSON['url'] = self.urlJSON['url']+"/flavors/detail"
		else:
			self.urlJSON['url'] = self.urlJSON['url']+"/flavors/"+str(flavorid)

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		respJSON = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		#print(respJSON)

		return str(respJSON)

	def imageList(self,imageid):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		if imageid == 0:
			self.urlJSON['url'] = self.urlJSON['url']+"/images/detail"
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/images/"+str(imageid)

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		respJSON = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		#print(respJSON)

		return str(respJSON)

	def keyList(self,keyname):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		if keyname == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs"
			respJSON = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs/"+str(keyname)
			respJSON = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		return respJSON

	def keyNew(self,keyname):
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		self.keypair['name'] = keyname
		self.contJSON['keypair'] = self.keypair
		self.contJSON = json.dumps(self.contJSON)
		self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs"
		respJSON = self.postRequest(self.urlJSON['url'],str(self.headJSON),str(self.contJSON))

		return respJSON

	def keyDel(self,keyname):
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs/"+str(keyname)
		respJSON = self.delRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		return respJSON


	def netList(self,netid):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		if netid == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/os-networks"
			respJSON = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/os-networks"+str(netid)
			respJSON = self.postRequest(self.urlJSON['url'],str(self.headJSON),str(self.contJSON))

		#print(respJSON)

		return str(respJSON)

	def postRequest(self,url,headers,json_data):
		headers = json.loads(headers)
		r = requests.post(url, data=json_data, headers=headers)

		return r.text

	def getRequest(self,url,header,param):
		header = json.loads(header)

		r = requests.get(url, headers = header,params=param)

		return r.text

	def delRequest(self,url, header,param):
		header = json.loads(header)

		r = requests.delete(url, headers = header, params=param)

		return r.text
