#!/usr/bin/env python2

# lserver.py: Web server for log visualization project 
# 11/29/2016
# Last Edited: 11/30/2016

import SimpleHTTPServer
import BaseHTTPServer
import json
import threading
import argparse


import log_parser

#FIXME: Clean up timer on KeyboardInterrupt 
def parse_auth_log(seconds):
		#ip_addresses, invalid_users = log_parser.parse_auth_log("/var/log/auth.log")
		ip_addresses, invalid_users = log_parser.parse_auth_log("logs/auth.log")
		with open('auth_log_ips','w') as ip_file:
			ip_file.write(json.dumps(ip_addresses))
		ip_file.closed
		self_timer = threading.Timer(seconds,parse_auth_log)
		self_timer.start()
	
class web_logger_handler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
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
			with open('auth_log_ips','r') as ip_file:
				ip_addresses = json.loads(ip_file.read())
				self.wfile.write(json.dumps(ip_addresses))
				self.wfile.close()
			ip_file.closed
		else:
			server_log = open('logs/server.log','a')
			server_log.write("Invalid URL visited: "+self.path+"\n");
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body><h1>404 Page Not Found\
							 <br> \
							 <img src="http://thecatapi.com/api/images/get?format=src&type=gif"\>\
							 <br> </h1><a href="/">Home Page</a> </body></html>')
			self.wfile.close()
			server_log.close()


	def do_POST(self):
		self.send_response(405)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("This server does not support POST yet")

if __name__ == '__main__':
	cli_args = argparse.ArgumentParser(description='Parse common *nix logs and map on a webpage')
	cli_args.add_argument('--timer',dest='timer_sec',type=int,help='Parse log file every --timer seconds',default=300)
	cli_args.add_argument('--port',dest='port',type=int,help='Port to run this server',default=8080)
	args = cli_args.parse_args()

	parse_auth_log(args.timer_sec)
	handler = web_logger_handler
	serverAddress = ('',args.port)
	server = BaseHTTPServer.HTTPServer(serverAddress,handler)
	server.serve_forever()