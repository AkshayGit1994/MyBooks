# MyBooks Flask Website

A small Flask website for entering and managing the `Authors` and `Books` tables in the MySQL `Mybooks` database.

## Your existing schema

The application expects:

- `Authors(AuthorId, AuthorName, Gender)`
- `Books(BookId, BookName, Year, Genre, AuthorId, Status)`

It does not modify your database schema.

## Features

- Add authors
- Delete authors
- Add books
- Edit books
- Delete books
- Search books by book name, author, genre or status
- Dashboard counts
- Author/book relationship through `AuthorId`
- Parameterized SQL queries
- Responsive interface

The application does not depend on the `Count` and `ReadStatus` views because their definitions were not supplied. The dashboard calculates its counts directly from `Books`.

## 1. Create the Python environment

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv
```

From this project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure MySQL

Copy the example configuration:

```bash
cp .env.example .env
```

Edit `.env`:

```text
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=Mybooks
FLASK_SECRET_KEY=CHANGE_THIS
```

Make sure the MySQL database already exists:

```sql
USE Mybooks;
SHOW TABLES;
```

No schema-changing SQL is required by this application.

## 3. Start the website

```bash
source .venv/bin/activate
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Important note about IDs

Your current schema shows:

```text
AuthorId int NOT NULL PRIMARY KEY
BookId   int NOT NULL PRIMARY KEY
```

Neither column is `AUTO_INCREMENT`.

Therefore, this website asks you to enter `AuthorId` and `BookId` manually when adding records.

If you later want the website to generate IDs automatically, the database schema can be changed to use `AUTO_INCREMENT`. Do not make that change blindly if existing IDs or relationships need to be preserved.

## Status values

The form currently provides:

- Finished
- Reading
- Want to Read
- Cancelled

All fit within your current `varchar(12)` limit.

If your existing database uses different status names, edit the list in `templates/book_form.html`.

## Running on your local network

For testing from another machine on your LAN, change the last line of `app.py` from:

```python
app.run(host="127.0.0.1", port=5000, debug=True)
```

to:

```python
app.run(host="0.0.0.0", port=5000, debug=False)
```

Then access it using the Debian machine's LAN IP and port 5000.

For a real deployment, use a production WSGI server such as Gunicorn and put it behind a reverse proxy rather than using Flask's development server.
