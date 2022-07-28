# import selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import seleniumwire,selenium
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep, time
from json import loads, load, dumps, dump
from table_manager import is_present, add_presence
import requests
import tarfile
from os import path, utime, getcwd
from downloader import add_file_from_memory
from gzip import compress
import json 

profile = webdriver.FirefoxProfile()
profile.set_preference("media.volume_scale", "0.0")
profile.set_preference("browser.link.open_newwindow", 3)
profile.set_preference("dom.webdriver.enabled", False) #spoof navigator.webdriver to undefined in js
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()

driver = webdriver.Firefox(firefox_profile=profile,seleniumwire_options={
    'suppress_connection_errors': False,
    'connection_timeout': None, # Show full tracebacks for any connection errors
	# 'connection_keep_alive': False
})
def interceptor(request, response):  # A response interceptor takes two args
	if 'tiktok.com/api/user/list' in request.url:
		body=json.loads(decode(response.body, response.headers.get('Content-Encoding', 'identity')))
		userlist=body.get("userList")
		if userlist:
			for user in userlist:
				pass
		else:
			print("WTFF")
			print(body)
			exit()
	elif 'tiktok.com/api/following' in request.url:
		body=json.loads(decode(response.body, response.headers.get('Content-Encoding', 'identity')))



driver.response_interceptor = interceptor
driver.get("https://www.tiktok.com/")

with open("cookies.json") as fp:
	for item in load(fp):
		driver.add_cookie(item)

driver.get("https://www.tiktok.com/following")
driver.maximize_window()

# on attend que le gars se connecte et va dans ses abonnements
# (j'arrivais pas à me connecter donc jsp si ça marche dessus)
# (et des fois même si j'suis pas co ça marche pas)
# from selenium.webdriver.support.ui import WebDriverWait
#while driver.current_url != "https://www.tiktok.com/following":
#	sleep(5)

olds = []
user_cache = {}

try:
	with open("user_cache2.json", "r") as fp:
		user_cache = load(fp)
except:
	pass

DOWNLOAD_DIR=path.join(getcwd(),"data","content")

def download(url, data):
	print("downloading", data["video_id"])
	try:
		response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"})
		if response.status_code != 200:
			raise Exception(response.status_code, response.reason)
	except Exception as e:
		print("err mdr", e)
		return
	mtime = time()
	try:
		mtime = path.getmtime(path.join(DOWNLOAD_DIR,data["author"]["uniqueId"].encode("utf8").hex()+".tar"))
	except:
		pass
	with tarfile.open(name=path.join(DOWNLOAD_DIR,data["author"]["uniqueId"].encode("utf8").hex()+".tar"), mode="a") as archive:
		add_file_from_memory(
			archive, data["video_id"]+".json.gz",
			compress(dumps(data).encode(), compresslevel=9)
		)
		add_file_from_memory(
			archive, data["video_id"]+".mp4",
			response.content
		)
	utime(path.join(DOWNLOAD_DIR,data["author"]["uniqueId"].encode("utf8").hex()+".tar"), times=(mtime,mtime))
	add_presence(data["video_id"], data["author_id"])
	print("done.")

i = 0
y = 0
while True:
	elements = driver.find_elements("xpath","/html/body/div[2]/div[2]/div[2]/div/div")
	thread_container = driver.find_element("xpath","/html")
	i += 1
	y += 1
	for elem in elements:
		#driver.execute_script('a = document.getElementsByTagName("video"); for (i = 0; i < a.length; i++) {a[i].volume = 0.0;}')
		if elem.id not in olds:
			try:
				author_elem =  elem.find_element("xpath","./a")
				author_link = author_elem.get_attribute("href")
				author = author_link.split("/@")[1].split("?")[0]
				video_elem = elem.find_element("xpath","./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/video")
				video_url = video_elem.get_attribute("src")
				#driver.execute_script("arguments[0].volume = 0.0;", video_elem)

				#####
				# je récupère l'invite what's app pour avoir l'id
				#####
				action = webdriver.ActionChains(driver)
				#action.click(elem.find_element("xpath","./div[1]/div[2]/div[2]/button[1]"))
				share = elem.find_element("xpath","./div[1]/div[2]/div[2]/button[3]")
				action.move_to_element(share)
				action.perform()
				video_id = share.find_element("xpath","./div[1]/div[1]/a[3]").get_attribute("href").split("%2Fvideo%2F")[1].split("%3F")[0]
			
				#action = webdriver.ActionChains(driver)
				#action.move_by_offset(-250, 0)
				#action.perform()
			except:
				continue
				
			print("video id :", video_id)
			
			if not is_present(video_id):
				if not author in user_cache:
					author_data = {"id": None, "uniqueId": author}
				else:
					author_data = user_cache[author]
				author_id = author_data["id"]
				
				print("author id:", author_id)
				print("video url:", video_url)

				download(video_url, {
					"author_id": author_id,
					"video_id": video_id,
					"author": author_data
				})
			else:
				print("already downloaded, skip")
			i = 0
			y += 1
			thread_container.send_keys(Keys.ARROW_DOWN)
			olds.append(elem.id)
			sleep(1)
		
	if i >= 5 or y >= 50:
		driver.refresh()
		i = 0
		y = 0
		olds = []
	
