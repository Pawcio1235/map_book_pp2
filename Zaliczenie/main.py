from bs4 import BeautifulSoup
import requests, folium, webbrowser, os, re

restaurants = [
    {"name": "Epoka", "city": "Warszawa", "guests": [{"name": "Mateusz Nowak", "city": ["Gdańsk"], "table": ["2"]}, {"name": "Anna Kowalska", "table": ["1"]}], "workers": [{"name": "Mateusz Kowalski", "city": ["Wałbrzych"]}]},
    {"name": "Marilor", "city": "Zakopane", "guests": [{"name": "Jan Nowak", "table": ["6"]}, {"name": "Maria Wiśniewska", "table": ["1"]}], "workers": [{"name": "Oliwier Nowacki", "city": ["Łódź"]}]},
    {"name": "Bulaj", "city": "Sopot", "guests": [{"name": "Kacper Nowak", "city": ["Gdańsk"], "table": ["3"]}, {"name": "Piotr Zieliński", "city": ["Zakopane"], "table": ["3"]}], "workers": [{"name": "Bartosz Szlachta", "city": ["Wrocław"]}]},
    {"name": "Mandragora", "city": "Lublin", "guests": [{"name": "Andrzej Nowak", "city": ["Lublin"], "table": ["2"]}, {"name": "Monika Lewandowska", "city": ["Lublin"], "table": ["2"]}], "workers": [{"name": "Jakub Piotrowski", "city": ["Sieradz"]}]},
    {"name": "Cafe Byfyj", "city": "Katowice", "guests": [{"name": "Jacek Nowak", "city": ["Katowice"], "table": ["3"]}, {"name": "Katarzyna Nowak", "city": ["Katowice"], "table": ["5"]}], "workers": [{"name": "Piotr Bartosik", "city": ["Poznań"]}]},
    {"name": "U Fukiera", "city": "Warszawa", "guests": [{"name": "Bartek Nowak", "city": ["Warszawa"], "table": ["1"]}, {"name": "Łukasz Nowicki", "city": ["Warszawa"], "table": ["7"]}], "workers": [{"name": "Tomasz Piotrowski", "city": ["Kielce"]}]}
]


#Funkcja do pokazania listy restauracji
def show_list(restaurants):
    print("Oto obecna lista restauracji: ")
    for restaurant in restaurants:
        print(f"{restaurant['name']}, {restaurant['city']}")

#Funkcja do dodania restauracji
def add_restaurant(restaurants):
    restaurant_name = input("Podaj nazwę restauracji do dodania: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurants.append({"name": restaurant_name, "city": city_name, "guests": [], "workers": []})
    print(f"{restaurant_name} został dodany do listy")
    show_list(restaurants)

#Funkcja do usunięcia restauracji
def remove_restaurant(restaurants):
    restaurant_name = input("Podaj nazwę restauracji do usunięcia: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    removed = False

    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            restaurants.remove(restaurant)
            print(f"{restaurant_name}, {city_name} została usunięta z listy")
            removed = True
            break

    if not removed:
        print(f"Nie znaleziono restauracji {restaurant_name}, {city_name} na liście.")

    show_list(restaurants)

#Funkcja do aktualizacji restauracji
def update_restaurant(restaurants):
    restaurant_name = input("Podaj nazwę restauracji do aktualizacji: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            new_name = input(f"Podaj nową nazwę dla {restaurant_name} w {city_name}: ")
            new_city = input(f"Podaj nowe miasto dla {new_name}: ")
            restaurant['name'] = new_name
            restaurant['city'] = new_city
            restaurant_found = True
            print(f"Nazwa restauracji w {city_name} została zmieniona z {restaurant_name} na {new_name} w {new_city}")
            break
    if not restaurant_found:
        print(f"Nie znaleziono restauracji {restaurant_name} w {city_name}")
    show_list(restaurants)


#Funkcja do pokaznia gości
def show_guests(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, która ma pokazać listę gości: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            restaurant_found = True
            print(f"Lista gości dla {restaurant_name}, {city_name}:")
            for guest in restaurant['guests']:
                print(f" {guest['name']}")

        if not restaurant_found:
            print(f"{restaurant_name} nie znaleziono na liście")

#Funkcja do dodania gości
def add_guest(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, do której chcesz dodać gościa: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False

    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            guest_name = input(f"Podaj nazwę gościa do dodania do {restaurant_name} w {city_name}: ")
            city_guest_name = input("Podaj miasto, w którym mieszka gość: ")
            restaurant['guests'].append({"name": guest_name, "city": [city_guest_name], "table": []})
            print(f"{guest_name} został dodany do listy gości restauracji {restaurant_name} w {city_name}.")
            restaurant_found = True
            break

    if not restaurant_found:
        print(f"{restaurant_name} w {city_name} nie znaleziono na liście.")

#Funkcja do usunięcia gościa
def remove_guest(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, z której chcesz usunąć gościa: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            guest_name = input(f"Podaj nazwę gościa do usunięcia z {restaurant_name} w {city_name}: ")
            guests = [guest['name'] for guest in restaurant['guests']]
            if guest_name in guests:
                restaurant['guests'] = [guest for guest in restaurant['guests'] if guest['name'] != guest_name]
                print(f"{guest_name} został usunięty z listy gości restauracji {restaurant_name} w {city_name}")
            else:
                print(f"{guest_name} nie znaleziono na liście gości restauracji {restaurant_name} w {city_name}")
            restaurant_found = True
            break
    if not restaurant_found:
        print(f"{restaurant_name}, {city_name} nie znaleziono na liście")

#Funckja do aktualizacji gościa
def update_guest(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, w której chcesz zaktualizować nazwę gościa: ").strip()
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ").strip()
    restaurant_found = False

    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            restaurant_found = True
            old_guest_name = input(
                f"Podaj starą nazwę gościa do zaktualizowania w {restaurant_name} w {city_name}: ").strip()
            old_city_name = input("Podaj stare miasto, zamieszkania gościa: ").strip()
            guest_found = False

            for guest in restaurant['guests']:
                if guest['name'].lower() == old_guest_name.lower() and guest['city'][
                    0].lower() == old_city_name.lower():
                    new_guest_name = input(f"Podaj nową nazwę dla {old_guest_name}: ").strip()
                    new_city_name = input("Podaj nowe miasto, zamieszkania gościa: ").strip()

                    guest['name'] = new_guest_name
                    guest['city'] = [new_city_name]
                    print(
                        f"Nazwa gościa została zmieniona z {old_guest_name} na {new_guest_name} oraz miasto z {old_city_name} na {new_city_name} w {restaurant_name} w {city_name}.")
                    guest_found = True
                    break

            if not guest_found:
                print(
                    f"Gość o nazwie {old_guest_name} i mieście {old_city_name} nie został znaleziony w restauracji {restaurant_name} w {city_name}.")
            break

    if not restaurant_found:
        print(f"Restauracja {restaurant_name} w {city_name} nie została znaleziona na liście.")

#Funkcja do pokazania pracowników
def show_workers(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, do której chcesz dodać pracownika: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            print(f"Lista pracowników dla {restaurant_name}:")
            for worker in restaurant['workers']:
                print(f" - {worker['name']}")
            restaurant_found = True
            break
    if not restaurant_found:
        print("Nie znaleziono na liście")

#Funkcja do dodania pracownika restauracji
def add_workers(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, do której chcesz dodać gościa: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False

    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            worker_name = input(f"Podaj nazwę pracownika do dodania do {restaurant_name} w {city_name}: ")
            city_worker_name = input("Podaj miasto, w którym mieszka pracownik: ")
            restaurant['workers'].append({"name": worker_name, "city": [city_worker_name]})
            print(f"{worker_name} został dodany do listy gości restauracji {restaurant_name} w {city_name}.")
            restaurant_found = True
            break

    if not restaurant_found:
        print(f"{restaurant_name} w {city_name} nie znaleziono na liście.")


#Funkcja do usunięcia pracowika restauracji
def remove_workers(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, z której chcesz usunąć pracownika: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            worker_name = input(f"Podaj nazwę pracownika do usunięcia z {restaurant_name} w {city_name}: ")
            workers = [worker['name'] for worker in restaurant['workers']]
            if worker_name in workers:
                restaurant['workers'] = [worker for worker in restaurant['workers'] if worker['name'] != worker_name]
                print(f"{worker_name} został usunięty z listy pracowników restauracji {restaurant_name} w {city_name}")
            else:
                print(f"{worker_name} nie znaleziono na liście pracowników restauracji {restaurant_name} w {city_name}")
            restaurant_found = True
            break
    if not restaurant_found:
        print(f"{restaurant_name}, {city_name} nie znaleziono na liście")

#Funkcja do aktualizacji pracownika
def update_workers(restaurants):
    restaurant_name = input("Podaj nazwę restauracji, w której chcesz zaktualizować nazwę pracownika: ").strip()
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ").strip()
    restaurant_found = False

    for restaurant in restaurants:
        if restaurant['name'].lower() == restaurant_name.lower() and restaurant['city'].lower() == city_name.lower():
            restaurant_found = True
            old_worker_name = input(
                f"Podaj starą nazwę pracownika do zaktualizowania w {restaurant_name} w {city_name}: ").strip()
            old_city_name = input("Podaj stare miasto, zamieszkania pracownika: ").strip()
            worker_found = False

            for worker in restaurant['workers']:
                if worker['name'].lower() == old_worker_name.lower() and worker['city'][0].lower() == old_city_name.lower():
                    new_worker_name = input(f"Podaj nową nazwę dla {old_worker_name}: ").strip()
                    new_city_name = input("Podaj nowe miasto, zamieszkania pracownika: ").strip()

                    worker['name'] = new_worker_name
                    worker['city'] = [new_city_name]
                    print(
                        f"Nazwa gościa została zmieniona z {old_worker_name} na {new_worker_name} oraz miasto z {old_city_name} na {new_city_name} w {restaurant_name} w {city_name}.")
                    guest_found = True
                    break

            if not worker_found:
                print(
                    f"Pracownik o nazwie {old_worker_name} i mieście {old_city_name} nie został znaleziony w restauracji {restaurant_name} w {city_name}.")
            break

    if not restaurant_found:
        print(f"Restauracja {restaurant_name} w {city_name} nie została znaleziona na liście.")

#Funkcja do pokazania stolików w restauracji
def show_table(restaurants):
    restaurant_name = input("Podaj nazwę restauracji: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    guest_name = input("Podaj gościa, którego zarezerwowany stolik chcesz zobaczyć: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            for guest in restaurant['guests']:
                if guest_name == guest['name']:
                    for table in guest['table']:
                        print(f"Ten gość rezerwuje stolik nr {table}")
                    if len(guest['table']) == 0:
                        print("Ten gość nic nie rezerwuje")

#Funkcja do dodania stolika
def add_table(restaurants):
    restaurant_name = input("Podaj nazwę restauracji: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    guest_name = input("Podaj gościa, do którego chcesz dodać zarezerwowany stolik: ")
    table_name = input(f"Podaj numer stolika: ")
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            for guest in restaurant['guests']:
                if guest_name == guest['name']:
                    guest['table'].append(table_name)

#Funkcja do usunięcia stolika
def remove_table(restaurants):
    restaurant_name = input("Podaj nazwę restauracji: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    guest_name = input("Podaj gościa, któremu chcesz usunąć zarezerwowany stolik: ")
    table_name = input(f"Podaj numer stolika: ")
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            for guest in restaurant['guests']:
                if guest_name == guest['name']:
                    guest['table'].remove(table_name)

#Funkcja do aktualizacji stolika
def update_table(restaurants):
    restaurant_name = input("Podaj nazwę restauracji: ")
    city_name = input("Podaj miasto, w którym znajduje się restauracja: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == restaurant_name and restaurant['city'] == city_name:
            restaurant_found = True
            guest_name = input("Podaj gościa, któremu chcesz zaktualizować zarezerwowany stolik: ")
            guest_found = False
            for guest in restaurant['guests']:
                if guest_name == guest['name']:
                    guest_found = True
                    old_table_number = input("Podaj stary numer stolika: ")
                    new_table_number = input(f"Podaj nowy numer stolika: ")
                    index = guest['table'].index(old_table_number)
                    guest['table'][index] = new_table_number
                    print(f"Numer stolika został zmieniony z {old_table_number} na {new_table_number}")
                else:
                    print(f"Stolik nie został znaleziony na liście stolików gościa")
                    break

            if not guest_found:
                print(f"Gość {guest_name} nie został znaleziony na liście gości restauracji {restaurant_name}")
                break
    if not restaurant_found:
        print(f"Gość {restaurant_name} nie został znaleziony na liście")


#Funkcja do konwersji współrzędnych geograficznych
def dms_to_decimal(dms):
    # Extract degrees, minutes, and seconds from the DMS string
    parts = re.split('[°′″]', dms)
    degrees = float(parts[0])
    minutes = float(parts[1]) if parts[1] else 0
    seconds = float(parts[2]) if parts[2] else 0
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    return decimal

#Funkcja do wydobywania współrzędnych geograficznych
def get_cords(restaurants):
    name = input("Podaj nazwę restauracji, której lokalizację chcesz wyszukać: ")
    restaurant_found = False
    for restaurant in restaurants:
        if restaurant['name'] == name:
            adres_url = f'https://pl.wikipedia.org/wiki/{restaurant["city"]}'
            response = requests.get(adres_url)
            response_html = BeautifulSoup(response.text, 'html.parser')

            # Extract latitude and longitude in DMS format
            latitude_dms = response_html.select('.latitude')[0].text
            longitude_dms = response_html.select('.longitude')[0].text

            # Convert DMS to decimal
            latitude = dms_to_decimal(latitude_dms)
            longitude = dms_to_decimal(longitude_dms)

            print([latitude, longitude])
            restaurant_found = True
            # Call the function to display a map
            display_map(latitude, longitude, restaurant["city"])
            return latitude, longitude
    if not restaurant_found:
        print(f"{restaurant["city"]} nie znaleziono na liście")

#Funkcja do do wyświetlania mapy
def display_map(latitude, longitude, miasto):
    # Create a map centered at the given latitude and longitude
    map_ = folium.Map(location=[latitude, longitude], zoom_start=12)
    # Add a marker for the city center
    for restaurant in restaurants:
        folium.Marker([latitude, longitude], tooltip=restaurant["city"]).add_to(map_)
    # Save the map as an HTML file
    map_file = f"{miasto}_map.html"
    map_.save(map_file)
    # Open the map in the default web browser
    webbrowser.open('file://' + os.path.realpath(map_file))


#Funkcja do wyświetlana współrzędnych gościa
def get_cords_guest(restaurants):
    name = input("Podaj nazwę restauracji, której lokalizację gości chcesz wyszukać: ")
    restaurant_found = False
    guest_locations = []

    for restaurant in restaurants:
        if restaurant['name'].lower() == name.lower():
            restaurant_found = True
            for guest in restaurant['guests']:
                if 'city' not in guest or not guest['city']:
                    print(f"Gość {guest['name']} nie ma podanego miasta.")
                    continue

                adres_url = f'https://pl.wikipedia.org/wiki/{guest["city"][0]}'
                response = requests.get(adres_url)
                response_html = BeautifulSoup(response.text, 'html.parser')

                try:
                    latitude_dms = response_html.select('.latitude')[0].text
                    longitude_dms = response_html.select('.longitude')[0].text

                    # Convert DMS to decimal
                    latitude = dms_to_decimal(latitude_dms)
                    longitude = dms_to_decimal(longitude_dms)

                    guest_locations.append((guest["name"], guest["city"][0], latitude, longitude))
                    print(f"Koordynaty gościa {guest['name']}: [{latitude}, {longitude}]")
                except IndexError:
                    print(f"Koordynaty dla {guest['city'][0]} nie znalezione na Wikipedii.")
            break

    if restaurant_found and guest_locations:
        display_map_guests(guest_locations, name)
    elif not restaurant_found:
        print(f"Restauracja {name} nie została znaleziona na liście.")

#Funkcja do wyświetlenia mapy gościa
def display_map_guests(guest_locations, restaurant_name):
    if guest_locations:
        avg_latitude = sum([loc[2] for loc in guest_locations]) / len(guest_locations)
        avg_longitude = sum([loc[3] for loc in guest_locations]) / len(guest_locations)
    else:
        avg_latitude = 0
        avg_longitude = 0

    map_ = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=5)

    # Add markers for each guest
    for name, city, latitude, longitude in guest_locations:
        folium.Marker(
            [latitude, longitude],
            tooltip=f"{name} ({city})",
            popup=f"{name} ({city})"
        ).add_to(map_)

    # Save the map as an HTML file
    map_file = f"{restaurant_name}_guest_locations_map.html"
    map_.save(map_file)
    # Open the map in the default web browser
    webbrowser.open('file://' + os.path.realpath(map_file))


#Funkcja do określenia współrzędnych pracowników restauracji
def get_cords_workers(restaurants):
    name = input("Podaj nazwę restauracji, której lokalizację pracowników chcesz wyszukać: ")
    restaurant_found = False
    worker_locations = []

    for restaurant in restaurants:
        if restaurant['name'].lower() == name.lower():
            restaurant_found = True
            for worker in restaurant['workers']:
                if 'city' not in worker or not worker['city']:
                    print(f"Gość {worker['name']} nie ma podanego miasta.")
                    continue

                adres_url = f'https://pl.wikipedia.org/wiki/{worker["city"][0]}'
                response = requests.get(adres_url)
                response_html = BeautifulSoup(response.text, 'html.parser')

                try:
                    latitude_dms = response_html.select('.latitude')[0].text
                    longitude_dms = response_html.select('.longitude')[0].text

                    # Convert DMS to decimal
                    latitude = dms_to_decimal(latitude_dms)
                    longitude = dms_to_decimal(longitude_dms)

                    worker_locations.append((worker["name"], worker["city"][0], latitude, longitude))
                    print(f"Koordynaty gościa {worker['name']}: [{latitude}, {longitude}]")
                except IndexError:
                    print(f"Koordynaty dla {worker['city'][0]} nie znalezione na Wikipedii.")
            break

    if restaurant_found and worker_locations:
        display_map_workers(worker_locations, name)
    elif not restaurant_found:
        print(f"Restauracja {name} nie została znaleziona na liście.")

#Funkcja do wyświetlania mapy pracowników
def display_map_workers(worker_locations, restaurant_name):
    if worker_locations:
        avg_latitude = sum([loc[2] for loc in worker_locations]) / len(worker_locations)
        avg_longitude = sum([loc[3] for loc in worker_locations]) / len(worker_locations)
    else:
        avg_latitude = 0
        avg_longitude = 0

    map_ = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=5)

    # Add markers for each guest
    for name, city, latitude, longitude in worker_locations:
        folium.Marker(
            [latitude, longitude],
            tooltip=f"{name} ({city})",
            popup=f"{name} ({city})"
        ).add_to(map_)

    # Save the map as an HTML file
    map_file = f"{restaurant_name}_worker_locations_map.html"
    map_.save(map_file)
    # Open the map in the default web browser
    webbrowser.open('file://' + os.path.realpath(map_file))

correct_password = "Paweł"
logged_in = False

while not logged_in:
    password = input('Enter your password: ')
    if password == correct_password:
        print("Zalogowany")
        logged_in = True
    else:
        print("Niepoprawne hasło")

if logged_in:
    if __name__ == '__main__':
        print("Witaj!")
        while True:
            print("Menu:")
            print("0. Zakończ program")
            print("1. Zarządzaj restauracjami")
            print("2. Zarządzaj gośćmi restauracji")
            print("3. Zarządzaj pracownikami restauracji")
            menu_option = input("Wybierz dostępną funkcję z menu: ")
            if menu_option == '0':
                break
            elif menu_option == '1':
                while True:
                    print("0. Powrót do głównego menu")
                    print("1. Wyświetl obecną listę restauracji")
                    print("2. Dodaj restaurację do listy")
                    print("3. Usuń restaurację z listy")
                    print("4. Aktualizuj nazwę restaurajcji")
                    print("5. Wyświetl współrzędne i mapę restauracji")
                    dzialanie = input("Jakie działanie chcesz podjąć?: ")
                    if dzialanie == '0':
                        break
                    elif dzialanie == '1':
                        show_list(restaurants)
                    elif dzialanie == '2':
                        add_restaurant(restaurants)
                    elif dzialanie == '3':
                        remove_restaurant(restaurants)
                    elif dzialanie == '4':
                        update_restaurant(restaurants)
                    elif dzialanie == '5':
                        get_cords(restaurants)
                    elif dzialanie == '6':
                        display_map(restaurants)
                    else:
                        print("Nieprawidłowa opcja, spróbuj ponownie.")
            elif menu_option == '2':
                while True:
                    print("0. Powrót do głównego menu")
                    print("1. Wyświetl listę gości danej restauracji")
                    print("2. Dodaj gościa do restauracji")
                    print("3. Usuń gościa z restauracji")
                    print("4. Aktualizuj nazwę restauracji")
                    print("5. Wyświetl stoliki gościa")
                    print("6. Dodaj stolik do gościa")
                    print("7. Usuń stolik gościa")
                    print("8. Aktualizuj stolik gościa")
                    print("9. Wyświetl współrzędne miejsca zamieszkania gości")
                    dzialanie = input("Jakie działanie chcesz podjąć?: ")
                    if dzialanie == '0':
                        break
                    elif dzialanie == '1':
                        show_guests(restaurants)
                    elif dzialanie == '2':
                        add_guest(restaurants)
                    elif dzialanie == '3':
                        remove_guest(restaurants)
                    elif dzialanie == '4':
                        update_guest(restaurants)
                    elif dzialanie == '5':
                        show_table(restaurants)
                    elif dzialanie == '6':
                        add_table(restaurants)
                    elif dzialanie == '7':
                        remove_table(restaurants)
                    elif dzialanie == '8':
                        update_table(restaurants)
                    elif dzialanie == '9':
                        get_cords_guest(restaurants)
                    else:
                        print("Nieprawidłowa opcja, spróbuj ponownie.")
            elif menu_option == '3':
                while True:
                    print("0. Powrót do głównego menu")
                    print("1. Wyświetl obecną listę pracowników danej restauracji")
                    print("2. Dodaj pracownika do listy")
                    print("3. Usuń pracownika z listy")
                    print("4. Aktualizuj pracownika na liście")
                    print("5. Wyświetl lokalizacje miejsca zamieszkania pracowników")
                    dzialanie = input("Jakie działanie chcesz podjąć?: ")
                    if dzialanie == '0':
                        break
                    elif dzialanie == '1':
                        show_workers(restaurants)
                    elif dzialanie == '2':
                        add_workers(restaurants)
                    elif dzialanie == '3':
                        remove_workers(restaurants)
                    elif dzialanie == '4':
                        update_workers(restaurants)
                    elif dzialanie == '5':
                        get_cords_workers(restaurants)
                    else:
                        print("Nieprawidłowa opcja, spróbuj ponownie.")