import requests
from bs4 import BeautifulSoup
import json
import pickle

def get_sigi(url):
	cookies = {
		"ttwid": "1%7CEtG-2a95eD2Q1JeYC2PFzfXjJkwONnAtEQcoOlMLI1Y%7C1658844903%7Cf85f6f709c37e4ea4776c4dd0581dbd1f3d0f8bfcefaa3a97cb192bd6d6d062e",
		"_abck": "C419328BCD04D4AE340D9EC3F22D8598~-1~YAAQV9p6XMGo4DWCAQAA9uPmOgj3Xg9VVeZmjM2Q+uUiTYDnZDlav/dN+tX931zhqbBNyV7H1v58cqIKaAxqJuP3kKphB1KnM2kDRiloxcmDTPi6nh+/Wqiwh3cARP/hniczE1tlZpzHlRgmt0xdYAoGoG1mCG1TmMqqUnKfkfGYVU4RF/5wKarMMYy9AyZwLwJqxUvTsYGH51qLwIS0HDT2coF7RHyHH7CRGHznXjDfUu27aoz7928OnnBtDka3rg4YoIm6SP+TS93XXnkTLbyw3a5DaZUH4ZdyzN7x1swj/k/HPKkbvwp/wLxtbDuVUS1Q76xQV+eZsNjHqEygIAUlMSU2fpR4H+ppLLI9Z9M=~-1~-1~-1",
		"s_v_web_id": "verify_l6289gey_pQYbhHj7_ihdg_4qZM_A8YS_MZ2mg3JiRwT3",
		"msToken": "Fzkhj4N6QNvM9YppRefCcM5WYjxZ8C_pvct0R3oTTZdjS62F-Ft465RJJ0_uyZPFK0wS0hMZ5svOfq2iMeGtc9K9xAE8pG-TR4yzqnsqRYU7NGlyUdCiDoKSxRq7IgqXL-M4G_Rhfrk8Xyk="
	}
	try:
		with open("coookie.cache", "rb") as fp:
			cookies = pickle.load(fp)
	except:
		pass
	response = requests.get(
		url,
		headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"},
		cookies=cookies
	)
	with open("cookie.cache", "wb") as fp:
		pickle.dump(response.cookies, fp)

	if response.status_code != 200:
		raise Exception("pas 200 mdr")
	
	soup = BeautifulSoup(response.text, "html.parser")
	tmp = soup.find("script", {"id": "SIGI_STATE"})
	if tmp is None:
		raise Exception("SIGI not found")
	return json.loads('<'.join('>'.join(str(tmp).split(">")[1:]).split("<")[:-1]))

def get_meta_from_video_id(video_id):
	data = get_sigi("https://www.tiktok.com/@/video/"+video_id)
	return {
		"video": data["ItemModule"][video_id],
		"users": data.get("UserModule", {}).get("users", []),
		"comments": data.get("CommentItem", {}).get(video_id, [])
	}

def get_meta_from_profile(user_id):
	data = get_sigi("https://www.tiktok.com/@"+user_id)
	return {
		"videos": data["ItemModule"],
		"users": data.get("UserModule", {}).get("users", [])
	}
