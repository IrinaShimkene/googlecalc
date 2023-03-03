import time
import allure
import keyboard
import pytest
import keyword
from data import *
from conftest import open_site
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

# 1. Тест, что на новой странице окно калькулятора не заполнено числами, отличными от нуля
@allure.feature('Общие базовые проверки')
@allure.story('При первичном открытии окно калькулятора пустое (заполнено нулем)')
def test_just_zero_in_new_window():
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))) # ожидание подгрузки элемента
    assert pytest.driver.find_element(By.ID, "cwos").text =='0' # находим содержание текста по локатору

# 2. На странице есть кнопка деления, обозначенная символом '÷'. Что роль элемента в атрибуте прописана как "кнопка"
@allure.feature('Общие базовые проверки')
@allure.story('Кнопка деления содержится на странице')
@allure.severity('blocker')
def test_division_button_is_on_page():
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'÷')]")))
    assert pytest.driver.find_element(By.XPATH, "//div[contains(text(),'÷')]") # находим содержание текста по локатору
    assert pytest.driver.find_element(By.XPATH, "//div[contains(text(),'÷')]").get_attribute('role') == 'button' # находим значение атрибута

# 3. Кнопка деления, обозначенная символом '÷', выполняет именно функцию деления. Проверяем на простом примере
@allure.feature('Общие базовые проверки')
@allure.story('Кнопка деления отвечает за функцию деления')
@allure.severity('blocker')
def test_division_button_resposible_for_division():
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))).click() # клик по полю калькулятора
    keyboard.write('80/10') # ввод значений с клавиатуры
    keyboard.send('enter')
    assert pytest.driver.find_element(By.ID, "cwos").text == '8' # сверяем ответ с ожидаемым

# 4. Корректность деления чисел. Значения из data.py подставляются через фикстуры.
# В данном примере используются комбинации рандомных целых чисел с заданной значностью (2-х, 3-х, 4-х и 5-ти значные, можно указать иные)
@allure.feature('Проверка функции деления')
@allure.story('Деление целых и дробных чисел')
@pytest.mark.parametrize("integer_division", [whole_numbers(2), whole_numbers(3)], ids=["двухзначные числа", "трехзначные числа"])
@pytest.mark.parametrize("integer_division2", [ whole_numbers(4), whole_numbers(5)], ids=["четырехзначные числа", "пятизначные числа"])
def test_integer_division(integer_division, integer_division2):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))).click()
    keyboard.write(integer_division + '/' + integer_division2) #вводим с клавиатуры 2 рандомных значения: из первой и второй фикстур
    keyboard.send('enter')
    """
    Придется долго комментировать. В разных примерах гугл обрезал число после точки на разное количество знаков (например, при делении 1 на 3 это 11 знаков
    после точки, а при делении 9256571 на 23 это 6 знаков, когда их больше) + он где-то именно обрезает, а где-то округляет, какое огругление используется — вопрос.
    Чтобы избежать падения тестов, приведём ответы к одинаковому виду. Посчитаем количество знаков (number) после точки в полученном в гугле результате (result).
    Получаем свой ответ при делении (answer), округлим его до number знаков после запятой и отбросим последнее число.
    У result тоже отбрасываем последнее число. Смотрим, что гугловский result и наш answer тождественны. Так становится неважно,
    округлил или обрезал гугл число в конкретном примере.
    Если при делении получается целое число, то эти ухищрения не нужны.

    А еще он иногда даёт ответ в виде 3.7673372e-34. Ищем 'e' в ответе, и, если она есть, обрезаем ответ до 'e' сравниваем с нашим результатом, который обрезаем на то же кол-во знаков

    Иногда числа получаются по типу '2.922481e-5' у гугла и '0.0000292248...' у нас. На таком исключении тест падает.
    """
    result = pytest.driver.find_element(By.ID, "cwos").text

    if 'e' in result: # если в ответе есть "е"
        num_length = len(result.split('e')[0]) - 1 # длина части до e с учетом 0 индекса
        result = result[:num_length]
        answer = int(integer_division) / int(integer_division2)
        answer = str(answer)
        answer = answer[:num_length]
        assert result == answer

    else: # если в ответе нет "е", ориентируемся, целое это число или дробь. Дроби приводим к общему виду, обрезаем
        if '.' in result: # смотрим, есть ли точка, указывающая на дробь, в гугловском ответе
            number = len(result.split('.')[1]) # разделяем по точке и берем длину части после точки
        else:
            number = 0

        answer = int(integer_division) / int(integer_division2)  # делим те же числа

        if number !=0:
            answer = round(answer, number)
            answer = str(answer)
            answer = answer[:-1]
            result = result[:-1]
            assert answer == result
        else:
            answer = str(answer)
            assert answer == result

# 5. Аналогично тесту 4 проверяем корректность деления дробных чисел.
# Псевдорандомные значения из файла data.py подставляются через фикстуры, можно указать верхний порог числа (от нуля до n)
@allure.feature('Проверка функции деления')
@allure.story('Деление дробных чисел')
@pytest.mark.parametrize("non_integer_division", [non_integer_numbers(50)], ids=["дробное число от 0 до 50"])
@pytest.mark.parametrize("non_integer_division2", [non_integer_numbers(70)], ids=["дробное число от 0 до 70"])
def test_non_integer_division(non_integer_division, non_integer_division2):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))).click()
    keyboard.write(non_integer_division + '/' + non_integer_division2)  # вводим с клавиатуры 2 рандомных значения: из первой и второй фикстур
    keyboard.send('enter')

    result = pytest.driver.find_element(By.ID, "cwos").text

    if 'e' in result: # если в ответе есть "е"
        num_length = len(result.split('e')[0]) - 1 # длина части до e с учетом 0 индекса
        result = result[:num_length]
        answer = float(integer_division) / float(integer_division2)
        answer = str(answer)
        answer = answer[:num_length]
        assert result == answer

    else: # если в ответе нет "е", ориентируемся, целое это число или дробь. Дроби приводим к общему виду, обрезаем
        if '.' in result:
            number = len(result.split('.')[1])
        else:
            number = 0

        answer = float(non_integer_division) / float(non_integer_division2)  # делим те же числа

        if number !=0:
            answer = round(answer, number)
            answer = str(answer)
            answer = answer[:-1]
            result = result[:-1]
            assert answer == result
        else:
            answer = str(answer)
            assert answer == result

# 6. При делении отрицательного числа на отрицательное всегда получится положительное. На примере целых отрицательных чисел с заданной значностью
@allure.feature('Проверка функции деления')
@allure.story('Получение положительного числа при делении двух отрицательных чисел')
@pytest.mark.parametrize("negative_number", [whole_negative_numbers(3)], ids=["отрицательное трехзначное число"])
@pytest.mark.parametrize("negative_number2", [whole_negative_numbers(4)], ids=["отрицательное четырехзначное число"])
def test_negative_numbers_division_results_in_positive_number(negative_number, negative_number2):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))).click()
    keyboard.write(negative_number + '/' + negative_number2) #вводим с клавиатуры 2 рандомных отрицательных числа: из первой и второй фикстур
    keyboard.send('enter')
    first_symbol = pytest.driver.find_element(By.ID, "cwos").text[0]
    assert '-' != first_symbol # чтобы не вылавливать "е-" просто смотрим, что первый символ — не минус

# 7. Backspace удаляет полученный ответ и очищает поле ввода, остаётся 0
@allure.feature('Общие базовые проверки')
@allure.story('Backspace удаляет полученный ответ')
@pytest.mark.parametrize("integer_division", [whole_numbers(2)], ids=["двухзначное число"])
@pytest.mark.parametrize("integer_division2", [whole_numbers(2)], ids=["двухзначное число"])
def test_backspace_deletes_answer(integer_division, integer_division2):
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "cwos"))).click()
    keyboard.write(integer_division + '/' + integer_division2)
    keyboard.send('enter')
    keyboard.send('backspace')
    assert pytest.driver.find_element(By.ID, "cwos").text == '0'

