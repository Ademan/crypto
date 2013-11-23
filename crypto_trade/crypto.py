#Matuszed 2013-07-03
#Questions about usage email mindsdecree@gmail.com

import time
import hmac
import base64
import hashlib
import urllib
import urllib2
import json
import httplib

class Throttle(object):
    def __init__(self, window, max):
        self.window = window
        self.max = max
        self.count = 0
        self.last = time.time() - window # We don't want to wait even if we immediately call throttle

    def peek(self):
        diff = time.time() - self.last

    def throttle(self):
        diff = time.time() - self.last
        if diff > self.window:
                self.count = 0
                self.last = time.time()
        self.count += 1
        if self.count > self.max:
            time.sleep(self.window - diff)

class CryptoTrade(object):
	def __init__(self, key='', secret='', agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0'):
		self.key, self.secret, self.agent = key, secret, agent
		self.baseprivate = 'https://www.crypto-trade.com/api/1/private/'	# for authenticated POST requests
		self.basepublic = 'https://www.crypto-trade.com/api/1/'				# for unauthenticated GET requests

	def reqpublic(self, path):
		# Send a request to the public API
		try:
			conn = httplib.HTTPSConnection("crypto-trade.com")
			url = self.basepublic + path
			print url
			conn.request("GET", url)
			response = conn.getresponse()
			try:
				response = json.load(response)
			except ValueError:
				response = {'success':0, 'error':'No JSON in response. Crypto-Trade down.'}
			conn.close()
			return response
		except:
			return {'success':0, 'error':'Connection failed.'}

	def makereq(self, path, data):
		# bare-bones hmac rest sign
		params = {'nonce':str(int(time.time() * 1e3))}
		return urllib2.Request(self.baseprivate + path, params, {
                        #'Content-Type' :'application/json',
			'AuthKey': self.key,
			'AuthSign': hmac.new(self.secret, data, hashlib.sha512).hexdigest()
		})

	def req(self, path, inp={}):
                # send request
                inp['nonce'] = str(int(time.time() * 1e3))
                inpstr = urllib.urlencode(inp.items())
                req = self.makereq(path, inpstr)
                response = urllib2.urlopen(req, inpstr)

                # interpret json response
                output = json.load(response)
                if 'error' in output:
                        raise ValueError(output['error'])
                return output
