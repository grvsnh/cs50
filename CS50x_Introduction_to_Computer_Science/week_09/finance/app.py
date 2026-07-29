import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Register custom filter to format numbers as US Dollars (e.g., $1,234.56)
app.jinja_env.filters["usd"] = usd

# Configure Flask session to use filesystem instead of signed cookies
# This is more secure and suitable for storing session data server-side
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database stored in finance.db
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """
    Configure HTTP headers to prevent caching.
    This ensures users always get fresh content and not stale cached pages.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """
    Show the user's portfolio: stocks owned, number of shares, current prices,
    total value per stock, and overall portfolio value including cash.
    """
    # Fetch user's holdings: symbol and total shares owned (only those with shares > 0)
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions \
        WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    # Fetch user's current cash balance
    cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
    )[0]["cash"]

    total_value = cash  # Initialize total portfolio value with cash balance

    # For each stock, look up its current price and calculate total value
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote is None:
            # Defensive fallback: if lookup fails, assign default values
            stock["name"] = stock["symbol"]
            stock["price"] = 0
            stock["value"] = 0
        else:
            stock["name"] = quote["name"]
            stock["price"] = quote["price"]
            stock["value"] = quote["price"] * stock["total_shares"]
        # Add this stock's value to total portfolio value
        total_value += stock["value"]

    # Render portfolio template passing stocks, cash, and calculated total value
    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """
    Allow a user to buy shares of a stock.
    Handles both GET (show form) and POST (process purchase).
    """
    if request.method == "POST":
        # Get stock symbol and number of shares from form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("Symbol is required", 400)
        symbol = symbol.upper()  # Normalize symbol to uppercase

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must be a positive number of shares", 400)

        shares = int(shares)

        # Look up the current stock price
        quote = lookup(symbol)
        if quote is None:
            return apology("Symbol not found", 400)

        price = quote["price"]
        total_cost = shares * price

        # Check if user has sufficient cash to buy
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"]

        if cash < total_cost:
            return apology("You don't have enough cash", 400)

        # Deduct total cost from user's cash
        db.execute(
            "UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
            total_cost=total_cost,
            user_id=session["user_id"]
        )

        # Record the transaction in transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=price
        )

        # Flash a success message indicating the purchase
        flash(f"Bought {shares} shares of {symbol} costing {usd(total_cost)}!")
        return redirect("/")
    else:
        # GET request: render buy form
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """
    Display history of all user's transactions, including buys and sells,
    with stock symbol, shares, price, and timestamp.
    """
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"]
    )

    # Render history page with transactions data
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in by verifying username and password.
    On successful login, stores user_id in session.
    """
    # Clear any existing user session
    session.clear()

    if request.method == "POST":
        # Validate username and password presence
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        if not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query user from database by username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Check that user exists and password matches hash
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

        # Store user id in session to signify login
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        # GET request: render login form
        return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log user out by clearing the session.
    """
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """
    Allow user to get a stock quote.
    GET renders form, POST processes form and shows quote.
    """
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required", 400)
        symbol = symbol.upper()

        # Look up stock quote
        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol", 400)

        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user with a unique username and password.
    Passwords are hashed securely before storage.
    """
    # Clear session to avoid confusion
    session.clear()

    if request.method == "POST":
        # Validate inputs
        if not request.form.get("username"):
            return apology("Username is required", 400)
        if not request.form.get("password"):
            return apology("Password is required", 400)
        if not request.form.get("confirmation"):
            return apology("You must confirm your password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        if len(rows) != 0:
            return apology("Username already exists", 400)

        # Insert new user with hashed password
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"),
                   generate_password_hash(request.form.get("password")))

        # Re-fetch user from database to get user id
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Log the user in immediately after registration
        session["user_id"] = rows[0]["id"]
        flash("Registered successfully! Please log in.")
        return redirect("/login")
    else:
        # GET request: render registration form
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """
    Allow user to sell shares of stock they own.
    Validates that user has sufficient shares.
    """
    # Fetch user's current holdings (stocks with shares > 0)
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("Symbol is required", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must be a positive number of shares", 400)

        shares = int(shares)

        # Check user owns enough shares to sell
        for stock in stocks:
            if stock["symbol"] == symbol.upper():
                if stock["total_shares"] < shares:
                    return apology("You don't have enough shares", 400)

                quote = lookup(symbol)
                if not quote:
                    return apology("Symbol not found", 400)

                price = quote["price"]
                total_sale = shares * price

                # Update user's cash balance to reflect the sale
                db.execute(
                    "UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                    total_sale=total_sale,
                    user_id=session["user_id"]
                )

                # Record sell transaction with negative shares
                db.execute(
                    "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"],
                    symbol=symbol.upper(),
                    shares=-shares,
                    price=price
                )

                flash(
                    f"Sold {shares} shares of {symbol.upper()} for {usd(total_sale)}!")
                return redirect("/")

        # Symbol was not found in user's holdings
        return apology("Symbol not found", 400)
    else:
        # GET request: render sell form with stocks owned listed
        return render_template("sell.html", stocks=stocks)
