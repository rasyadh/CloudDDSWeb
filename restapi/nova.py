from flask import jsonify, json
from keystone import keystone as keystoneapi
import requests

class nova():

	headers = {}
	data = {}
	post_data = ""
	get_param = {}
	urlJSON = ""
	headJSON = ""
	contJSON = {}
	keypair = {}
	respJSON = ""
	server = {}
	networks = {}
	network = []
	OS_SCH_HNT = {}
	returnJSON = ""
	responsepacket = {}

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

		r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		respJSON = r.text

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

		r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		respJSON = r.text

		#print(respJSON)

		return str(respJSON)

	def serverCreate(self,name,imageRef,flavorRef,availability_zone, key_name, networks_uuid):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		self.server['name'] = name
		self.server['imageRef'] = imageRef
		self.server['flavorRef'] = flavorRef
		self.server['availability_zone'] = availability_zone
		self.server['key_name'] = key_name
		self.network = [{"uuid": ""+networks_uuid}]
		self.server['networks'] = self.network
		#self.OS_SCH_HNT['same_host'] = "48e6a9f6-30af-47e0-bc04-acaed113bb4e"
		self.data['server'] = self.server
		#self.data['OS-SCH-HNT:scheduler_hints'] = self.OS_SCH_HNT

		self.post_data = json.dumps(self.data)

		self.urlJSON['url'] = self.urlJSON['url']+"/servers"
		r = self.postRequest(self.urlJSON['url'],str(self.headJSON),self.post_data)
		respJSON = r.text

		#print(respJSON)

		return respJSON

	def serverList(self,server_id):
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		if server_id == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/servers"
			r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		else:
			self.urlJSON['url'] = self.urlJSON['url']+"/servers/"+server_id
			r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		respJSON = r.text

		return respJSON




	def keyList(self,keyname):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		if keyname == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs"
			r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs/"+str(keyname)
			r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)

		respJSON = r.text

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
		
		r = self.postRequest(self.urlJSON['url'],str(self.headJSON),str(self.contJSON))
		respJSON = r.text

		if r.status_code == 200:
			self.responsepacket['status'] = True
			self.responsepacket['content'] = respJSON
			self.returnJSON = json.dumps(self.responsepacket)
		else :
			self.responsepacket['status'] = False
			respJSON = json.loads(respJSON)
			self.responsepacket['content'] = respJSON
			self.returnJSON = json.dumps(self.responsepacket)

		return str(self.returnJSON)

	def keyDel(self,keyname):
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		self.urlJSON['url'] = self.urlJSON['url']+"/os-keypairs/"+str(keyname)
		r = self.delRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		respJSON = r.text

		return respJSON


	def netList(self,netid):
		#self.urlJSON = self.getUrl()
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		if netid == "yj34f8r7j34t79j38jgygvf3":
			self.urlJSON['url'] = self.urlJSON['url']+"/os-networks"
			r = self.getRequest(self.urlJSON['url'],str(self.headJSON),self.get_param)
		else :
			self.urlJSON['url'] = self.urlJSON['url']+"/os-networks"+str(netid)
			r = self.postRequest(self.urlJSON['url'],str(self.headJSON),str(self.contJSON))

		respJSON = r.text

		#print(respJSON)

		return str(respJSON)

	addFloatingIp = {}


	def setFloatingIp(self,privateip,publicip,serverid):
		self.urlJSON = json.loads(self.getUrl())

		self.headers['Content-Type'] = 'application/json'
		self.headers['X-Auth-Token'] = self.urlJSON['x-token']
		self.headJSON = json.dumps(self.headers)

		self.addFloatingIp['address'] = publicip
		self.addFloatingIp['fixed_address'] = privateip
		self.data['addFloatingIp'] = self.addFloatingIp

		self.post_data = json.dumps(self.data)

		self.urlJSON['url'] = self.urlJSON['url']+"/servers/" + str(serverid) + "/action"
		r = self.postRequest(self.urlJSON['url'],str(self.headJSON),self.post_data)
		respJSON = r.text

		#print(respJSON)

		return respJSON

	def postRequest(self,url,headers,json_data):
		headers = json.loads(headers)
		r = requests.post(url, data=json_data, headers=headers)

		return r

	def getRequest(self,url,header,param):
		header = json.loads(header)

		r = requests.get(url, headers = header,params=param)

		return r

	def delRequest(self,url, header,param):
		header = json.loads(header)

		r = requests.delete(url, headers = header, params=param)

		return r