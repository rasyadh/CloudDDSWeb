from flask import jsonify, json
from keystone import keystone as keystoneapi
import requests

class glance():

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
		self.urlJSON = keystone.getUrl('glance')

		return str(self.urlJSON)

	def imageList(self,imagename):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		if imagename == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/v2/images?sort=name:asc,status:desc"
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/v2/images/"+str(imagename)

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.tmpJSON = json.dumps(self.headers)

		respJSON = self.getRequest(self.urlJSON['url'],str(self.tmpJSON),self.get_param)

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