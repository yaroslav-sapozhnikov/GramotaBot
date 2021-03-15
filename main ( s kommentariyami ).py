import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from requests import post, get
from urllib.request import urlretrieve

from PIL import Image, ImageFont, ImageDraw


access_token = ''
vk_session = vk_api.VkApi(token=access_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def start_point(draw, text, font, center_point): # функция для расчета позиции точки, от которой будет строиться текст
        
        # если не поймешь, что делает эта функция, потом в дискорде объясню визуально
        text_size = draw.textsize(text, font) # получаем размер надписи, которая должна получиться
        start_point = center_point[0] - text_size[0] / 2  # рассчитываем координату Х самой левой точки текста (от нее он будет строиться)

        return (start_point, center_point[1]) # возвращаем полученную координату Х и координату У (ее нам менять не надо)


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        if event.text.lower() == 'привет':
            if event.from_user:

                first_name = vk.users.get(user_ids=(event.user_id))[0]['first_name']
                msg = f'Привет, [id{event.user_id}|{first_name}]'

                vk.messages.send(user_id=event.user_id, message=msg, random_id=get_random_id())

        elif event.text.lower() == 'пока':
            if event.from_user:

                first_name = vk.users.get(user_ids=(event.user_id))[0]['first_name']
                msg = f'Пока, [id{event.user_id}|{first_name}]'

                vk.messages.send(user_id=event.user_id, message=msg, random_id=get_random_id())

        elif event.text.lower() == 'грамота' or event.text.lower() == 'g': # функция грамоты
            if event.from_user:

                first_name = vk.users.get(user_ids=(event.user_id))[0]['first_name'] # получаем имя, фамилию, пол
                last_name = vk.users.get(user_ids=(event.user_id))[0]['last_name']
                sex = vk.users.get(user_ids=(event.user_id), fields='sex')[0]['sex']

                img = Image.open('gramota2.jpg') # открываем картинку
                draw = ImageDraw.Draw(img)

                font = ImageFont.truetype('arial.ttf', size=40) # настройки шрифта

                if sex == 1: # выбираем надпись в зависимости от пола
                    text = 'Самой топовой\nдевушке'
                if sex == 2:
                    text = 'Самому топовому\nпарню'
                text_color = (0,50,0)

                center_point = (298, 300) # точка, относительно которой будет построен текст
                text_position = start_point(draw, text, font, center_point) # чекни вверху кода эту функцию

                draw.multiline_text(text_position, text, text_color, font, align='center') # рисуем текст в несколько линий

                text = f'{first_name} {last_name}' # фамилия и имя, которые мы запишем в грамоту
                text_color = (0,0,0)
                center_point = (298, 400)
                text_position = start_point(draw, text, font, center_point) # все аналогично тому, что выше

                draw.multiline_text(text_position, text, text_color, font, align='center')

                img.save('gramota2_wtxt.jpg') # сохраняем картинку

                upload = vk.photos.getMessagesUploadServer(peer_id=event.user_id)['upload_url'] # получаем ссылку для загрузки картинки на сервера вк
                photo_file = {'photo': open('../images/gramota2_wtxt.jpg', 'rb')} # формируем пост-запрос на сервер с картинкой
                pfile = post(upload, files=photo_file).json() # отправляем пост-запрос, в ответ получаем json с данными загруженной картинки
                photo = vk.photos.saveMessagesPhoto(server=pfile['server'], photo=pfile['photo'], hash=pfile['hash'])[0] # сохраняем картинку на сервере
                attachment = f"photo{photo['owner_id']}_{photo['id']}" # формируем вложение по шаблону (по факту это ссылка на фото)

                vk.messages.send(user_id=event.user_id, message='', attachment=attachment, random_id=get_random_id()) # отправляем картинку

        else:
            if event.from_user:

                first_name = vk.users.get(user_ids=(event.user_id))[0]['first_name']
                msg = f'[id{event.user_id}|{first_name}], я не знаю, что значит "{event.text}"'
                vk.messages.send(user_id=event.user_id, message=msg, random_id=get_random_id())
