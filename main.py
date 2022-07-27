import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from json import loads

driver = webdriver.Firefox()
driver.get("https://www.tiktok.com/")

# on attend que le gars se connecte et va dans ses abonnements
# (j'arrivais pas à me connecter donc jsp si ça marche dessus)
# (et des fois même si j'suis pas co ça marche pas)
while driver.current_url != "https://www.tiktok.com/following":
	sleep(5)

olds = []

while True:
	elements = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div")
	thread_container = driver.find_element_by_xpath("/html")
	action = webdriver.ActionChains(driver)
	for elem in elements:
		if elem.id not in olds:
			try:
				author = elem.find_element_by_xpath("./a").get_attribute("href").split("/@")[1].split("?")[0]
				video = elem.find_element_by_xpath("./div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/video")
			except:
				continue
			
			#####
			# je récupère l'invite what's app pour avoir l'id
			#####
			share = elem.find_element_by_xpath("./div[1]/div[2]/div[2]/button[3]")
			sleep(1)
			action.move_to_element(share)
			action.perform()
			sleep(2)
			video_id = share.find_element_by_xpath("./div[1]/div[1]/a[3]").get_attribute("href").split("%2Fvideo%2F")[1].split("%3F")[0]

			# TODO: récupérer l'id de l'auteur (sinon on saura pas dans quel tar le foutre)
			print("author   :", author)
			print("video url:", video.get_attribute("src"), flush=True)
			print("video id :", video_id)

			thread_container.send_keys(Keys.ARROW_DOWN)
			olds += elements[:elements.index(elem)+1]
			break

	sleep(5)