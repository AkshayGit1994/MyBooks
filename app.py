import os

import mysql.connector
from mysql.connector import Error
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-only-change-this")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "Mybooks")
    )


def query_db(sql, params=()):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def execute_db(sql, params=()):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_authors():
    return query_db("""
        SELECT AuthorId, AuthorName, Gender
        FROM Authors
        ORDER BY AuthorName
    """)


def get_genres():
    return [
        row["Genre"] for row in query_db("""
            SELECT DISTINCT Genre
            FROM Books
            WHERE Genre IS NOT NULL AND Genre <> ''
            ORDER BY Genre
        """)
    ]


def get_statuses():
    return [
        row["Status"] for row in query_db("""
            SELECT DISTINCT Status
            FROM Books
            WHERE Status IS NOT NULL AND Status <> ''
            ORDER BY Status
        """)
    ]


def get_stats():
    return {
        "books": query_db("SELECT COUNT(*) AS n FROM Books")[0]["n"],
        "authors": query_db("SELECT COUNT(*) AS n FROM Authors")[0]["n"],
        "finished": query_db(
            "SELECT COUNT(*) AS n FROM Books WHERE Status = %s",
            ("Finished",)
        )[0]["n"],
        "reading": query_db(
            "SELECT COUNT(*) AS n FROM Books WHERE Status = %s",
            ("Reading",)
        )[0]["n"],
        "want_to_read": query_db(
            "SELECT COUNT(*) AS n FROM Books WHERE Status = %s",
            ("Want to Read",)
        )[0]["n"],
        "cancelled": query_db(
            "SELECT COUNT(*) AS n FROM Books WHERE Status = %s",
            ("Cancelled",)
        )[0]["n"],
    }


@app.route("/")
def index():
    sort = request.args.get("sort", "BookId").strip()
    direction = request.args.get("direction", "desc").strip().lower()

    allowed_sort_columns = {
        "BookId": "b.BookId",
        "BookName": "b.BookName",
        "Year": "b.Year",
        "Genre": "b.Genre",
        "AuthorName": "a.AuthorName",
        "Status": "b.Status"
    }

    if sort not in allowed_sort_columns:
        sort = "BookId"

    if direction not in ("asc", "desc"):
        direction = "desc"

    sort_column = allowed_sort_columns[sort]
    sort_direction = direction.upper()

    book_id = request.args.get("book_id", "").strip()
    book_name = request.args.get("book_name", "").strip()
    year = request.args.get("year", "").strip()
    genre = request.args.get("genre", "").strip()
    author_id = request.args.get("author_id", "").strip()
    status = request.args.get("status", "").strip()

    conditions = []
    params = []

    if book_id and book_id.isdigit():
        conditions.append("b.BookId = %s")
        params.append(int(book_id))

    if book_name:
        conditions.append("b.BookName LIKE %s")
        params.append(f"%{book_name}%")

    if year and year.isdigit():
        conditions.append("b.Year = %s")
        params.append(int(year))

    if genre:
        conditions.append("b.Genre = %s")
        params.append(genre)

    if author_id and author_id.isdigit():
        conditions.append("b.AuthorId = %s")
        params.append(int(author_id))

    if status:
        conditions.append("b.Status = %s")
        params.append(status)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    rows_param = request.args.get("rows", "10")
    allowed_rows = [10, 25, 50, 100]

    if rows_param == "all":
        rows_per_page = "all"
    else:
        try:
            rows_per_page = int(rows_param)
        except ValueError:
            rows_per_page = 10

        if rows_per_page not in allowed_rows:
            rows_per_page = 10

    total_books = query_db(
        f"SELECT COUNT(*) AS total FROM Books b {where_clause}",
        tuple(params)
    )[0]["total"]

    if rows_per_page == "all":
        total_pages = 1
        page = 1
    else:
        total_pages = max(
            1,
            (total_books + rows_per_page - 1) // rows_per_page
        )
        page = max(1, min(page, total_pages))

    select_sql = f"""
        SELECT
            b.BookId,
            b.BookName,
            b.Year,
            b.Genre,
            b.AuthorId,
            b.Status,
            a.AuthorName,
            a.Gender
        FROM Books b
        LEFT JOIN Authors a ON a.AuthorId = b.AuthorId
        {where_clause}
        ORDER BY {sort_column} {sort_direction}
    """

    if rows_per_page == "all":
        books = query_db(select_sql, tuple(params))
    else:
        offset = (page - 1) * rows_per_page
        books = query_db(
            select_sql + " LIMIT %s OFFSET %s",
            tuple(params + [rows_per_page, offset])
        )

    authors = get_authors()
    genres = get_genres() or ["Fantasy", "Sci-Fi", "Self-Help", "Thriller"]
    statuses = get_statuses()
    stats = get_stats()

    current_filters = {
        "book_id": book_id,
        "book_name": book_name,
        "year": year,
        "genre": genre,
        "author_id": author_id,
        "status": status,
        "rows": rows_param,
        "sort": sort,
        "direction": direction
    }

    def sort_url(column):
        if sort == column:
            new_direction = "asc" if direction == "desc" else "desc"
        else:
            new_direction = "asc"

        return url_for(
            "index",
            page=1,
            rows=rows_param,
            book_id=book_id,
            book_name=book_name,
            year=year,
            genre=genre,
            author_id=author_id,
            status=status,
            sort=column,
            direction=new_direction
        )

    return render_template(
        "index.html",
        books=books,
        authors=authors,
        genres=genres,
        statuses=statuses,
        stats=stats,
        page=page,
        total_pages=total_pages,
        total_books=total_books,
        rows_param=rows_param,
        filters=current_filters,
        sort=sort,
        direction=direction,
        sort_url=sort_url
    )


@app.route("/authors")
def authors():
    authors = query_db("""
        SELECT
            a.AuthorId,
            a.AuthorName,
            a.Gender,
            COUNT(b.BookId) AS BookCount
        FROM Authors a
        LEFT JOIN Books b ON b.AuthorId = a.AuthorId
        GROUP BY a.AuthorId, a.AuthorName, a.Gender
        ORDER BY a.AuthorName
    """)
    return render_template("authors.html", authors=authors)


@app.route("/authors/add", methods=["POST"])
def add_author():
    author_name = request.form.get("AuthorName", "").strip()
    gender = request.form.get("Gender", "").strip()

    if not author_name or not gender:
        flash("Author Name and Gender are required.", "error")
        return redirect(url_for("authors"))

    if len(author_name) > 20:
        flash("Author Name cannot exceed 20 characters.", "error")
        return redirect(url_for("authors"))

    if len(gender) > 6:
        flash("Gender cannot exceed 6 characters.", "error")
        return redirect(url_for("authors"))

    try:
        author_id = execute_db(
            "INSERT INTO Authors (AuthorName, Gender) VALUES (%s, %s)",
            (author_name, gender)
        )
        flash(f"Author added successfully. Author ID: {author_id}", "success")
    except Error as e:
        flash(f"Could not add author: {e}", "error")

    return redirect(url_for("authors"))


@app.route("/authors/delete/<int:author_id>", methods=["POST"])
def delete_author(author_id):
    try:
        execute_db(
            "DELETE FROM Authors WHERE AuthorId = %s",
            (author_id,)
        )
        flash("Author deleted successfully.", "success")
    except Error:
        flash(
            "This author cannot be deleted because one or more books "
            "are associated with this author.",
            "error"
        )
    return redirect(url_for("authors"))


@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    authors = get_authors()
    genres = get_genres() or ["Fantasy", "Sci-Fi", "Self-Help", "Thriller"]

    if request.method == "POST":
        book_name = request.form.get("BookName", "").strip()
        year = request.form.get("Year", "").strip()
        genre = request.form.get("Genre", "").strip()
        author_id = request.form.get("AuthorId", "").strip()
        status = request.form.get("Status", "").strip()

        if not all([book_name, year, genre, author_id, status]):
            flash("Please fill in all book fields.", "error")
            return render_template(
                "book_form.html",
                authors=authors,
                genres=genres,
                book=None
            )

        if not year.isdigit():
            flash("Year must be a valid number.", "error")
            return render_template(
                "book_form.html",
                authors=authors,
                genres=genres,
                book=None
            )

        if len(book_name) > 40:
            flash("Book Name cannot exceed 40 characters.", "error")
            return render_template(
                "book_form.html",
                authors=authors,
                genres=genres,
                book=None
            )

        if len(genre) > 10:
            flash("Genre cannot exceed 10 characters.", "error")
            return render_template(
                "book_form.html",
                authors=authors,
                genres=genres,
                book=None
            )

        try:
            book_id = execute_db(
                """
                INSERT INTO Books
                    (BookName, Year, Genre, AuthorId, Status)
                VALUES
                    (%s, %s, %s, %s, %s)
                """,
                (book_name, int(year), genre, int(author_id), status)
            )
            flash(f"Book added successfully. Book ID: {book_id}", "success")
            return redirect(url_for("index"))
        except Error as e:
            flash(f"Could not add book: {e}", "error")

    return render_template(
        "book_form.html",
        authors=authors,
        genres=genres,
        book=None
    )


@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    rows = query_db(
        "SELECT * FROM Books WHERE BookId = %s",
        (book_id,)
    )

    if not rows:
        flash("Book not found.", "error")
        return redirect(url_for("index"))

    book = rows[0]
    authors = get_authors()
    genres = get_genres() or ["Fantasy", "Sci-Fi", "Self-Help", "Thriller"]

    if request.method == "POST":
        book_name = request.form.get("BookName", "").strip()
        year = request.form.get("Year", "").strip()
        genre = request.form.get("Genre", "").strip()
        author_id = request.form.get("AuthorId", "").strip()
        status = request.form.get("Status", "").strip()

        if not all([book_name, year, genre, author_id, status]):
            flash("Please fill in all book fields.", "error")
            return render_template(
                "book_form.html",
                authors=authors,
                genres=genres,
                book=book
            )

        try:
            execute_db(
                """
                UPDATE Books
                SET
                    BookName = %s,
                    Year = %s,
                    Genre = %s,
                    AuthorId = %s,
                    Status = %s
                WHERE BookId = %s
                """,
                (
                    book_name,
                    int(year),
                    genre,
                    int(author_id),
                    status,
                    book_id
                )
            )
            flash("Book updated successfully.", "success")
            return redirect(url_for("index"))
        except Error as e:
            flash(f"Could not update book: {e}", "error")

    return render_template(
        "book_form.html",
        authors=authors,
        genres=genres,
        book=book
    )


@app.route("/books/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    try:
        execute_db(
            "DELETE FROM Books WHERE BookId = %s",
            (book_id,)
        )
        flash("Book deleted successfully.", "success")
    except Error as e:
        flash(f"Could not delete book: {e}", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
