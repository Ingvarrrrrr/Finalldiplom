from pprint import pprint
from datetime import datetime
# импортирую
import vk_api
from vk_api.exceptions import ApiError


from config import acces_token


# get users data
class VkTools:
    def __init__(self, acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)


    def _bdate_toyear(self, bdate):
        user_year = bdate.split('.')[2]
        now = datetime.now().year
        return now - int(user_year)


    # def get_profile_info(self, user_id):
    #     # TRY -это работа с ошибками или исключениями,( если дословно на человеческом,
    #     # то пытайся делать действие ниже, и если вдруг окажется что чего то не неходится, в данном
    #     # случае ответа от АПИ, тогда забей на всё и доложи мне об этом, но продолжай мониторить,
    #     # если вдруг АПИ начнёт отвечать, то продолжай работу. То есть не даст работнику
    #     # забить на всё раз и навсегда, однажды не получив ответ.
    #     # в данном случае будет обрабатываться
    #     # такой косяк, если висит VK и не получается от него ответ, но VKapi тоже не дураки
    #     # писали и все исключения api обрабатывает сам, поэтому импортируем from vk_api.exceptions import ApiError
    #
    #     try:
    #         info, = self.vkapi.method('users.get',
    #                                   {'user_id': user_id,
    #                                    'fields': 'city,sex,bdate,relation'})
    #
    #         # когда делаешь исключения надо всегда описывать, какую ошибку ждёшь
    #         # иначе как компу догадаться? сейчас мы ждем ошибку АПИ и указали ApiError, Если
    #         # не указывать конкретное исключение, то как я понимаю, любую ошибку будет приписывать
    #         # к этому исключению и отрабатываться как исключение. НЕОБХОДИМО КОНКРЕТИЗИРОВАТЬ. В данном
    #         # случае если происходит ошибка, то info = пустому словарю, и выводится сообщение про косяк
    #
    #     except ApiError:
    #         info = {}
    #         print(f'У нас тут косяк со стороны АПИ')
    #
    #     # получаем из словаря нормально Имя и Фамилию, но
    #     # но это нигде не выводится, нужно для дальyейшего обращения бота ко пользователю, пол просто
    #     # в виде кода остаётя, можно прикрутить мужчина женщина, но зачем, город по названию
    #     # При этом город, это словарь в словаре, распаковываем его ещё, ну и дата рождения как есть
    #     # метод get почему то помогает избежать ошибку, если неправильный Токен, то есть запрашивать
    #     # через гет информацию, а не ключ/значение из словаря
    #
    #     result = {'name': (info['first_name'] + ' ' + info[
    #         'last_name']) if 'first_name' in info and 'last_name' in info else None,
    #               'sex': info.get('sex'),
    #               'city': info.get('city')['title'] if info.get('city') is not None else None,
    #               'year': self._bdate_toyear(info.get('bdate')),
    #               'relation': info.get('relation')}
    #
    #     if 'city' not in result or 'sex' not in result or 'year' not in result or 'relation' not in result:
    #         if 'city' not in result:
    #             result['city'] = input('У вас города не хватает, введите пожалуйста: ')
    #         if 'sex' not in result:
    #             result['sex'] = input('Кто вы? (1 - девушка, 2 - мальчик): ')
    #         if 'year' not in result:
    #             result['year'] = input('Дата рождения ваша в формате день.месяц.год: ')
    #         if 'relation' not in result:
    #             result['relation'] = input('Как у вас с семейным положением?: ')
    #
    #
    #     return result

    def send_message(self, user_id, message):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        })

    def get_profile_info(self, user_id):
        try:
            info, = self.vkapi.method('users.get', {'user_id': user_id, 'fields': 'city,sex,bdate,relation'})
        except ApiError:
            info = {}
            print(f'У нас тут косяк со стороны АПИ')

        result = {
            'name': (info['first_name'] + ' ' + info[
                'last_name']) if 'first_name' in info and 'last_name' in info else None,
            'sex': info.get('sex'),
            'city': info.get('city')['title'] if info.get('city') is not None else None,
            'year': self._bdate_toyear(info.get('bdate')),
            'relation': info.get('relation')
        }

        if 'city' not in result:
            result['city'] = self.send_message('У вас города не хватает, введите пожалуйста: ')
        if 'sex' not in result:
            result['sex'] = self.send_message('Кто вы? (1 - Девушка, 2 - Молодой человек): ')
        if 'year' not in result:
            result['year'] = self.send_message('Дата рождения ваша в формате день.месяц.год: ')
        if 'relation' not in result:
            result['relation'] = self.send_message('Как у вас с семейным положением?: ')

        return result

        # ну и возвращаем результат который выше определён , чтобы была только нужная информация

    def search_worksheet(self, params, offset):
        try:
            users = self.vkapi.method('users.search',
                                      {
                                          'count': 500,
                                          'offset':offset,
                                          'hometown': params['city'],
                                          'sex': 1 if params['sex'] == 2 else 2,
                                          'has_photo': True,
                                          'age_from': params['year'] - 10,

                                          'age_to': params['year'] + 3,
                                      })


        except ApiError:
            users = []
            print(f'У нас тут косяк со стороны АПИ')

        result = [{
            'name': item['first_name'] + ' ' + item['last_name'],
            # if 'first_name' in item and 'last_name' in item else None,
            # 'sex': users.get('sex'),
            # 'city': users.get('city')['title']  if users.get('city') is not None else None,
            # 'year': self._bdate_toyear(users.get('bdate'))}
            'id': item['id']
        } for item in users['items'] if item['is_closed'] is False
        ]

        return result
        ''' а теперь добавим к этому делу метод как искафть фото'''



    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                      {'owner_id': id,
                                      'album_id': 'profile',
                                      'extended':1}
            # этот параметр показывает какая
            # дополнительная информация по фотографиям нам требуется. 1 - означает, что
            # необходима вся инфо о фото, такая кодировка в документации)
                                    )
        except ApiError:
            photos = {}
            print(f'Лажа с фотками')

        '''Создается списко чтобы не показываеть всю информацию о фото, а только нужную,
        в данном случае это количество лайков и соответсвенно функция будет возвращать
        result'''

        result = [ {'owner_id': item ['owner_id'], #это id профиля пользователя
                    'id':item ['id'], # а это id фотографии , он у каждой фото свой
                    'likes': item['likes']['count'],
                    'comments': item['comments']['count']
                    } for item in photos ['items']
                   ]
        ''' Сюда надо добавить сортировку по лайка и комментам от большого к меньшему'''
        # Сортируем все фотографии по количеству лайков в порядке убывания
        sorted_photos = sorted(result, key=lambda x: x['likes'], reverse=True)

        # Возвращаем три фотографии с наибольшим количеством лайков
        return sorted_photos[:3]
        # return result[:3]


    # получаем из словаря нормально Имя и Фамилию, но
    # но это нигде не выводится, нужно для дальyейшего обращения бота ко пользователю, пол просто
    # в виде кода остаётя, можно прикрутить мужчина женщина, но зачем, город по названию
    # При этом город, это словарь в словаре, распаковываем его ещё, ну и дата рождения как есть
    # метод get почему то помогает избежать ошибку, если неправильный Токен, то есть запрашивать
    # через гет информацию, а не ключ/значение из словаря


if __name__ == '__main__':
    user_id = 1456975  # this is my user_id from VK
    print ("фигня 1")
    tools = VkTools(acces_token)
    print("фигня 2")
    params = tools.get_profile_info(user_id)  # получили параметры пользователя
    print("фигня 3")
    worksheets = tools.search_worksheet(params,3)  # ищем с помощью воркщитов по входным параметра пользователя, полученным ранее
    print("фигня 4")
    worksheet= worksheets.pop() # принцип работы метода pop. Он берёт последний элемент из списка
    print("фигня 5")
    # добавляет его в переменную, но при этом удаляет его из списка.И список уже выводится
    # без неё

    photos= tools.get_photos(worksheet['id'])
    print("фигня 6")
    pprint(params)
    print("фигня 7")
    pprint(worksheets)
    print("фигня 8")
    pprint(worksheet)
    print("фигня 9")
    pprint(photos)
    print("фигня 10")

    print (worksheet['id'])
