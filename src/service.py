from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver


def select_language(lang: str, driver: ChromeWebDriver) -> None:
    if lang == 'KZ':
        button = driver.find_elements(By.CLASS_NAME, 'nav-item')[-3]
    elif lang == 'RU':
        button = driver.find_elements(By.CLASS_NAME, 'nav-item')[-2]
    elif lang == 'EN':
        button = driver.find_elements(By.CLASS_NAME, 'nav-item')[-1]
    else:
        print('Invalid language')
        return
    button.click()


def get_list_of_person_data(driver: ChromeWebDriver) -> List[WebElement]:
    return driver.find_elements(By.CLASS_NAME, 'list-group-item')


def get_person_photo_url(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH,
        './/div[1]/div[1]/div[1]/img',
    ).get_attribute('src')


def get_person_name(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH,
        './/div[1]/div[2]/div[1]/div[1]/h5',
    ).text


def get_person_age(person_data_web_element: WebElement) -> int:
    return int(person_data_web_element.find_element(
        By.XPATH,
        './/div[1]/div[1]/div[1]/div[1]',
    ).text.split()[0])


def get_number_of_days_in_wanted(person_data_web_element: WebElement) -> int:
    number_of_days_in_wanted = None
    words = person_data_web_element.find_element(
        By.XPATH,
        './/div[1]/div[2]/div[1]/div[2]',
    ).text.split()
    for word in words:
        try:
            number_of_days_in_wanted = int(word)
        except ValueError:
            continue
    return number_of_days_in_wanted


def get_birthdate(person_data_web_element: WebElement) -> str:
    return (person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[1]'
    )
            .text
            .split(',')[0]
            .split(':')[-1]
            .strip())


def get_gender(person_data_web_element: WebElement) -> str:
    return (person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[1]'
    )
            .text
            .split(',')[1]
            .split(':')[-1]
            .strip())


def get_nationality(person_data_web_element: WebElement) -> str:
    return (person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[1]'
    )
            .text
            .split(',')[2]
            .split(':')[-1]
            .strip())


def get_ethnicity(person_data_web_element: WebElement) -> str:
    return (person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[1]'
    )
            .text
            .split(',')[3]
            .split(':')[-1]
            .strip())


def get_case_description(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[2]'
    ).text


def get_case_initiator(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[3]'
    ).text


def get_case_executor(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[4]'
    ).text.split(':')[-1].strip()


def get_disappearance_conditions(person_data_web_element: WebElement) -> str:
    return person_data_web_element.find_element(
        By.XPATH, './/div[1]/div[2]/div[2]/div[5]'
    ).text.split(':')[-1].strip()


def get_paginator_button(driver: ChromeWebDriver) -> WebElement:
    return driver.find_elements(By.CLASS_NAME, 'page-link')[-2]


def get_is_paginator_button_clickable(driver: ChromeWebDriver) -> bool:
    class_attribute = driver.find_elements(
        By.XPATH,
        '/html/body/div[1]/div/div[3]/div/ul[1]/li'
    )[-2].get_attribute('class')
    if class_attribute is not None:
        return 'disabled' not in class_attribute.split()
    return False
