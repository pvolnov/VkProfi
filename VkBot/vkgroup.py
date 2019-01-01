import json

import requests
import vk
import config
from  models import Subs
session = vk.Session(access_token=config.vktoken)
vk = vk.API(session,v=5.5)


users = Subs.select()
for u in users:

    url = vk.photos.getMessagesUploadServer(peer_id=191215854)['upload_url']


    photo_files = open('f.jpg','rb')
    r = requests.post(url, files={'photo': photo_files})
    #vk.messages.send(user_id=u.vk_id, attachment='photo'+owner_id+'_'+ )

    result = json.loads(r.text)

    uploadResult = vk.photos.saveMessagesPhoto(server=result["server"],
                                                  photo=result["photo"],
                                                  hash=result["hash"])

    # vk.messages.send(user_id=191215854,
    #                     attachment=uploadResult[0]["id"])
    vk.messages.send(user_id=u.vk_id, attachment='photo' +str(uploadResult[0]['owner_id']) + '_' + str(uploadResult[0]['id']))
    print(uploadResult[0])
