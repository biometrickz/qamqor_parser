import subprocess

import undetected_chromedriver as uc
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from env_settings import settings

from config import (
    urls,
    default_photo_url
)
from service import *

client = MongoClient(
    host=settings.model_dump().get('mongo_host'),
    port=settings.model_dump().get('mongo_port'),
)
db_name = settings.model_dump().get('mongo_db')
client.drop_database(db_name)
db = client[db_name]

options = uc.ChromeOptions()
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")
# options.add_argument( "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
# Chrome/87.0.4280.88 Safari/537.36") options.add_argument('--disable-dev-shm-usage')

chrome_driver = uc.Chrome(options=options, version_main=122, enable_cdp_events=True, headless=True)
chrome_driver.maximize_window()
wait = WebDriverWait(chrome_driver, timeout=60)


for url_shortcut in urls.keys():
    chrome_driver.get(urls[url_shortcut])

    wait.until(
        ec.visibility_of_element_located(
            (By.CLASS_NAME, 'nav-item')
        ))
    select_language('RU', chrome_driver)
    while True:
        wait.until(
            ec.visibility_of_element_located(
                (By.CLASS_NAME, 'page-link')
            ))
        paginator_button = get_paginator_button(chrome_driver)
        is_button_clickable = get_is_paginator_button_clickable(chrome_driver)

        wait.until(
            ec.visibility_of_element_located(
                (By.CLASS_NAME, 'list-group-item')
            ))
        persons_data = get_list_of_person_data(chrome_driver)

        for person_data in persons_data:
            # person photo
            photo_url = get_person_photo_url(person_data)
            if photo_url == default_photo_url:
                continue

            # person main data
            name = get_person_name(person_data)
            age = get_person_age(person_data)
            days_in_wanted = get_number_of_days_in_wanted(person_data)

            # person additional data
            birthdate = get_birthdate(person_data)
            gender = get_gender(person_data)
            nationality = get_nationality(person_data)
            ethnicity = get_ethnicity(person_data)

            # case data
            case_description = get_case_description(person_data)
            case_initiator = get_case_initiator(person_data)
            case_executor = get_case_executor(person_data)

            case = {
                'name': name,
                'age': age,
                'photo_url': photo_url,
                'birthdate': birthdate,
                'gender': gender,
                'nationality': nationality,
                'ethnicity': ethnicity,
                'number_of_days_in_wanted': days_in_wanted,
                'case_description': case_description,
                'case_initiator': case_initiator,
                'case_executor': case_executor,
            }

            if url_shortcut == 'children' or url_shortcut == 'missing':
                disappearance_conditions = get_disappearance_conditions(person_data)
                case['disappearance_conditions'] = disappearance_conditions

            db[url_shortcut].insert_one(case)
        if is_button_clickable:
            paginator_button.click()
        else:
            break

chrome_driver.quit()
subprocess.run(['mongodump', '--db', db_name])
client.close()
