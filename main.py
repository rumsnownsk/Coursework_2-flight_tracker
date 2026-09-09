# Создание экземпляра класса для работы с API сайтов с самолетами
from src import aeroplane, json_saver
from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.json_saver import JSONSaver
from src.helpers import print_json

# api = AeroplanesAPI()
#
# # Получение информации о самолетах с opensky-network.org
# raw_aeroplanes = api.get_aeroplanes("Spain")
#
# # Преобразование набора данных в список объектов
# aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)
# #
# for item in aeroplanes:
#     print(item)

# # Пример работы контструктора класса с одним самолетом
# aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
#
# Сохранение информации в файл
# json_saver = JSONSaver()
# json_saver.add_aeroplane(vacancy)
# json_saver.delete_aeroplane(vacancy)

# # Функция для взаимодействия с пользователем
def user_interaction():
    # 1. =================
    country = input("Введите название страны (на англ.):\n>>> ")

    api = AeroplanesAPI()
    raw_data = api.get_aeroplanes(country)

    aeroplanes = Aeroplane.cast_to_object_list(raw_data)

    json_saver = JSONSaver()
    json_saver.write_to_file(raw_data)

    print(f"""
    Получены данные по рейсам в воздушном пространстве страны: < {country} >
    Количество записей - {len(aeroplanes)} 
    Данные сохранены в файл
    """)

    # 2. =================
    # top_n = int(input("Введите количество самолетов для вывода в топ N: "))

    # 3. =================
    reg_country = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    #
    # # 4. =================
    # altitude_range = input("Введите диапазон высот полета: ") # Пример: 100000 - 150000

    # Создание объекта как экземпляра класса Aeroplane
    aeroplane = Aeroplane()

    filtered_aeroplanes = aeroplane.filter_aeroplanes_by_reg_country(reg_country)
    #
    # ranged_aeroplanes = get_aeroplanes_by_altitude(aeroplanes, altitude_range)
    #
    # sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    # top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    # print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
