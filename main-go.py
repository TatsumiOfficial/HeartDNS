import requests, sys, traceback
import tldextract
from termcolor import colored

def read_file(file_name):
	liss = [ i.strip() for i in open(file_name, 'r').readlines() ]
	return liss

def filter(list_web, list_filter):
    filter_word = list_filter
    
    trash = []

    for website in list_web:
        for mute_word in filter_word:
            if mute_word in website:
                trash.append(website)
                break
    

    for trasher in trash:
        try:
            list_web.remove(trasher)
        except Exception as e:
            print(str(e) + " --> Exception goes here")

    return list_web

def subdomain_filter(list_web):
	new_domain = []
	
	for x in list_web:
		domain = tldextract.extract(x).registered_domain
		new_domain.append(domain)
	
	return new_domain

def process_ip(ip_address, api_key, cidr, is_subdo, is_filter):
	url = "https://godns.biz.id/API/index.php"
	
	payload = {
		"ip_address": ip_address + cidr,
		"api_key": api_key
	}

	try:
		response = requests.post(url, data=payload, timeout=45)
		
		if response.status_code == 200:
			data = response.json()

			if "error" in data:
				if data["error"] == "Tidak ada domain yang ditemukan":
					print(colored(ip_address + " : Total Domain 0", "red"))
				elif data["error"] == "API key tidak valid atau tidak aktif":
					print(colored(api_key + " : Apikey Invalid", "red"))
					sys.exit()
			else:
				domains = []
				
				for item in data:
					domains.append(item['domain'])
			
				if is_subdo:
					print("subdo filtering")
					domains = subdomain_filter(domains)

				if is_filter:
					domains = filter(domains, is_filter)

				with open('domains.txt', 'a') as file:
					for domain in domains:
						file.write(domain+"\n")

				print(colored(ip_address + ": Success Total Domain " + str(len(domains)), "green"))
		else:
			save = open('log.txt', 'a')
			save.write(str(response.status_code)+"\n"+str(response.content)+"\n")
			save.close()

			print(colored(ip_address + ": Something went wrong with the server, send log.txt", "red"))
			sys.exit()

	except Exception as e:
		save = open('log.txt', 'a')
		save.write(str(e) + "\n")
		save.close()

		print(colored("Check your internet connection\n"));
		print("Log saved to log.txt\n")
		sys.exit()			


def main():
	file_name = input("List : ")
	api_key = input("APIKEY : ")
	cidr = input("RANGE IP/16 /24 [or just enter] : ")
	is_filter = input("Filter list [or just enter]: ")
	is_subdo = input("Grab subdo [y/N] :")

	try:
		#Process IP#
		ip_addresses_raw = read_file(file_name)
		#Process filter#
		try:
			answer = is_filter.strip()
			
			if len(answer) < 1:
				print("Empty filter")
				filtering = False

			else:
				filter_raw = read_file(is_filter)

				if len(filter_raw) < 1:
					print("Empty filter")
					filtering = False
				else:
					print(colored("Found " + str(len(filter_raw)) + " filter list"))
					filtering = filter_raw

		except Exception as e:

			print("Filter list not found")
			sys.exit()

		#Process subdo#
		answer = is_subdo.strip()

		if answer == "y" or answer =="Y":
			get_subdo = False
		else:
			get_subdo = True

		for ip_address in ip_addresses_raw:
			process_ip(ip_address.strip(), api_key, cidr, get_subdo, filtering)

	except Exception as e:
		print(traceback.format_exc())
		print("File not found")
		sys.exit()

if __name__ == "__main__":
	main()
