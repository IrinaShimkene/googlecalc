# googlecalc
Тесты писались запускались через IDE PyCharm. 
Для запуска тестов необходимо:
- установить библиотеки из файла requirements.txt, набрав в терминале pip install -r requirements.txt
- тесты написаны для Chrome браузера, версия для Chrome 110. лежит в папке. Если у вас версия отличается, установите драйвер отсюда: https://chromedriver.chromium.org/downloads
- для запуска тестов с сохранением allure-отчетов из терминала: pytest --alluredir=results ui_tests.py
!!! Здесь в папке results сохранены мои результаты последнего прогона. Не знаю, сколько хранится ссылка, вот отчет: http://172.20.10.5:56309/index.html# или выгрузите из папки/удалите для нового запуска тестов.

Для всех тестов оставлены комментарии. Всего получилось 10 позитивных тестов.
