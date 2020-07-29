import sys
import requests
import hashlib

if __name__ == '__main__':
	if len(sys.argv) < 2 :
		print("please provide atleast one password to check :)")
		exit()
	passwords_list = sys.argv[1:]
	
	for password in passwords_list:
		print(f"checking for {password} ...")
	#password = sys.argv[1]
		sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
		#print(sha1_password)
		url = 'https://api.pwnedpasswords.com/range/'+sha1_password[0:5]
		response = requests.get(url)
		#print(dir(response))
		is_password_seen = False
		response_list = response.content.decode('utf-8').split('\n')
		for response_item in response_list:
			if sha1_password[5:] in response_item:
				is_password_seen = True
				times_leaked = response_item.split(":")[1][0]
				print(f'{password} is been listed {times_leaked} times please consider changing')
				break
		if not is_password_seen:
			print(f'{password} is never seen till now')