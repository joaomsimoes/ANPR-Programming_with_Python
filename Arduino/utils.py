import random
from db_conn import query
from datetime import datetime
import requests
import cv2


def random_place():
    # Verify empty spaces, if there is a free parking place
    # it chooses randomly
    free_place = [i[0] for i in query('free_place', [])]

    return random.choice(free_place)


def plate_is_parked(plate=None):
    # Verify if car is parked, returns empty list if not parked
    return query('verify_car_is_parked', [plate])


def car_entry(plate=None, place=None):
    # Ocupy an empty car spot
    query('ocupy_place', [plate, place])

    # Register entry time
    hr_entry = datetime.now()
    query('entry', [plate, hr_entry])

    print(f"{plate} - Entry time: {hr_entry}")


def car_exits(plate=None):
    # Exist time
    hr_exits = datetime.now()

    # Query the entry time
    hr_entry = query('entry_time', [plate])

    # Register the car exit
    query('exit_park', [plate, hr_exits])

    # Make the spot again available
    query('empty_parking_place', [plate])

    # Calculate the total time in minutes and cost
    total_time = hr_exits - hr_entry[0][0]
    total_minutes = int(total_time.total_seconds() / 60)
    total_cost = round(float(0.4 * total_minutes), 2)

    values_registo = [plate, total_minutes, total_cost]
    query('payment', values_registo)

    print(f'{plate} - Exit time: {hr_exits}\n'
          f'Total Time: {total_minutes} minutes\n'
          f'Total Cost: {total_cost}\n'
          f'Have a good trip!')


def api(image='plate.jpg'):
    # Send the image with API
    url = "http://localhost:8000/files"
    files = {'image': open(image, 'rb')}

    return requests.post(url, files=files)


def park(prediction=None, frame=None):
    # Saves the image to send it trough the API service
    cv2.imwrite('plate.jpg', frame)
    plate = api()
    plate = plate.json()

    if plate is not None:
        try:
            if plate_is_parked(plate=plate) == 1:
                car_exits(plate=plate)
            else:
                if random_place() == 0:
                    print('Everything is ocupied')
                else:
                    car_entry(plate=plate, place=random_place())
        except:
            print('Could not read plate')
    else:
        pass
