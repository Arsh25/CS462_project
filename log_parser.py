#!/usr/bin/env python2

# log_parser.py: Parse various Unix log files 
# 11/10/2016
# Last Edited: 11/10/2016

# Pre: fileName is a valid auth.log file
# Post: Returns
#	attacks: Dictionary where key is atatcker IP and value is user attempted to login as
#	invalid_users: array of users with attempted login that do not exist on system   
def parse_auth_log(fileName):
	with open(fileName) as log_file:
		auth_log = log_file.readlines()
		attacks = {}
		invalid_users = []
		for line in auth_log:
			#print(line)
			attack = line.find("Failed password")
			if attack != -1:
				user = line[line.find("for")+3:line.find("from")]
				ip = line[line.find("from")+4:line.find("port")]
				invalid_user  = line.find("invalid user")
				if invalid_user != -1: # Find invalid users that attackers tried to login as
					invalid_username = line[invalid_user+len("invalid user"):line.find("from")]
					invalid_users.append(invalid_username)
				attacks[ip] = user
		return attacks, invalid_users

if __name__ == '__main__':
	ssh_attacks,invalid_users = parse_auth_log("auth.log")
	attacker_ips={}
	# Count attacks from IP's
	# for attacker in ssh_attacks:
	# 	if attacker not in attacker_ips:
	# 		attacker_ips[attacker] = 1
	# 	else:
	# 		attacker_ips[attack] += 1	
	print(invalid_users)
	print(ssh_attacks)