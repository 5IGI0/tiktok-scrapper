import requests
import json
def awemeRequest(request_path, type="get"):
    headers ={"User-Agent": "okhttp"}
    url = "https://api-t2.tiktokv.com" \
            + request_path \
            + "&device_id=6158568364873266588" \
            + "&version_code=100303" \
            + "&build_number=10.3.3" \
            + "&version_name=10.3.3" \
            + "&aid=1233" \
            + "&app_name=musical_ly" \
            + "&app_language=en" \
            + "&channel=googleplay" \
            + "&device_platform=android" \
            + "&device_brand=Google" \
            + "&device_type=Pixel" \
            + "&os_version=9.0.0"
    print(url)
    if type == "get":
        resp = requests.get(url, headers=headers)
    if type == "post":
        resp = requests.post(url, headers=headers)
    return resp



def getUidByUsername(username):
    endpoint = "/aweme/v1/discover/search/" \
            + "?keyword=" + username \
            + "&cursor=0" \
            + "&count=10" \
            + "&type=1" \
            + "&hot_search=0" \
            + "&search_source=discover"
    response = awemeRequest(endpoint, type="post").json()
    print(json.dumps(response))
    for userObj in response.get("user_list"):
            userInfo = userObj.get("user_info")
            if userInfo.get("unique_id") == username:
                userId = userInfo.get('uid')
                videoCount = userInfo.get('aweme_count')
                roomId = userInfo.get('room_id')
                secUid = userInfo.get('sec_uid')
                return userId
    return ""


def getpost(userId):
endpoint = "/aweme/v1/discover/search/" \
        + "?keyword=fyp"  \
        + "&cursor=0" \
        + "&count=10" \
        + "&type=2"
response = awemeRequest(endpoint, type="post").json()
print(json.dumps(response))


rep=awemeRequest("/aweme/v1/user/follower/list/?user_id=" + str(userId)+"&count=20&max_cursor==0",type="get")
print(response.content)


def getVideosIdByUid(uid, cursor=0, hasmore=True, page=1, count=0, total=0):
    endpoint = "/aweme/v1/aweme/post/?" \
            + "user_id=" + str(uid) \
            + "&count=20" \
            + "&max_cursor=" + str(cursor) 
    response = awemeRequest(endpoint, type="get")
    print(response.content)
    # print(json.dumps(response))
    hasmore = response.get('has_more', True)
    cursor = response.get("max_cursor", cursor)
    videosIdList = []
    for videoObj in response.get("aweme_list"):
        awemeId = videoObj.get("aweme_id")
        url = videoObj.get("video").get("play_addr").get('url_list')[0]
        createTime = videoObj.get("create_time")
        description = videoObj.get("desc")
        userName = videoObj.get("author").get('unique_id')
        count += 1
        videosIdList.append(awemeId)
    if hasmore:
        print()
        page += 1
        getVideosIdByUid(uid=uid, cursor=cursor, hasmore=hasmore,page=page, count=count, total=total)
    else:
        print()
        print("> Finished adding ({:d}/{:d}) videos.".format(count, total))
        if count < total:
            print("! {:d} videos are missing, they are either private or have\n! otherwise not been returned by TikTok's API for unknown reasons.".format((total-count)))
    return videosIdList



userId = getUidByUsername('washingtonpost')
print(userId)
print(getVideosIdByUid(userId))


u= "https://api.tiktokv.com/aweme/v1/aweme/post/?version_code=2.2.1&language=ja&app_name=trill&vid=18DD92EA-42E1-848F-4BA4-CDFAB132F79D&app_version=2.2.1&carrier_region=HK&is_my_cn=1&channel=App%20Store&mcc_mnc=45406&device_id=6539510560658635543&tz_offset=28800&account_region=HK&sys_region=HK&aid=1180&screen_width=640&openudid=92046a2f432be94bec4d1b7369d754ab57259918&os_api=18&ac=WIFI&os_version=11.4&app_language=ja&tz_name=Asia/Hong_Kong&device_platform=iphone&build_number=22102&device_type=iPhone8,4&iid=6564579886684473090&idfa=CE02FD8A-E2BA-44B5-884B-C03EBAFC413B&count=21&max_cursor=0&min_cursor=0&user_id=$_userID&mas=035160f738fae1dd802eef2d7ae9b80526a7d06a0300db4d1378d8&as="+str(time.time())
