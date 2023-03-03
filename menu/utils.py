import requests
import json


def send_notification(registration_ids, message_title, message_desc):
    try:
        fcm_api = "AAAAasZ17Sw:APA91bGJ7VUPdMGuNoVspTWdisG0rROoah-KqidIvcRYAdo_bKRfsRndhOOhVJPHrQ5wYd8QF3q3RZiEaHoZXia6T0Fxx8bsBfe3C32YuHq_BBXpcSeWJHZskOIbifNPvOJultxg5She"
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Content-Type": "application/json",
            "Authorization": 'key=' + fcm_api}

        payload = {
            "registration_ids": registration_ids,
            "priority": "high",
            "notification": {
                "body": message_desc,
                "title": message_title,
                "image": "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
                "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",

            }
        }

        result = requests.post(url, data=json.dumps(payload), headers=headers)
        response = result.json()
        if int(response['failure']) == 1:
            return False
        return True
    except json.JSONDecodeError:
        pass
