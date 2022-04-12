### Проект "Yatube"

Социальная сеть Yatube с авторизацией, персональными лентами, 
комментариями и подпиской на авторов. 

Покрытие кода тестами.


(python, django, html/ccs, git, sqlite)
```
1) Создавать профиль, для публикации записей.
```
```
2) Публикация поста в ленте, (возможность выбора группы, в которой появится этот пост).
```
```
3) Просматривать и подписываться на страницы других авторов.
```

```
4) Комментировать записи других авторов.
```
```
5) Работа с пользователями, создание групп осуществляется через панель администратора
```
```
6) Unittest основных функций.
```



### Как запустить проект:

```
https://github.com/pkrfc/python-django.git
```


Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```



