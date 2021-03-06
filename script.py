import db
import geopy
from geopy.distance import distance
import pandas as pd


def form_answer():
    answer = {}
    mas1 = []
    mas2 = []
    mas3 = []
    dct_stations = db.get_dict_stations()
    dct_apartments = db.get_dict_apartments()
    for key_apartment, value_apartment in dct_apartments.items():
        start = geopy.Point(value_apartment[0], value_apartment[1])
        d = geopy.distance.distance(kilometers=1.2)
        north = d.destination(point=start, bearing=0)  # Сдвиг на 1.2 км на север
        east = d.destination(point=start, bearing=90)  # Сдвиг на 1.2 км на восток
        south = d.destination(point=start, bearing=180)  # Сдвиг на 1.2 км на юг
        west = d.destination(point=start, bearing=270)  # Сдвиг на 1.2 км на запад
        north_coord = north[0]  # Получение самой северной долготы для квадрата
        east_coord = east[1]  # Получение самой восточной широты для квадрата
        south_coord = south[0]  # Получение самой южной долготы для квадрата
        west_coord = west[1]  # Получение самой западной широты для квадрата
        for key_station, value_station in dct_stations.items():
            longitude = value_station[0]
            latitude = value_station[1]

            # Проверка того, что остановка лежит в квадрате 2.4 км * 2.4 км
            if south_coord < longitude < north_coord and west_coord < latitude < east_coord:
                dist = distance((longitude, latitude), start).m
                if dist <= 1000:
                    mas1.append(key_apartment)
                    mas2.append(key_station)
                    mas3.append(dist)
    x = zip(mas1, mas2, mas3)
    xs = sorted(x, key=lambda tup: (tup[0], tup[2]))  # Сортировка по удалённости, а затем по названию ЖК
    answer['Название ЖК'] = [x[0] for x in xs]
    answer['Название Остановки'] = [x[1] for x in xs]
    answer['Расстояние до остановки'] = [x[2] for x in xs]
    z = pd.DataFrame(answer)
    z.to_excel("final_table.xlsx", index=False)


