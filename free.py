import requests, sys, traceback
import tldextract
from termcolor import colored

def godnsrequest(ip_address, apikey):
  url = "https://heartdns.com/API/search.php"
  payload = f"ip_address={ip_address}&apikey={apikey}"
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  try:
    response = requests.request("POST", url, data=payload, headers=headers, timeout=15)

    if response.status_code == 200:
      data = response.json()
      try:
        if data['error'] == 'apikey invalid':
          print(colored(apikey + " -> Apikey & Device invalid", "red"))
          return
      except (TypeError, KeyError):
        domains = data
        if domains is not None:
          return domains
        else:
          print(colored(ip_address + " -> Failed Total Domain 0", "red"))
    else:
      print(f"ERROR -> {ip_address}", response.status_code)
  except Exception as e:
    print(colored("Check your internet connection\n"));
    return []

def get_domains(ip_address, apikey):
    domains = godnsrequest(ip_address, apikey)
    if domains is not None:
        print(colored(ip_address + " -> Success Total Domain " + str(len(domains)), "green"))
        with open(f'reversed.txt', 'a', encoding='utf-8') as f:
            for domain in domains:
                if 'domain' in domain:
                    f.write(str(domain['domain']) + '\n')
                else:
                    print(colored(f"{ip_address} -> Failed, Invalid Domain", "red"))
    else:
        print(colored(f"{ip_address} -> Failed, Invalid Domain", "red"))

def get_inputs():
  ip_addresses_file = input("Select Your List: ")
  apikey = input("Masukkan API-CODE: ")
  return ip_addresses_file, apikey

ip_addresses_file, apikey = get_inputs()

with open(ip_addresses_file, 'r') as f:
  ip = f.readlines()

ip = [x.strip() for x in ip]

for ip_address in ip:
  domains = get_domains(ip_address, apikey)
