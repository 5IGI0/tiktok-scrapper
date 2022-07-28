from hashlib import md5
import os
from time import time

PRESENCE_DIR=os.path.join(os.getcwd(),"data","presence")

os.makedirs(PRESENCE_DIR, exist_ok=True)

def is_present(element_id):
	table_elem_id = md5(str(element_id).encode("ascii")).hexdigest()
	table_prefix = table_elem_id[:2]

	if not os.path.exists(os.path.join(PRESENCE_DIR,table_prefix)):
		return False

	with open(os.path.join(PRESENCE_DIR,table_prefix)) as fp:
		for line in fp:
			if table_elem_id == line.split(":")[0]:
				return True
		return False

def add_presence(element_id, user_id):
	table_elem_id = md5(str(element_id).encode("ascii")).hexdigest()
	table_prefix = table_elem_id[:2]

	with open(os.path.join(PRESENCE_DIR,table_prefix), "a") as fp:
		fp.write(table_elem_id+":"+str(user_id)+":"+str(int(time()))+"\n")