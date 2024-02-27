from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.remote.webelement import WebElement
import re

import time


def set_driver(db_link):
    driver = webdriver.Chrome()
    driver.get(db_link)
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.implicitly_wait(1)
    return driver


def get_region(driver):
    page_region = driver.page_source
    soup = BeautifulSoup(page_region, features="lxml")
    all_regions = soup.find_all("a", {"class": "subhead"})

    region = all_regions[0].text.replace("'", "").replace('"', "").strip()
    return region


def click_on_element(driver, element_type, element, comment, MODE='presentation'):
    print(comment)
    try:
        driver.implicitly_wait(1.5)
        if element_type == "xpath":
            driver.find_element(By.XPATH, element).click()
        elif element_type == "class":
            driver.find_element(By.CLASS_NAME, element).click()
    #     time.sleep(0.6)
    except Exception as e:
        print(f"in part {comment}:")
        print(f"Exception {e[:100]}")
    if MODE == "presentation":
        time.sleep(5)


def click_on_xpath(driver, xpath, comment=None):
    click_on_element(driver, "xpath", xpath, comment)


def click_on_class(driver, class_name, comment=None):
    click_on_element(driver, "class", class_name, comment)


def accept_alert(driver):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
    #         print("alert accepted")
    except TimeoutException:
        #         print("no alert")
        pass


def get_id(driver, tag, element="a", attr="class", attr_name="subhead"):
    ps = driver.page_source
    soup = BeautifulSoup(ps, features="lxml")
    all_btn = soup.find_all(element, {attr: attr_name})
    tag = [x for x in all_btn if tag in x.text][0]
    #     print(tag.attrs["id"])
    return tag.attrs["id"]


def clicker_naselenie(driver):
    id_nas = get_id(driver, "Население")
    click_on_xpath(driver, f'//*[@id="{id_nas}"]', "Клик на папку <<Население>>")
    el = driver.find_element(By.XPATH, f'//*[@id="{id_nas}v"]')
    table_context = el.text.split('\n')
    context = 'городского населения по полу'
    context = [x for x in table_context if context in x][0]
    id_city = table_context.index(context) + 1
    click_on_xpath(driver,
                   f'//*[@id="{id_nas}v"]/table[{id_city}]/tbody/tr/td[1]/span/img',
                   "Городское население")
    click_on_class(driver, "BtnStyle", 'Кнопка "Далее"')


def clicker_year(driver):
    el = driver.find_element(By.XPATH,
                             f'/html/body/div[2]/div/font/center/table/tbody/tr[1]/td/form/table[6]/tbody/tr[2]/td[3]/select')
    select_year = el.text.split('\n')
    year = '2023'
    year = [x for x in select_year if year in x][0]
    id_year = select_year.index(year) + 1
    click_on_xpath(driver,
                   f'/html/body/div[2]/div/font/center/table/tbody/tr[1]/td/form/table[6]/tbody/tr[2]/td[3]/select/option[{id_year}]',
                   "Выбрать 2023 год")


def get_xpath(el: WebElement, xpath: str = ""):
    if el.tag_name == "html":
        return "/html" + xpath

    tmp = el.tag_name
    parent = el.find_element("xpath", "..")
    children = parent.find_elements("xpath", "*")
    index = 0
    for child in children:
        if child.tag_name == el.tag_name:
            index += 1
            if child == el:
                elem_index = index
    if index > 1:
        tmp += f"[{elem_index}]"
    tmp = "/" + tmp + xpath
    return get_xpath(el=parent, xpath=tmp)


def get_web_element(driver, tag, class_name="SelectWord"):
    elements_class = driver.find_elements(By.CLASS_NAME, class_name)
    web_element = [x for x in elements_class if tag in x.text][0]
    return web_element


def clicker_year(driver):
    el = driver.find_element(By.XPATH,
                             f'/html/body/div[2]/div/font/center/table/tbody/tr[1]/td/form/table[6]/tbody/tr[2]/td[3]/select')
    select_year = el.text.split('\n')
    year = '2023'
    year = [x for x in select_year if year in x][0]
    id_year = select_year.index(year) + 1
    click_on_xpath(driver,
                   f'/html/body/div[2]/div/font/center/table/tbody/tr[1]/td/form/table[6]/tbody/tr[2]/td[3]/select/option[{id_year}]',
                   f"Выбрать {year} год")


def click_param_by_tag(driver, tag, ):
    el = get_web_element(driver, tag, "SelectWord")
    parent = el.find_element("xpath", "..")
    td_name = "td"
    while "tr" not in parent.tag_name:
        td_name = get_xpath(parent).split('/')[-1]
        parent = parent.find_element("xpath", "..")
    if tag == "Годы":
        txt = parent.text
        ind = txt.find("Выберите Годы")
        year_num = re.findall(r'\d+', txt[ind:ind + 25])[0]
        clickable_path = get_xpath(parent)[:-2] + f'2]/{td_name}/select/option[{year_num}]'
    else:
        clickable_path = get_xpath(parent)[:-2] + f'2]/{td_name}/input'
    click_on_xpath(driver, clickable_path, tag)


def clicker_manual(driver):
    click_on_xpath(driver,
                   '//*[@id="Manual"]',
                   "Выбрать <<Ручное маркетирование>>")
    click_on_xpath(driver,
                   '//*[@id="form2"]/table/tbody/tr[1]/td[1]/table/tbody/tr[4]/td[3]/input',
                   "Засунуть муниципалитеты в шапку (1)")
    click_on_xpath(driver,
                   '//*[@id="form2"]/table/tbody/tr[1]/td[1]/table/tbody/tr[6]/td[3]/input',
                   "Засунуть муниципалитеты в шапку (2)")
    click_on_xpath(driver,
                   '//*[@id="form2"]/table/tbody/tr[1]/td[1]/table/tbody/tr[8]/td[3]/input',
                   "Засунуть Структуру населения в шапку (2)")


def show_table(driver):
    click_on_xpath(driver,
                   '//body',
                   "Нажать на свободное место")
    click_on_xpath(driver,
                   '/html/body/div[2]/div/font/center/table/tbody/tr[2]/td[1]/form/table/tbody/tr/td/input[1]',
                   "Кнопка <<Показать таблицу>>")
