from src.database import DatabaseConnection
from flask import Flask, jsonify, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "QUYFCUQCQGWCQBWXJHCIsndjsbcajnka"  # Replace with a strong, random key

db_config = {
    "host": "localhost",
    "database": "blueGateFarm",
    "user": "root",
    "password": "",
}
db = DatabaseConnection(**db_config)


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET"])
def login():
    try:
        print("User logged in:", session["username"])
        if "logged_in" in session and session.get("logged_in"):
            return redirect("/main")
        return render_template("login.html")
    except KeyError:
        return render_template("login.html")


@app.route("/login-check", methods=["POST"])
def login_data():
    global db
    email = request.form.get("email")
    password = request.form.get("password")
    # if email == "demo@gmail.com" or password == "demo123":
    #    return redirect("/demo-main")
    user, success = db.auth_with_email_and_password(email, password)
    if success and user:
        session["logged_in"] = True
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["email"] = user[2]
        session["id_user_type_fk"] = user[4]
        session["id_employee_fk"] = user[5]

        print("User logged in:", session["username"])
        return redirect("/main")
    return render_template("login.html", error=user)


@app.route("/main", methods=["GET"])
def main():
    return render_template("main.html")


@app.route("/estoque", methods=["GET"])
def estoque():
    return render_template("estoque.html")


@app.route("/funcionario", methods=["GET"])
def funcionario():
    return render_template("funcionario.html")

@app.route("/exit", methods=["GET"])
def exit():
    session.clear()
    return redirect("/")

@app.route("/data", methods=["GET"])
def get_data():
    try:
        db.connect()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM my_table")
        results = cursor.fetchall()
        db.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
