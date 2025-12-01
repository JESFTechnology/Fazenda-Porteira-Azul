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
    return render_template(
        "main.html", username=session.get("username"), list_materials=[]
    )


@app.route("/estoque", methods=["GET"])
def estoque():
    try:
        db.connect()
        cursor = db.get_cursor()
    except Exception as e:
        return render_template("erro404.html", msg=e)
    query = """
    SELECT s.id_storage AS id, CONCAT(g.name, " ", g.`type`) AS name, 
       s.quantity_bags, 
       sl.name AS local, s.id_grain_fk, s.id_location_fk
    FROM storage s LEFT JOIN storagelocations sl ON sl.id_storage_location = s.id_location_fk LEFT JOIN grains g ON g.id_grain = s.id_grain_fk ORDER BY s.id_storage DESC;"""
    cursor.execute(query)
    list_storage = []
    materials = cursor.fetchall()
    for material in materials:
        list_storage.append(
            {
                "id": material[0],
                "name": material[1],
                "quantity_bags": material[2],
                "local": material[3],
                "id_grain": material[4],
                "id_location": material[5],
            }
        )
    cursor.execute("SELECT * FROM storagelocations;")
    locations = []
    storagelocations = cursor.fetchall()
    for storagelocation in storagelocations:
        locations.append(
            {"id_storage_location": storagelocation[0], "name": storagelocation[1]}
        )

    cursor.execute("SELECT * FROM grains;")
    list_grains = []
    grains = cursor.fetchall()
    for grain in grains:
        list_grains.append({"id_grain": grain[0], "name": grain[1] + " " + grain[2]})
    db.close()
    return render_template(
        "estoque.html",
        list_storage=list_storage,
        locations=locations,
        list_grains=list_grains,
    )


@app.route("/estoque-gerenciamento", methods=["POST"])
def estoque_gerenciamento():
    id = request.form.get("id_storage")
    grain = request.form.get("grain")
    amount = request.form.get("amount")
    location = request.form.get("location")
    button = request.form.get("button")
    if button == "Adicionar":
        db.connect()
        cursor = db.get_cursor()
        query = f"INSERT INTO storage (id_grain_fk, quantity_bags, id_location_fk, entry_date) VALUES ({int(grain)}, {int(amount)}, {int(location)}, NOW());"
        cursor.execute(query)
        db.commit()
        db.close()
        print(query)
    elif button == "Remover":
        if id is not None:
            db.connect()
            cursor = db.get_cursor()
            query = f"DELETE FROM storage WHERE id_storage = {int(id)};"
            cursor.execute(query)
            db.commit()
            db.close()
            print(query)
        else:
            print("ID is None, cannot remove storage item.")
    elif button == "Editar":
        if id is not None:
            db.connect()
            cursor = db.get_cursor()
            query = f"UPDATE storage SET id_grain_fk = {int(grain)}, id_location_fk = {int(location)}, quantity_bags = {int(amount)} WHERE id_storage = {int(id)};"
            cursor.execute(query)
            db.commit()
            db.close()
    return redirect("/estoque")


@app.route("/funcionario", methods=["GET"])
def funcionario():
    try:
        db.connect()
        cursor = db.get_cursor()
    except Exception as e:
        return render_template("erro404.html", msg=e)
    query = """
    SELECT u.id_user AS id, e.name, u.email, e.job 
    FROM users AS u INNER JOIN employees AS e 
    ON e.id_employee = u.id_employee_fk ORDER BY e.name;"""
    cursor.execute(query)
    list_employees = []
    employees = cursor.fetchall()
    for employee in employees:
        list_employees.append(
            {
                "id": employee[0],
                "name": employee[1],
                "email": employee[2],
                "job": employee[3],
            }
        )
    return render_template("funcionario.html", list_employees=list_employees)


@app.route("/maquinario", methods=["GET"])
def maquinario():
    try:
        db.connect()
        cursor = db.get_cursor()
    except Exception as e:
        return render_template("erro404.html", msg=e)
    query = """
    SELECT id_machinery_usage, usage_date, hours_usage, fuel_consumed, observation, CONCAT(m.model," / ",m.`year`)AS machinery, e.name AS employees FROM machineryusage AS mu INNER JOIN machinery AS m ON mu.id_machinery_fk = m.id_machinery INNER JOIN employees AS e ON e.id_employee = mu.id_employee_fk;"""
    cursor.execute(query)
    list_machinery = []
    machineries = cursor.fetchall()
    for machinery in machineries:
        list_machinery.append(
            {
                "id_machinery_usage": machinery[0],
                "usage_date": machinery[1],
                "hours_usage": machinery[2],
                "fuel_consumed": machinery[3],
                "observation": machinery[4],
                "machinery":machinery[5],
                "employees":machinery[6]
            }
        )
    return render_template("maquinario.html", list_machinery=list_machinery)


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
