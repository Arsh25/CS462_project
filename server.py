#!/usr/bin/env python2

# lserver.py: Web server for log visualization project 
# Arsh Chauhan 
#11/29/2016
# Last Edited: 12/5/2016

import SimpleHTTPServer
import BaseHTTPServer
import json
import threading
import argparse
import socket
from datetime import datetime
from geoip import geolite2
from os import curdir, sep
import cPickle as pickle


import log_parser

#FIXME: Clean up timer on KeyboardInterrupt 
def parse_auth_log(log_file,seconds):
		#ip_addresses, invalid_users = log_parser.parse_auth_log("/var/log/auth.log")
		attacks, invalid_users = log_parser.parse_auth_log(log_file)
		with open('auth_log_ips','a+r') as ip_file:
			attacks_list=[]
			current_attacks = ip_file.read().splitlines()
			for attack in attacks:
				if attack not in current_attacks:
					ip = attack['ip'].strip()
					# ip = "'"+ip+"'"
					if ip != '':
						socket.inet_aton(ip)
						#print(ip)
						geo_data = geolite2.lookup(ip)
						if geo_data is not None:
							attack["lat"] = geo_data.location[0]
							attack["long"] = geo_data.location[1]
						attacks_list.append(attack)
					ip_file.write(str(attacks_list))	
		ip_file.closed
		unique_ips = log_parser.get_unique_ips(attacks)
		with open('unique_ips_file','a+r+b') as unique_ips_file:
			current_unique_ips = unique_ips_file.read().splitlines()
			for ip in unique_ips:
				entry={'ip':ip}
				if ip != '':
					socket.inet_aton(ip)
					#print(ip)
					geo_data = geolite2.lookup(ip)
					if geo_data is not None:
						entry["lat"] = geo_data.location[0]
						entry["long"] = geo_data.location[1]
				if entry not in current_unique_ips:
						unique_ips_file.write(str(entry)+'\n')
				else:
					print("Found " +str(entry) +" in current_unique_ips")

		with open('logs/update.log','a') as parser_log:
			parser_log.write("Ran parse_auth_log at: " + str(datetime.now())+'\n')
		parser_log.closed
		self_timer = threading.Timer(seconds,parse_auth_log,args=[log_file,seconds])
		self_timer.start()
	
class web_logger_handler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path =='/':
			with open ('index.html') as index:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(index.read())
				self.wfile.close()
		elif self.path == '/live':
			entries = []
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()
			with open('auth_log_ips','r') as ip_file:
				for entry in ip_file:
					entries.append(entry)
				# response = set(entries)
				# response = list(response)
				self.wfile.write(json.dumps(entries))
				self.wfile.close()
		elif self.path == '/topip':
			with open('auth_log_ips','r') as ip_file:
				ip_addresses = ip_file.read().splitlines()
				sorted_ips = log_parser.sort_ips(ip_addresses)
				print(sorted_ips)
				top_10_ips = log_parser.get_top(sorted_ips,10)
				self.send_response(200)
				self.send_header('Content-type','application/json')
				self.end_headers()
				self.wfile.write(json.dumps(top_10_ips))
				self.wfile.close()
		elif self.path.endswith('scripts.js'):
			with open ('scripts.js') as scripts:
				self.send_response(200)
				self.send_header('Content-type','application/javascript')
				self.end_headers()
				self.wfile.write(scripts.read())
				self.wfile.close()
		elif self.path.endswith('style.css'):
			with open ('style.css') as styles:
				self.send_response(200)
				self.send_header('Content-type','text/css')
				self.end_headers()
				self.wfile.write(styles.read())
				self.wfile.close()

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
	cli_args.add_argument('--port',dest='port',type=int,help='Port to run this server',default=9000)
	cli_args.add_argument('--log',dest='log_file',type=str,help='File to parse as auth.log',default='logs/auth.log')
	args = cli_args.parse_args()

	parse_auth_log(args.log_file,args.timer_sec)
	handler = web_logger_handler
	serverAddress = ('',args.port)
	server = BaseHTTPServer.HTTPServer(serverAddress,handler)
	server.serve_forever()