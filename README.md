(.venv) akshay@DEBIANWM:~/jupyter-projects/mybooks_web$ cat README.md 
# MyBooks — Flask Book Management System

MyBooks is a web-based book management application built with **Python, Flask, MySQL, HTML, CSS, and Jinja2**.

The application allows users to manage a personal collection of books and authors, track reading status, search and filter books, and view basic statistics about their library.

## Features

* View all books in a searchable and sortable table
* Filter books by:

  * Book ID
  * Book name
  * Year
  * Genre
  * Author
  * Reading status
* Sort books by clicking table column headers
* Choose the number of rows displayed per page
* Add new books
* Edit existing books
* Delete books
* Add authors
* Delete authors
* View the number of books associated with each author
* Dashboard statistics for:

  * Total books
  * Total authors
  * Finished books
  * Currently reading
  * Want to Read
  * Cancelled books
* Genre selection using genres already present in the database
* Form validation
* Parameterized SQL queries
* Responsive web interface

## Technology Stack

| Technology             | Purpose                          |
| ---------------------- | -------------------------------- |
| Python 3               | Application programming language |
| Flask                  | Web framework                    |
| MySQL                  | Database                         |
| mysql-connector-python | MySQL database connectivity      |
| Jinja2                 | HTML templating                  |
| HTML5                  | Page structure                   |
| CSS3                   | Styling                          |
| python-dotenv          | Environment variable management  |
| Git                    | Version control                  |

## Project Structure

```text
mybooks_web/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── authors.html
    ├── book_form.html
    └── error.html
```

## Database

The application uses an existing MySQL database named:

```text
Mybooks
```

The main tables are:

### Authors

```text
AuthorId
AuthorName
Gender
```

`AuthorId` is the primary key and uses `AUTO_INCREMENT`.

### Books

```text
BookId
BookName
Year
Genre
AuthorId
Status
```

`BookId` is the primary key and uses `AUTO_INCREMENT`.

`AuthorId` is a foreign key referencing:

```text
Authors.AuthorId
```

This creates a relationship between books and their authors.

The database also contains the following views:

```text
Count
ReadStatus
```

The application does not depend on these views for its dashboard calculations. Statistics are calculated directly from the `Books` table.

## Current Genres

The application dynamically reads the available genres from the database.

The current database contains:

```text
Fantasy
Sci-Fi
Self-Help
Thriller
```

## Reading Status

The application currently supports:

```text
Finished
Reading
Want to Read
Cancelled
```

## Requirements

* Python 3
* MySQL Server
* MySQL database named `Mybooks`

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd mybooks_web
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local `.env` file from the example:

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
FLASK_SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_SECRET
```

**Do not commit `.env` to GitHub.**

The `.env` file contains local configuration and credentials and is intentionally excluded through `.gitignore`.

### 5. Start the application

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Then run:

```bash
python3 app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

## Accessing the Application From Another Machine

The Flask application is configured to listen on:

```python
host="0.0.0.0"
```

Therefore, when the VM is reachable from another machine, the application can be accessed using the VM's IP address:

```text
http://<VM-IP>:5000
```

For example:

```text
http://192.168.x.x:5000
```

The exact IP address depends on the VM's network configuration.

For production deployment, a production WSGI server such as Gunicorn should be used instead of Flask's built-in development server.

## Security Notes

* Database credentials are stored in `.env`.
* `.env` is excluded from Git using `.gitignore`.
* SQL queries use parameterized values rather than directly concatenating user input.
* The Flask secret key should be supplied through the environment.
* Debug mode is disabled when the application is started normally.

## Future Improvements

Planned improvements include:

* Refactoring the application into a modular Flask structure
* SQLAlchemy ORM integration
* Improved Bootstrap-based UI
* Interactive dashboard charts
* User authentication
* Automated tests using pytest
* REST API
* API documentation
* Docker support
* Production deployment configuration
* Improved error handling and logging

## Learning Goals

This project is also being developed as a practical Python portfolio project.

The goal is to demonstrate experience with:

* Python
* Flask
* MySQL
* SQL
* CRUD operations
* Relational database design
* Foreign keys
* HTML/CSS
* Jinja2 templates
* Form handling
* Input validation
* Git and GitHub
* Web application architecture
* Automated testing
* API development

## License

This project is intended as a personal learning and portfolio project.
