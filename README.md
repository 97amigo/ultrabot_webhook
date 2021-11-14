Телеграм бот для сервисного отдела компании "Ультрафиолет". Позволяет клиенту записаться на выполнение процедур сервисного обслуживания его аппарата.
Работает следующим образом:
Клиент пишет в сообщении боту свой ID и номер своей манипулы. Если такой клиент с такой манипулой присутствует в базе данных, бот делает соответсвующую запись в гугл таблице (доступ которой есть только у меня:) ) и выводит сообщение об успешной записи на сервисное обслуживание, в противном случае выводит сообщение что "вас нет в базе".

Реализация:
База данных - sqlLite. Используется ORM Peewee для более удобной работы с ней.
Для работы с Телеграмом используется библиотека telebot.
Бот запускается как demon на сервере с OC Linux, работает на веб-хуках.
Для авторизации в гугл-таблицах используется библиотека oauth2client.service_account.
