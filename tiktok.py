import requests
from bs4 import BeautifulSoup
import json
import pickle

def get_sigi(url):
	cookies = {}
	try:
		with open("coookie.cache", "rb") as fp:
			cookies = pickle.load(fp)
	except:
		pass
	response = requests.get(
		url,
		headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"},
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
