# UploadProcessFiles

## Обзор
Это Django-приложение предоставляет API для загрузки и асинхронной обработки различных типов файлов с
использованием Celery. В нем реализована поддержка обработки текстовых файлов, изображений и PDF. Для 
контейнизации приложения используется Docker, что упрощает его развертывание и запуск.

## Предварительные требования
- [Docker](https://www.docker.com/get-started) установлен на вашей системе.

## Начало работы
1. Склонируйте этот репозиторий на свой локальный компьютер:
   ```bash
   git clone https://github.com/vvvdanilsss/UploadProcessFiles.git
   
   ```

2. Постройте Docker-контейнеры:
   ```bash
   docker-compose build

   ```

3. Запустите приложение и сервисы:
   ```bash
   docker-compose up
   
   ```

4. Django API теперь доступен по адресу [http://localhost:8000/api/](http://localhost:8000/api/).

## Использование
- Чтобы загрузить файл, выполните POST-запрос к точке `/api/upload/`, передав файл как поле формы. Файл
- будет обработан асинхронно, и ответ API будет содержать информацию о загруженном файле.

- Чтобы просмотреть список загруженных файлов и их статус обработки, выполните GET-запрос к точке `/api/files/`.

## Поддерживаемые типы файлов
- Текстовые файлы (например, `.txt`, `.csv`)
- Изображения (например, `.jpg`, `.jpeg`, `.png`)
- PDF-файлы (например, `.pdf`)

## Обработка ошибок
Приложение обрабатывает различные сценарии ошибок, включая ошибки валидации и ошибки "файл не найден". Для 
каждого случая возвращаются соответствующие HTTP-статусы и сообщения об ошибках.

## Пользовательские настройки
Вы можете расширить и настроить приложение для поддержки дополнительных типов файлов или задач обработки по 
вашему усмотрению.

## Развертывание
Это приложение можно развернуть на различных хостинг-платформах, таких как AWS, Heroku или на вашей собственной 
серверной инфраструктуре. Убедитесь, что у вас есть необходимые переменные окружения и настройки для развертывания 
в рабочей среде.