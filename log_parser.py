#!/usr/bin/env python2

# log_parser.py: Parse various Unix log files 
# Arsh Chauhan
# 11/10/2016
# Last Edited: 12/05/2016

# Pre: fileName is a valid auth.log file
# Post: Returns
#	attacks: IP's with invalid login attempts 
#	invalid_users: array of users with attempted login that do not exist on system   
def parse_auth_log(fileName):
	with open(fileName) as log_file:
		auth_log = log_file.readlines()
		attacks = []
		invalid_users = []
		for line in auth_log:
			#print(line)
			attack = line.find("Failed password")
			if attack != -1:
				user = line[line.find("for")+3:line.find("from")]
				ip = line[line.find("from")+4:line.find("port")]
				invalid_user  = line.find("invalid user")
				user = line[line.find('for')+4:line.find('from')-1]
				if invalid_user != -1: # Find invalid users that attackers tried to login as
					invalid_username = line[invalid_user+len("invalid user"):line.find("from")]
					invalid_users.append(invalid_username)
				time_stamp = line[0:15]
				entry = {'time_stamp':time_stamp,'ip':ip,'user':user}
				attacks.append(entry)
		return attacks, invalid_users

def get_unique_ips(attacks):
	unique_ips = []
	for entry in attacks:
		if entry['ip'].strip() not in unique_ips:
		 	unique_ips.append(entry['ip'].strip())
	return unique_ips;

# Pre: user_array is an array 
# Post: Returns
#	sorted_invalid_users: Array of tuples (string,int) representing a username and the 
#							number of times it was found in user_array    
def count_invalid_users(user_array):
	invalid_users = {}
	for user in user_array:
		user = user.strip()
		if user in invalid_users.keys():
			invalid_users[user]+=1
		else:
			invalid_users[user]=1
	sorted_invalid_users = sorted(invalid_users.items(),key=lambda x:x[1],reverse=True)
	return sorted_invalid_users

# Pre: ip_array is an array 
# Post: Returns
#	sorted_ips: Array of tuples (string,int) representing an ip addresse and the 
#							number of times it was found in user_array    
def sort_ips(ip_array):
	sorted_ips={}
	for ip in ip_array:
		ip = ip.strip()
		if ip in sorted_ips.keys():
			sorted_ips[ip] += 1
		else:
			sorted_ips[ip] = 1
	sorted_ips = sorted(sorted_ips.items(),key=lambda x:x[1],reverse=True)
	return sorted_ips

# Pre: sorted_list is an iterable type
#		num is an integer
# Post: Returns
#	top_entries: list containing sorted_list[0] to sorted_list[num] 
def get_top(sorted_list,num):
	top_entries=[]
	for i in range(0,num):
		top_entries.append(sorted_list[i])
	return top_entries


if __name__ == '__main__':
	ssh_attacks,invalid_users = parse_auth_log("logs/auth.log")
	
	# UNCOMMENT TO SEE RAW DATA. WILL SPEW LOTS OF TEXT TO SCREEN
	
	#print("Printing all IP's found with failed SSH logins")
	#print(ssh_attacks)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Printing all invalid users found with failed SSH logins")
	# print(invalid_users)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Printing Unique IP's")
	unique_ips = get_unique_ips(ssh_attacks)
	print(unique_ips)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Sorting usernames found by number of times seen in file")
	# sorted_invalid_users = count_invalid_users(invalid_users)
	# print(sorted_invalid_users)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Sorting IP's found by number of times seen in file")
	# sorted_ips = sort_ips(ssh_attacks)
	# print(sorted_ips)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Printing top 10 usernames")
	# top_usernames = get_top(sorted_invalid_users,10)
	# print(top_usernames)
	# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	# print("Printing top 10 IP's")
	# top_ips = get_top(sorted_ips,10)
	# print(top_ips)