# Создание экземпляра класса для работы с API сайтов с самолетами
from src import aeroplane, json_saver
from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.flight_manager import FlightManager
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
    aeroplanes = []
    country = ""

    while not aeroplanes:
        country = input("Введите название страны (на англ.):\n>>> ")

        if not country:
            print("Страна не введена. Попробуем взять данные из сохранённого файла.\n")
            # если человек нажал Enter и поле country пустое
            saver = JSONSaver()

            # загружаем старые сырые данные из файла data.json
            raw = saver.read_from_file()

            if raw and "states" in raw:
                states = raw["states"]

                aeroplanes = Aeroplane.cast_to_object_list(states)
                if aeroplanes:
                    country = raw.get("country")
                    print(f"Данные загружены из файла. Всего записей: {len(aeroplanes)}")
                    break
                else:
                    print("В файле нет данных. Введите название страны.")
                    continue
            else:
                print("Файл не найден или пуст. Введите название страны.")
                continue

        api = AeroplanesAPI()
        raw_data = api.get_aeroplanes(country)
        if not raw_data:
            print(f"По стране <{country}> ничего не найдено. Попробуйте ещё раз.")
            print("="*40 + "\n")
            continue

        raw_data = {"country":country, **raw_data}

        saver = JSONSaver()
        saver.data = raw_data
        saver.write_to_file(raw_data)

        if "states" in raw_data:
            try:
                states = raw_data["states"]
            except KeyError:
                raise KeyError("Отсутствуют данные по ключу <states>")

            aeroplanes = Aeroplane.cast_to_object_list(states)

        if not aeroplanes:
            print(f"По стране <{country}> нет данных о самолётах.")
            continue


    print(f"""
    Получены данные по рейсам в воздушном пространстве страны: < {country.upper()} >
    Количество записей - {len(aeroplanes)}
    """)


    # создаём экземпляр класса для работы со списком самолётовых объектов
    flight_manager = FlightManager(aeroplanes)
    # 2. =================
    top_n = input("Введите количество самолетов для вывода в топ N:\n>>> ")


    # 3. =================
    reg_country = input("Введите названия стран (через пробел) для фильтрации по стране регистрации:\n>>> ").split()
    flight_manager.filter_by_reg_country(reg_country)

    # 4. =================
    altitude_range = input("Введите диапазон высот полета (пример: 100000 - 150000):\n>>> ") # Пример: 100000 - 150000
    flight_manager.filter_by_altitude(altitude_range)

    flight_manager.sort_aeroplanes_by_altitude()

    flight_manager.get_top_aeroplanes(top_n)

    for el in flight_manager.filtered_aeroplanes:
        print(el)


    # !!!!!!! Метод готов и работает
    # filtered_aeroplanes = aeroplane_obj.get_aeroplanes_by_reg_country(reg_country)
    # print(f"""
    # Рейсы по странам-регистраторам: < {print(filtered_aeroplanes)} >
    # """)

    # ranged_aeroplanes = aeroplane.get_aeroplanes_by_altitude(altitude_range)
    #
    # sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    # top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    # print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
