import requests
import tarfile
from os import makedirs, utime, path, getcwd
import io
from gzip import compress
import json
from time import time

from tiktok import get_meta_from_video_id, get_meta_from_profile
from table_manager import is_present, add_presence

DOWNLOAD_DIR=path.join(getcwd(),"data","content")
makedirs(DOWNLOAD_DIR, exist_ok=True)

def add_file_from_memory(archive, fname, buffer):
	info = tarfile.TarInfo(fname)
	info.size = len(buffer)
	archive.addfile(info, fileobj=io.BytesIO(buffer))

def download_tiktok(video_id):
	print("downloading tiktok", video_id)

	if is_present(video_id):
		print("this asset is already present, skiping.")
		return

	data = get_meta_from_video_id(video_id)

	print("author:", data["video"]["author"], data["video"]["authorId"])

	mtime = time()
	try:
		mtime = path.getmtime(path.join(DOWNLOAD_DIR,data["video"]["authorId"]+".tar"))
	except:
		pass

	with tarfile.open(name=DOWNLOAD_DIR+"/"+data["video"]["authorId"]+".tar", mode="a") as archive:
		add_file_from_memory(
			archive, data["video"]["id"]+".json.gz",
			compress(json.dumps(data).encode(), compresslevel=9))
		add_file_from_memory(archive, data["video"]["id"]+".mp4",
			requests.get(data["video"]["video"]["downloadAddr"]).content
		)

	utime(DOWNLOAD_DIR+"/"+data["video"]["authorId"]+".tar", times=(mtime,mtime))
	
	add_presence(video_id, data["video"]["authorId"])
	print("done.")

def download_tiktoks_profile(user_id):
	print("downloading [new]", user_id, "tiktoks")

	data = get_meta_from_profile(user_id)

	numeric_user_id = list(data["users"].values())[0]["id"]

	with tarfile.open(name=path.join(DOWNLOAD_DIR,list(data["users"].values())[0]["id"]+".tar"), mode="a") as archive:
		for video in data["videos"].values():
			json_data = json.dumps({
				"video": video,
				"users": data["users"]
			}).encode()

			if is_present(video["id"]):
				continue
				
			print("downloading tiktok", video["id"])

			add_file_from_memory(
				archive, video["id"]+".json.gz",
				compress(json_data, compresslevel=9))
			add_file_from_memory(archive, video["id"]+".mp4",
				requests.get(video["video"]["downloadAddr"]).content
			)

			add_presence(video["id"], list(data["users"].values())[0]["id"])

	print("done.")
	utime(path.join(DOWNLOAD_DIR,numeric_user_id+".tar"), times=(time(),time()))
	


if __name__ == "__main__":
	import sys

	if sys.argv[1].isdigit():
		download_tiktok(sys.argv[1])
	else:
		download_tiktoks_profile(sys.argv[1].replace("@",""))
