import time
from colorama import Fore, init
from functions.utilities import title, logo
from modules.playstation.check import starter

init(autoreset=True)

def playstation():
	title("Playstation - Username Checker")

	logo()
	print(f"{Fore.LIGHTMAGENTA_EX}Kontrol edilecek kullanıcı adlarının bulunduğu dosyayı girin. (.txt ile)")
	usernames_file = input("\n~# ")

	logo()
	print(f"{Fore.LIGHTMAGENTA_EX}Proxy Kullanmak İstiyormusunuz (y/n)")
	use_proxies = input("\n~# ").lower()
	if use_proxies == "y":
		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Kendi proxy'lerinizi kullanmak ister misiniz? (Yalnızca HTTP(ler), y/n)")
		own_proxies = input("\n~# ").lower()
		if own_proxies == "y":
			logo()
			print(f"{Fore.LIGHTMAGENTA_EX}Proxy'lerin bulunduğu dosyayı girin. (.txt ile))")
			proxies_file = input("\n~# ")
		else:
			proxies_file = "proxies.txt"
	else:
		own_proxies  = "n"
		proxies_file = None

	logo()
	try:
		print(f"{Fore.LIGHTMAGENTA_EX}Hız Miktarını Giriniz.")
		threads_amount = int(input("\n~# "))
	except:
		logo()
		print(Fore.LIGHTRED_EX + "[Hata] Geçersiz miktar.")
		time.sleep(10)
		init()
	logo()

	starter(usernames_file, use_proxies, own_proxies, proxies_file, threads_amount)