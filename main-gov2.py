import requests, sys, traceback
import tldextract
from termcolor import colored
from tqdm import tqdm

def godnsrequest(ip_address, apikey):
    url = "https://godns.biz.id/API/index.php"
    payload = f"ip_address={ip_address}&apikey={apikey}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.request("POST", url, data=payload, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            try:
                if data['error'] == 'apikey invalid':
                    return
            except (TypeError, KeyError):
                domains = data
                if domains is not None:
                    return domains
                else:
                    return
        else:
            return
    except Exception as e:
        return

def get_domains(ip_address, apikey):
    domains = godnsrequest(ip_address, apikey)
    if domains is not None:
        with open(f'reversed.txt', 'a', encoding='utf-8') as f:
            for domain in domains:
                if 'domain' in domain:
                    f.write(str(domain['domain']) + '\n')
        return len(domains)
    else:
        return 0


print(colored("""                             
 _____     ____  _____ _____ 
|   __|___|    \|   | |   __|
|  |  | . |  |  | | | |__   |
|_____|___|____/|_|___|_____|
       Project Osint                          
""", "yellow"))

def get_inputs():

    ip_addresses_file = input("Select Your List: ")
    apikey = input("Masukkan API-CODE: ")
    return ip_addresses_file, apikey

ip_addresses_file, apikey = get_inputs()

with open(ip_addresses_file, 'r') as f:
    ip = f.readlines()

ip = [x.strip() for x in ip]
total_ip = len(ip)
processed_ip = 0
success_ip = 0
total_domain = 0
bar = tqdm(ip, desc='Processing IPs', leave=False)
for ip_address in bar:
    try:
        n_domains = get_domains(ip_address, apikey)
        if n_domains > 0:
            success_ip += 1
        else:
            processed_ip += 1
        total_domain += n_domains
        percentage = (processed_ip / total_ip) * 100
        bar.set_description(f"Processing IPs: {ip_address}")
        bar.set_postfix({"Total Domain Success": total_domain})
    except:
        pass
bar.close()
print("Finished Total Domain Success ", total_domain)
