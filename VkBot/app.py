import os
import warnings

import config
import json
import vk
from flask import Flask, request
from vk_api.keyboard import VkKeyboard

warnings.simplefilter("ignore")
from models import *
from supfunc import *


dphoto=-14
dbegin=3


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'VkProfi bot v 2.0!'



@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего POST-запроса

    data = json.loads(request.data)
    print(data)

    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return config.confirmation_token
    elif data['type'] == 'message_new':

        session = vk.Session(config.vktoken)
        api = vk.API(session, v=5.8)

        user_id = data['object']['from_id']
        print(data)

        #Создадим пользователя
        try:
            if(len(Subs.select().where(Subs.vk_id==user_id))==0):
                u=Subs(vk_id=user_id,name=user_id,qnow=1,bals="")
            else: u=Subs.get(Subs.vk_id==user_id)
            if (data['object']['text'] == 'Старт' or data['object']['text'] == 'Начало'):
                api.messages.send( user_id=str(user_id),
                                  message="Добро пожаловать, ответь на парочку наших вопросов и мы"+
                                          "расскажем тебе о твоем будущем")
                u.qnow = dbegin
                u.bals=""
                u.save()
            elif data['object']['text'] == 'Да':
                s=Subs.get(Subs.vk_id==user_id)
                s.result=1
                s.save()
            elif data['object']['text'] == 'Нет':
                s=Subs.get(Subs.vk_id==user_id)
                s.result=0
                s.save()

            else:
                if (u.qnow > len(rTest.select())+dbegin):
                    api.messages.send( user_id=str(user_id),
                                      message='Что бы пройти тест еще раз, отправьте "Старт" ')
                    return 'ok'

                an = 0
                i = 0
                print(u.qnow)
                s = str(rTest.select().where(rTest.id == u.qnow)[0].ans)
                ubegin=u.bals
                for ans in s.split(';'):
                    i += 1
                    if ( data['object']['text'] == ans ):
                        an = i
                        u.bals += str(an)
                        break
                if(ubegin==u.bals):
                    u.bals+='1'
                u.save()

            if(u.qnow>len(rTest.select())+dbegin):
                u.qnow=1
                u.result=data['object']['text']
                u.save()
                k = VkKeyboard(one_time=False)
                api.messages.send( user_id=str(user_id),
                                  message="Спасибо и удачи вам", keyboard=k.get_empty_keyboard())
                return "ok"


            elif(u.qnow==len(rTest.select())+dbegin):
                #бработка данных
                api.messages.send( user_id=str(user_id),
                                  message="Обработка данных")
                # Вывести результаты
                answers=u.bals
                wname=predict(answers)

                wor=Works.get(Works.name==wname)
                winfo=wor.winfo
                work=wor.name

                api.messages.send(user_id=user_id,
                                  attachment=wor.photoname)
                #Отправляем информацию о профессии
                api.messages.send( user_id=str(user_id),
                                  message=winfo)


                k = VkKeyboard(one_time=False)
                k.add_button("Да", color='positive', payload=None)
                k.add_button("Нет", color='negative', payload=None)
                api.messages.send( user_id=str(user_id),
                                  message="Тест окончен, вы довольны результатом?",keyboard=k.get_keyboard())
                u.qnow += 1
                u.save()

                return 'ok'


            k = VkKeyboard(one_time=True)
            k.get_keyboard()

            print('qnow',u.qnow)
            tt = rTest.select().where(rTest.id == u.qnow + 1)[0].text
            if (tt == 't'):
                api.messages.send(user_id=user_id,
                                  attachment=rTest.get(rTest.id == u.qnow + 1).photoname)

                addmes="На что похоже?"
            else:
                addmes = tt

            i=0
            t=0
            le= len(rTest.select().where(rTest.id==u.qnow+1)[0].ans.split(';'))
            for ans in rTest.select().where(rTest.id==u.qnow+1)[0].ans.split(';'):

                if (i == 2 and le!=t):
                    i=0
                    k.add_line()
                i += 1
                t += 1

                k.add_button(ans, color='primary', payload=None)


            api.messages.send( user_id=user_id,
                              keyboard=k.get_keyboard(), message=addmes)

            u.qnow += 1
            u.save()

        except Exception as e:
            print(e)
            api.messages.send( user_id=user_id,
                             message="Сообщение не распознано, что бы пройти тест еще раз, отправьте 'Старт'")

        # Сообщение о том, что обработка прошла успешно
        return 'ok'



if __name__ == '__main__':

    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
