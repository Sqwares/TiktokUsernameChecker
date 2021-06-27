import requests
import random
import time

def proxies_scraper():
	while True:
		response = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite&simplified=true")
		with open("proxies.txt", "wb") as file:
			file.write(response.content)
			file.close()
		
		time.sleep(300)

def proxies_random(proxies_file):
	with open(proxies_file) as file:
		proxy = random.choice(file.readlines()).rstrip()
		file.close()
	
	proxies = {
		"http": f"http://{proxy}",
		"https": f"http://{proxy}"
	}
	
	return proxies