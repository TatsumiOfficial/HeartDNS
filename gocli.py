import requests
from termcolor import colored

def read_ip_file(file_name):
  with open(file_name, "r") as file:
    return file.read()

def split_ip_addresses(ip_addresses_raw):
  return ip_addresses_raw.split("\n")

def process_ip(ip_address, api_key, ip_addressing):
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }
  url = "https://godns.biz.id/API/index.php"
  payload = {
    "ip_address": ip_address + ip_addressing,
    "api_key": api_key
  }
  try:
    response = requests.post(url, data=payload, headers=headers, timeout=15)

    if response.status_code == 200:
      data = response.json()

      if "error" in data:
        if data["error"] == "Tidak ada domain yang ditemukan":
          print(colored(f"{ip_address}: Failed Total Domain 0", "red"))
        elif data["error"] == "API key tidak valid atau tidak aktif":
          print(colored(f"{api_key}: Apikey Invalid", "red"))
      else:
        domains = []
        for item in data:
          domains.append(item["domain"])
        with open("domains.txt", "a") as file:
          for domain in domains:
            file.write(domain + "\n")
        print(colored(f"{ip_address}: Success Total Domain {len(domains)}", "green"))
    else:
      print(colored(f"{ip_address}: Apikey Invalid", "red"))

  except:
    print(colored(f"{ip_address}: Unknown Silahkan Check Ulang", "red"))

def main():
  file_name = input("Select Your List : ")
  api_key = input("APIKEY : ")
  ip_addressing = input("Input CIDR IP : ")

  ip_addresses_raw = read_ip_file(file_name)

  ip_addresses = split_ip_addresses(ip_addresses_raw)

  for ip_address in ip_addresses:
    process_ip(ip_address, api_key, ip_addressing)

if __name__ == "__main__":
  main()
