import cloudscraper
import threading
import os
import time
from datetime import datetime
from colorama import Fore, init
from functions.utilities import title, logo
from functions.proxies import proxies_scraper, proxies_random

init(autoreset=True)

locker = threading.Lock()
request = cloudscraper.create_scraper()

date = datetime.today().strftime("%Y-%m-%d %H.%M.%S")
tocheck = []
hits = 0
invalid = 0

def check(use_proxies, proxies_file, username):
	global tocheck, hits, invalid

	retry = 0
	while retry <= 5:
		try:
			if use_proxies == "y":
				proxy = proxies_random(proxies_file)
			else:
				proxy = {
					"http": None,
					"https": None
				}
			response = request.post("https://accounts.api.playstation.com/api/v1/accounts/onlineIds", json={"onlineId": username, "reserveIfAvailable": False}, proxies=proxy)
			if response.status_code != 403:
				locker.acquire()
				if response.status_code == 201:
					hits += 1
					title(f"Checking - Hits: {hits}")	
					
					if not os.path.exists(f"bulunan/Playstation/{date}"):
						os.makedirs(f"bulunan/Playstation/{date}")
					if not os.path.isfile(f"results/Playstation/{date}/playstation.txt"):
						open(f"bulunan/Playstation/{date}/playstation", "x").close()
					with open(f"bulunan/Playstation/{date}/playstation", "a") as file:
						file.write(f"{username}\n")
						file.close()
					
					print(f"{Fore.LIGHTGREEN_EX}[Hit] {username}")
				else:
					invalid += 1
					print(f"{Fore.LIGHTRED_EX}[Invalid] {username}")
				
				if len(tocheck) == hits + invalid:
					title("Kontrol - Tamamlandı")

					logo()
					print(f"{Fore.LIGHTWHITE_EX}Username Checker Buldu {Fore.LIGHTGREEN_EX}{hits} {Fore.LIGHTWHITE_EX}mevcut kullanıcı adları!")
					if hits >= 1:
						print(f"{Fore.LIGHTWHITE_EX}mevcut kullanıcı adlarını burdan bulabilirsiniz: bulunan/Playstation/{date}/bulunan.txt")
					time.sleep(10)
				locker.release()
				break
			else:
				retry += 1
				locker.acquire()
				print(f"{Fore.LIGHTRED_EX}[Proxy Kara Listeye Alındı] {username} - {proxy['http']}")
				locker.release()
		except:
			pass
	
	if retry >= 5:
		invalid += 1
		if len(tocheck) == hits + invalid:
			locker.acquire()
			title("Kontrol - Tamamlandı")

			logo()
			print(f"{Fore.LIGHTRED_EX}Username-Checker Buldu {Fore.LIGHTGREEN_EX}{hits} {Fore.LIGHTRED_EX}mevcut kullanıcı adları!")
			if hits >= 1:
				print(f"{Fore.LIGHTRED_EX}Burdan Bulabilirsiniz: {Fore.LIGHTGREEN_EX}bulunan/Playstation/{date}/bulunan.txt")
			locker.release()
			time.sleep(10)

def starter(usernames_file, use_proxies, own_proxies, proxies_file, threads_amount):
	global tocheck
	
	with open(usernames_file) as file:
		for username in file:
			tocheck.append(username.rstrip())

		file.close()

	if use_proxies == "y":
		if own_proxies != "y":
			threading.Thread(target=proxies_scraper).start()

	title(f"Hedef İsimler Kontrol Ediliyor: {hits}")

	for username in tocheck:
		thread = threading.Thread(target=check, args=(use_proxies, proxies_file, username))
		thread.start()

		default_threads = threading.active_count()
		if threading.active_count() == threads_amount + default_threads:
			thread.join()
