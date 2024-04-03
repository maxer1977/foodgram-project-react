# **Каталог рецептов - Foodgram**

## Описание

**«Foodgram»** - это ресурс для пользователей о красивой и вкусной еде. Здесь польмзователи смогут не только познакомиться с разнообразными рецептами, но и  опубликовать свои. 
- Рецепты отсортированны по дате публикации (от новых к старым).
- Рецепты фильтруются по тегам (категориям рецептов).
- Рецепты разбиты по страницам (т.н. пагинация).
При этом:
- _НЕавторизовавшиеся пользователи_:
  * имеют доступ только к главной странице и отдельному рецепту.
  * им доступна регистрация и последующая авторизация на ресурсе.
- _Авторизовавшиеся пользователи_:
  * имеют доступ к главной странице, отдельному рецепту, странице подписок, странице покупок с последующим созданием рецептов, подписок и покупок.
  * могут оформить/аннулировать подписку на выбранного автора или отдельный рецепт.
  * могут сохранить «Список покупок» в txt-файле, при этом продукты повторяющиеся в разных рецептах объединяются в одну строку, а их количество суммируется.
- _Администратор_:
  * имеет полный доступ (чтение и редактирование/удаление) ко всем моелям в "админке"

Применена пагинация и фильтрация по тегам (категории рецептов).
Проект запускается на удалённом сервере в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Контейнер с проектом обновляется на Docker Hub.
Данные сохраняются в volumes.
 
### Технологии
Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL

### Запуск проекта на удаленном сервере
- Установить на сервере Docker, Docker Compose
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```
- Клонировать репозиторий
- Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra:
```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```
- Заполнить переменные в разделе Secrets > Actions для работы с GitHub Actions:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение
DB_ENGINE               # django.db.backends.postgresql
POSTGRES_DB             # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```
- Создать и запустить контейнеры Docker, выполнить команду на сервере :
```
sudo docker compose up -d
```
- Выполнить миграции:
```
sudo docker compose exec backend python manage.py migrate
```
- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```
- Собрать статику:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

После каждого обновления репозитория (ветка master) автоматически выполняется
сборка и доставка докер-образов frontend и backend на Docker Hub, затем
разворачивание обновленного проекта на удаленном сервере
Дополнительно реализована отправка сообщения в Telegram при успешном
разворачивании проекта


### API-endpoints

- просмотр списка пользователей и добавление нового пользователя **GET, POST**: /api/users/
- просмотр пользователя **GET**: /api/users/<id>/
- просмотр "текущего" пользователя **GET**: /api/users/me/
- просмотр списка рецептов и добавление нового **GET, POST**: /api/recipes/
- просмотр рецепта **GET**: /api/recipes/<id>/
- добавить/удалить рецепт в список покупок **POST, DELETE**: /api/recipes/<id>/shopping_cart/
- сформировать и сохранить список покупок **GET**: /api/recipes/<id>/download_shopping_cart
- добавить/удалить рецепт в список избранного **POST, DELETE**: /api/recipes/<id>/favorite/
- подписаться/отписаться на автора **POST, DELETE**: /api/recipes/<id>/subscribe/
- просмотр списка подписок **GET**:/api/recipes/subscriptions

### Авторы
Максим и команда Практикума
