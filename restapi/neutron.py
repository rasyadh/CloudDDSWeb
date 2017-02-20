from flask import jsonify, json
from keystone import keystone as keystoneapi
import requests

class neutron():

	headers = {}
	post_data = {}
	get_param = {}
	urlJSON = ""
	tmpJSON = ""
	respJSON = ""

	def _init_(self):
		self.token = 190997 #not important

	def getUrl(self):
		# make a json object for keystone authentication
		# all in-commented value are default by keystone parameter
		keystone = keystoneapi()
		self.urlJSON = keystone.getUrl('neutron')

		return str(self.urlJSON)

	def floatipList(self,keyname):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		if keyname == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/v2.0/floatingips"
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/v2.0/floatingips/"+str(keyname)

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.tmpJSON = json.dumps(self.headers)

		respJSON = self.getRequest(self.urlJSON['url'],str(self.tmpJSON),self.get_param)

		#print(respJSON)

		return str(respJSON)

	def postRequest(self,url,headers,json_data):

		return ""

	def getRequest(self,url,header,param):
		header = json.loads(header)

		r = requests.get(url, headers = header,params=param)

		return r.text