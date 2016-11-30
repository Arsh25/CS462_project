#!/usr/bin/env python2

# lserver.py: Web server for log visualization project 
# 11/29/2016
# Last Edited: 11/29/2016

import SimpleHTTPServer
import BaseHTTPServer
import json

import log_parser


class web_logger_handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		print("Path is:"+self.path)

		if self.path =='/':
			with open ('jmap.html') as index:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(index.read())
				self.wfile.close()
		elif self.path == '/live':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			#ip_addresses, invalid_users = log_parser.parse_auth_log("/var/log/auth.log")
			ip_addresses, invalid_users = log_parser.parse_auth_log("logs/auth.log")
			self.wfile.write(json.dumps(ip_addresses))
			self.wfile.close()
		else:
			server_log = open('logs/server.log','a')
			server_log.write("Invalid URL visited: "+self.path+"\n");
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.wfile.write('<html><h1>404: Page Not Found</h1></html>')
			self.wfile.close()


	def do_POST(self):
		self.send_response(405)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("This server does not support POST yet")

if __name__ == '__main__':
	handler = web_logger_handler
	serverAddress = ('',8080)
	server = BaseHTTPServer.HTTPServer(serverAddress,handler)
	server.serve_forever()
