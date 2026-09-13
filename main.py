# Создание экземпляра класса для работы с API сайтов с самолетами
from src import aeroplane, json_saver
from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.flight_manager import FlightManager
from src.json_saver import JSONSaver


# --------------------------------------------
# Функционал для тестирования добавления и удаления данных в файл JSON
# --------------------------------------------

# plane1 = Aeroplane("test1", "test", "test", True, 0.0, 0.0)
# plane2 = Aeroplane("test2", "test", "test", True, 0.0, 0.0)

# saver = JSONSaver()
# saver.add_aeroplane(plane1)
# saver.add_aeroplane(plane2)
# print(saver.delete_aeroplane("test2"))
# --------------------------------------------




# --------------------------------------------
# Функция для взаимодействия с пользователем
# --------------------------------------------
def user_interaction():
    # 1. =================
    aeroplanes = []
    country = ""

    while not aeroplanes:
        country = input("\nВведите название страны (на англ.) для обновления данных:\n>>> ")

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
                    # print(f"Данные загружены из файла. Всего записей: {len(aeroplanes)}")
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
    Получены данные по рейсам в воздушном пространстве страны: < {country.upper()} > \n
    Количество записей - {len(aeroplanes)}
    """)


    # 1. =================
    # создаём экземпляр класса для работы со списком самолётовых объектов
    flight_manager = FlightManager(aeroplanes)

    # 2. =================
    reg_country = input("Введите названия стран (через пробел) для фильтрации по стране регистрации \n('Enter' - пропустить):\n>>> ").split()
    flight_manager.filter_by_reg_country(reg_country)

    # 3. =================
    altitude_range = input("Введите диапазон высот полета \n(пример: 100000 - 150000. 'Enter' - пропустить):\n>>> ") # Пример: 100000 - 150000
    flight_manager.filter_by_altitude(altitude_range)

    # 4. =================
    sort_altitude = input("Сортировать самолёты по высоте?\n('y' - да. 'Enter' - пропустить):\n>>>")
    flight_manager.sort_aeroplanes_by_altitude(sort_altitude)

    # 5. =================
    top_n = input("Введите количество самолетов для вывода в топ N \n('Enter' - пропустить):\n>>> ")
    flight_manager.get_top_aeroplanes(top_n)

    # принтуем итоговый набор рейсов
    for flight in flight_manager.filtered_aeroplanes:
        print(flight)


if __name__ == "__main__":
    while True:
        user_interaction()
