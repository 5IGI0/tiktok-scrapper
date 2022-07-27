import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep, time
from json import loads, load, dumps
from table_manager import is_present, add_presence
import requests
import tarfile
from os import path, utime
from downloader import add_file_from_memory
from gzip import compress

driver = webdriver.Firefox()
driver.get("https://www.tiktok.com/")

with open("cookies.json") as fp:
	for item in load(fp):
		driver.add_cookie(item)
driver.get("https://www.tiktok.com/following")

driver.execute_script("window.open('about:blank','_blank');")
sleep(2)
driver.switch_to.window(driver.window_handles[0])

# on attend que le gars se connecte et va dans ses abonnements
# (j'arrivais pas à me connecter donc jsp si ça marche dessus)
# (et des fois même si j'suis pas co ça marche pas)
#while driver.current_url != "https://www.tiktok.com/following":
#	sleep(5)

olds = []

DOWNLOAD_DIR="./data/content/"

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
		mtime = path.getmtime(DOWNLOAD_DIR+"/"+data["author_id"]+".tar")
	except:
		pass

	with tarfile.open(name=DOWNLOAD_DIR+"/"+data["author_id"]+".tar", mode="a") as archive:
		add_file_from_memory(
			archive, data["video_id"]+".json.gz",
			compress(dumps(data).encode(), compresslevel=9)
		)
		add_file_from_memory(
			archive, data["video_id"]+".mp4",
			response.content
		)

	utime(DOWNLOAD_DIR+"/"+data["author_id"]+".tar", times=(mtime,mtime))
	add_presence(data["video_id"], data["author_id"])
	print("done.")

while True:
	elements = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div")
	thread_container = driver.find_element_by_xpath("/html")
	action = webdriver.ActionChains(driver)
	for elem in elements:
		if elem.id not in olds:
			try:
				author_link = elem.find_element_by_xpath("./a").get_attribute("href")
				author = author_link.split("/@")[1].split("?")[0]
				video_url = elem.find_element_by_xpath("./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/video").get_attribute("src")
			except:
				continue

			#####
			# je récupère l'invite what's app pour avoir l'id
			#####
			share = elem.find_element_by_xpath("./div[1]/div[2]/div[2]/button[3]")
			action.move_to_element(share)
			action.perform()
			sleep(0.2)
			video_id = share.find_element_by_xpath("./div[1]/div[1]/a[3]").get_attribute("href").split("%2Fvideo%2F")[1].split("%3F")[0]

			if not is_present(video_id):
				# on vas dans l'onglet qu'on vient d'ouvrir
				driver.switch_to.window(driver.window_handles[1])
				driver.get(author_link)
				author_data = loads(driver.find_element_by_id("SIGI_STATE").get_attribute("innerText"))["UserModule"]["users"][author]
				author_id = author_data["id"]
				driver.switch_to.window(driver.window_handles[0])
				
				print("author id:", author_id)
				print("video url:", video_url)
				print("video id :", video_id)

				download(video_url, {
					"author_id": author_id,
					"video_id": video_id,
					"author": author_data
				})
			else:
				print("already downloaded, skip")

			thread_container.send_keys(Keys.ARROW_DOWN)
			olds += elements[:elements.index(elem)+1]
			break
	sleep(0.75)