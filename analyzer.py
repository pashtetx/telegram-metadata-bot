from exifread import process_file
from exifread.classes import IfdTag
from fake_useragent import UserAgent
from geopy import Nominatim
from typing import Dict
from utils import parse_coordinate

import datetime
import pytz

geolocator = Nominatim(user_agent=UserAgent(platforms=["pc"]).chrome)

def read_image_make(image: Dict[str, IfdTag]) -> str:
    model = image.get("Image Model")
    if not model:
        return "Недостаточно данных"
    return str(model)

def read_gps_location(image: Dict[str, IfdTag], language="ru") -> str:
    gps_latidute = image.get("GPS GPSLatitude")
    gps_langitude = image.get("GPS GPSLongitude")
    if not gps_latidute or not gps_langitude:
        return "Недостаточно данных"
    latitude = parse_coordinate(gps_latidute.values)
    longidute = parse_coordinate(gps_langitude.values)
    return geolocator.reverse(f'{latitude}, {longidute}', language=language)

def read_datetime(image: Dict[str, IfdTag]) -> str:
    offset = image.get("EXIF OffsetTimeOriginal")
    create_at = image.get("Image DateTime")
    if not create_at or not offset:
        return "Недостаточно данных"
    create_at = datetime.datetime.strptime(create_at.values + offset.values, "%Y:%m:%d %H:%M:%S%z")
    create_at = create_at.astimezone(tz=pytz.timezone("Europe/Kiev"))
    return create_at.strftime("%Y.%m.%d, %H:%M:%S")

options = {
    0:None,
    "📱 Модель":read_image_make,
    "📍 Локация":read_gps_location,
    "⏰ Дата создания (по киеву)":read_datetime,
    1:None,
}

def parse_image(image: bytes, filename: str = None) -> set:
    response = list()
    exifdata = process_file(image)
    if filename:
        response.append(f"📷 <b>Фото - {filename}</b>")
    for name, reader in options.items():
        if not reader:
            response.append('')
        else:
            response.append(f"{name}: {reader(exifdata)}")
    response.append(f"<b><a href=\"https://t.me/geolocation_photo_bot\">Узнать геолокацию по фотографии</a></b>")
    return response
