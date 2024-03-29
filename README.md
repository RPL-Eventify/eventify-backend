# Eventify

## Link

1. Production: <https://eventify.adaptable.app/>
2. Development: <https://eventify-dev.adaptable.app/>

## Local Development

1. Buat virtual environment

    ```shell
    python -m venv env
    ```

2. Aktifkan virtual environment

    ```shell
    env\Scripts\activate
    ```

    > Note: Perintah di atas dijalankan pada sistem operasi Windows

3. Install semua *dependencies*

    ```shell
    pip install -r requirements.txt
    ```

4. Masukkan `.env` file pada folder project `eventify` dengan informasi yang sesuai.

    ```shell
    DEBUG=<value>
    ENVIRONMENT=<value>
    DB_NAME=<value>
    DB_USER=<value>
    DB_PASSWORD=<value>
    DB_HOST=<value>
    DB_PORT=<value>
    SECRET_KEY=<value>
    DB_SCHEMA=<value>
    ```

    > Note: \<value\> diganti dengan informasi yang sesuai.

5. Jalankan migrasi

    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Jalankan development server

    ```shell
    python manage.py runserver
    ```
