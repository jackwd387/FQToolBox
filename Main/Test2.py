import requests,json,os
def reading(tone_id,item_ids):
  url = f"https://reading.snssdk.com/reading/reader/audio/playinfo/?tone_id={tone_id}&item_ids={item_ids}&aid=507386&version_code=999"
  data = json.loads(requests.get(url=url).text)["data"][0]
  print("主:"+data["main_url"])
  print("备用:"+data["backup_url"])
  return data["main_url"]
reading(input('音色:'),input('item_id:'))
input('Enter键退出')
