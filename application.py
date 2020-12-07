import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, current_app, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask import Blueprint

from helpers import apology, login_required, lookup, clp, Pager

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = clp

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 21
app.config['VISIBLE_PAGE_COUNT'] = 8

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///super.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
#@login_required
def index():
    """Show all prices"""

    if request.method == "GET":
        # Get data from lider
        indexes_lider = db.execute("SELECT * FROM lider ORDER BY LENGTH(savings), savings, LENGTH(price), price DESC")
        indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE savings > 0 ORDER BY LENGTH(savings), savings LIMIT 6")
        brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")
        indexes2 = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE '%superpack%' OR name LIKE '%promo%' ORDER BY LENGTH(savings), savings LIMIT 6")

        # Pagination
        page = int(request.args.get('page', 1))

        count = len(indexes)
        data = indexes

        pager = Pager(page, count)
        pages = pager.get_pages()

        offset = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[offset: offset + limit]

        # Get data from jumbo
        indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
        # Search through the loop the symbols to display in html and specify through the render template
        return render_template("index.html", lider = indexes_lider, jumbo = indexes_jumbo, indexes2 = indexes2, pages = pages, data_to_show = data_to_show, indexes = indexes)

@app.route("/ofertas", methods=["GET", "POST"])
#@login_required
def ofertas():
    """Show all prices"""

    if request.method == "GET":
        # Get data from lider
        indexes_lider = db.execute("SELECT * FROM lider ORDER BY LENGTH(savings), savings, LENGTH(price), price DESC")
        indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE savings > 0 ORDER BY LENGTH(savings), savings")
        brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

        # Pagination
        page = int(request.args.get('page', 1))

        count = len(indexes)
        data = indexes

        pager = Pager(page, count)
        pages = pager.get_pages()

        offset = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[offset: offset + limit]

        # Get data from jumbo
        indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
        # Search through the loop the symbols to display in html and specify through the render template
        return render_template("ofertas.html", lider = indexes_lider, jumbo = indexes_jumbo, brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/promos", methods=["GET", "POST"])
#@login_required
def promos():
    """Show all prices"""

    if request.method == "GET":
        # Get data from lider
        indexes_lider = db.execute("SELECT * FROM lider ORDER BY LENGTH(savings), savings, LENGTH(price), price DESC")
        indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE '%superpack%' OR name LIKE '%promo%' ORDER BY LENGTH(savings), savings")
        brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

        # Pagination
        page = int(request.args.get('page', 1))

        count = len(indexes)
        data = indexes

        pager = Pager(page, count)
        pages = pager.get_pages()

        offset = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[offset: offset + limit]

        # Get data from jumbo
        indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
        # Search through the loop the symbols to display in html and specify through the render template
        return render_template("promos.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/lider", methods=["GET", "POST"])
#@login_required
def lider():
    """Show portfolio of stocks"""

    if request.method == "GET":
        # Get data from lider
        indexes = db.execute("SELECT * FROM lider ORDER BY LENGTH(savings), savings, LENGTH(price), price DESC")
        brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

        # Pagination
        page = int(request.args.get('page', 1))

        count = len(indexes)
        data = indexes

        pager = Pager(page, count)
        pages = pager.get_pages()

        offset = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[offset: offset + limit]

        # Get data from jumbo
        indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
        # Search through the loop the symbols to display in html and specify through the render template
        return render_template("lider.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)


@app.route("/jumbo", methods=["GET", "POST"])
#@login_required
def jumbo():
    """Show portfolio of stocks"""

    if request.method == "GET":
        # Get data from lider
        indexes = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(savings), savings, LENGTH(price), price DESC")
        brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

        # Pagination
        page = int(request.args.get('page', 1))

        count = len(indexes)
        data = indexes

        pager = Pager(page, count)
        pages = pager.get_pages()

        offset = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[offset: offset + limit]

        # Get data from jumbo
        indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
        # Search through the loop the symbols to display in html and specify through the render template
        return render_template("jumbo.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)



@app.route("/search", methods=["GET", "POST"])
#@login_required
def search():
    """Search for products"""
    # Display form
    #global busqueda

    if request.method == "POST":

        # Get data from search
        if request.form.get("search"):
            session['search_query'] = request.form.get("search")

            search_result = db.execute("SELECT * FROM (SELECT * FROM lider WHERE name LIKE  (?) OR brand LIKE (?) UNION ALL SELECT * FROM jumbo WHERE name LIKE  (?) OR brand LIKE (?)) ORDER BY LENGTH(price), price", "%" + request.form.get("search") + "%", "%" + request.form.get("search") + "%", "%" + request.form.get("search") + "%", "%" + request.form.get("search") + "%")
            return redirect("/search_results")
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/search_results")
@app.route("/search_results/<busqueda>")
#@login_required
def search_results():
    """Show items for search query"""
    busqueda = session.get('search_query', None)
    # Search results
    search_result = db.execute("SELECT * FROM (SELECT * FROM lider WHERE name LIKE  (?) OR brand LIKE (?) UNION ALL SELECT * FROM jumbo WHERE name LIKE  (?) OR brand LIKE (?)) ORDER BY LENGTH(price), price", "%" + busqueda + "%", "%" + busqueda + "%", "%" + busqueda + "%", "%" + busqueda + "%")
    if len(search_result) == 0:
        return apology("Ningún producto encontrado")
    # Pagination
    page = int(request.args.get('page', 1))

    count = len(search_result)
    data = search_result

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    return render_template("search_results.html", data_to_show = data_to_show, pages = pages, count = count, busqueda = busqueda.upper())


@app.route("/pisco", methods=["GET", "POST"])
def pisco():
    """Show pisco"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE '%pisco%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("pisco.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/gin", methods=["GET", "POST"])
def gin():
    """Show gin"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'gin%' OR name LIKE '% gin%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("gin.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/ron", methods=["GET", "POST"])
def ron():
    """Show ron"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'ron%' OR name LIKE '% ron%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("ron.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/cerveza", methods=["GET", "POST"])
def cerveza():
    """Show cerveza"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'cerveza%' OR name LIKE '% cerveza%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("cerveza.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/vodka", methods=["GET", "POST"])
def vodka():
    """Show vodka"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'vodka%' OR name LIKE '% vodka%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("vodka.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/whisky", methods=["GET", "POST"])
def whisky():
    """Show whisky"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'whisky%' OR name LIKE '% whisky%' OR name LIKE 'whiskey%' OR name LIKE '% whiskey%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("whisky.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/tequila", methods=["GET", "POST"])
def tequila():
    """Show tequila"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'tequila%' OR name LIKE '% tequila%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("tequila.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/vino", methods=["GET", "POST"])
def vino():
    """Show wine"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'vino%' OR name LIKE '% vino%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Get data from jumbo
    indexes_jumbo = db.execute("SELECT * FROM jumbo ORDER BY LENGTH(price), price")
    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("vino.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)

@app.route("/espumante", methods=["GET", "POST"])
def espumante():
    """Show espumantes"""

    # Get data like pisco
    indexes = db.execute("SELECT * FROM (SELECT * FROM lider UNION ALL SELECT * FROM jumbo) WHERE name LIKE 'espumante%' OR name LIKE '% espumante%' OR name LIKE 'champaña%' OR name LIKE '% champaña%' ORDER BY LENGTH(price), price ASC")
    brands = db.execute("SELECT * FROM (SELECT brand FROM lider UNION SELECT brand FROM jumbo)")

    # Pagination
    page = int(request.args.get('page', 1))

    count = len(indexes)
    data = indexes

    pager = Pager(page, count)
    pages = pager.get_pages()

    offset = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[offset: offset + limit]

    # Search through the loop the symbols to display in html and specify through the render template
    return render_template("espumante.html", brands = brands, pages = pages, data_to_show = data_to_show, count = count, indexes = indexes)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
