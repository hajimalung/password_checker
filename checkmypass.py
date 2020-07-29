import sys
import hashlib
import requests
def get_pawned_passwords_tailing_hashes_of(hash_param):
	url = 'https://api.pwnedpasswords.com/range/'+hash_param
	response = requests.get(url)
	if response.status_code == 200:
		return response.text.splitlines()
	else: 
		raise RuntimError('something went wrong while fetching pwned hashes')

def get_count_of_tail_seen_in(list_of_hashes,hash_to_check):
	for item in list_of_hashes:
		hash_in_list,count = item.split(':')
		if hash_to_check == hash_in_list:
			return count
	return 0

def count_num_times_password_seen(password):
	hashed_password = get_hashed_password(password)
	first_5_in_hash_of_password,tailing_hash_of_password = hashed_password[:5],hashed_password[5:]
	list_of_tails_to_check = get_pawned_passwords_tailing_hashes_of(first_5_in_hash_of_password)
	return  get_count_of_tail_seen_in(list_of_tails_to_check,tailing_hash_of_password)

def get_hashed_password(password):
	encoded_password = password.encode('utf-8')
	sha1_password = hashlib.sha1(encoded_password)
	hex_digested_password = sha1_password.hexdigest()
	return hex_digested_password.upper()

def check_passwords_pwned(passwords_list):
	for password in passwords_list:
		count = count_num_times_password_seen(password)
		if count:
			print(f'{password} is seen {count} times please consider changing it!!!!')
		else: 
			print(f'{password} is never seen you can continue using it. :)')
	return "all passwords checked for pwning"

if __name__ == '__main__':
	if len(sys.argv) < 2 :
		print("please provide atleast one password to check :)")
		exit(1)
	sys.exit(check_passwords_pwned(sys.argv[1:]))
	
	# for password in passwords_list:
	# 	print(f"checking for {password} ...")
	# #password = sys.argv[1]
	# 	sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	# 	#print(sha1_password)
	# 	url = 'https://api.pwnedpasswords.com/range/'+sha1_password[0:5]
	# 	response = requests.get(url)
	# 	#print(dir(response))
	# 	is_password_seen = False
	# 	response_list = response.content.decode('utf-8').split('\n')
	# 	for response_item in response_list:
	# 		if sha1_password[5:] in response_item:
	# 			is_password_seen = True
	# 			times_leaked = response_item.split(":")[1][0]
	# 			print(f'{password} is been listed {times_leaked} times please consider changing')
	# 			break
	# 	if not is_password_seen:
	# 		print(f'{password} is never seen till now')