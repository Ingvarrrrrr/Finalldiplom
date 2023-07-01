
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from my_core_work_3 import VkTools
from my_data_store_4_4 import check_user,engine

class BotInterface():
    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)
        self.params = {}
        self.offset = 0
        self.worksheets = []

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )

    def get_photos_from_worksheet(self):
        worksheet = self.worksheets.pop()
        photos = self.vk_tools.get_photos(worksheet['id'])
        top_three_photos = photos[:3]
        photo_string = ''
        for photo in top_three_photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
        self.offset += 500
        return worksheet['id'], worksheet, photo_string

    def event_handler(self):
        while True:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.lower() == 'привет':
                        self.params = self.vk_tools.get_profile_info(event.user_id)
                        self.message_send(event.user_id, f"Приветики, {self.params['name']}")
                    elif event.text.lower() == 'поиск':
                        self.message_send(event.user_id, "Погнали")
                        while True:
                            if not self.worksheets:
                                self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
                            worksheet_id, worksheet, photo_string = self.get_photos_from_worksheet()
                            if not check_user(engine,event.user_id, worksheet_id):# сюда столбец с id пользователя и должен
                                self.message_send(
                                    event.user_id,
                                    f'Это {worksheet["name"]}, Вот ссылочка vk.com/id{worksheet["id"]}',
                                    attachment=photo_string)
                                yield event.user_id, worksheet["id"]
                                break
                    elif event.text.lower() == 'пока':
                        self.message_send(event.user_id, 'пока')
                        break
                    elif event.text.lower() == event.text:
                        self.message_send(event.user_id, "Ничего не понимаю, поздароваться хочешь - пиши 'Привет', "
                                                         "хочешь найти кого-нибудь - 'Поиск', уйти хочешь - 'Пока' напиши ")


if __name__ == '__main__':
    bot_interface = BotInterface(comunity_token, acces_token)
    profile_ids = bot_interface.event_handler()

    for profile_id in profile_ids:
        print (profile_ids)
        print(profile_id)
