from src.database import DatabaseConnection
from src.web import money_coffe_requests
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
        list_storage_local=locations,
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


@app.route("/estoque-local-gerenciamento", methods=["POST"])
def estoque_local_gerenciamento():
    id = request.form.get("id_storage")
    nome_local = request.form.get("nome_local")
    button = request.form.get("button")
    if button == "Adicionar":
        db.connect()
        cursor = db.get_cursor()
        query = f"INSERT INTO storagelocations (name) VALUES ('{nome_local}');"
        cursor.execute(query)
        db.commit()
        db.close()
        print(query)
    elif button == "Remover":
        print("Removendo local de estoque...")
        if id is not None:
            print(f"ID to remove: {id}")
            db.connect()
            cursor = db.get_cursor()
            query = (
                f"DELETE FROM storagelocations WHERE id_storage_location = {int(id)};"
            )
            cursor.execute(query)
            db.commit()
            db.close()
            print(query)
        else:
            print("ID is None, cannot remove storage location.")
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
    list_machineryusage = []
    machineries = cursor.fetchall()
    for machinery in machineries:
        list_machineryusage.append(
            {
                "id_machinery_usage": machinery[0],
                "usage_date": machinery[1],
                "hours_usage": machinery[2],
                "fuel_consumed": machinery[3],
                "observation": machinery[4],
                "machinery": machinery[5],
                "employees": machinery[6],
            }
        )

    query = """
    SELECT id_machinery_brand, name FROM machinerybrand;"""
    cursor.execute(query)

    list_machinerybrand = []
    machinerybrandies = cursor.fetchall()
    for machinerybrand in machinerybrandies:
        list_machinerybrand.append(
            {"id_machinery_brand": machinerybrand[0], "name": machinerybrand[1]}
        )
    list_id_machinery_type = []

    query = """
    SELECT id_machinery_type, name FROM machinerytype;"""
    cursor.execute(query)

    machinerytypes = cursor.fetchall()
    for machinerytype in machinerytypes:
        list_id_machinery_type.append(
            {"id_machinery_type": machinerytype[0], "name": machinerytype[1]}
        )

    list_machinery = []
    query = """
    SELECT id_machinery, model, `year`, total_worked_hours, total_fuel_consumption, mb.name AS machinery_brand, mt.name AS machinery_type FROM machinery 
INNER JOIN machinerybrand AS mb ON machinery.id_machinery_brand_fk = mb.id_machinery_brand
INNER JOIN machinerytype AS mt ON machinery.id_machinery_type_fk = mt.id_machinery_type;"""
    cursor.execute(query)
    machineries = cursor.fetchall()
    for machinery in machineries:
        list_machinery.append(
            {
                "id_machinery": machinery[0],
                "model": machinery[1],
                "year": machinery[2],
                "total_worked_hours": machinery[3],
                "total_fuel_consumption": machinery[4],
                "machinery_brand_fk": machinery[5],
                "machinery_type_fk": machinery[6],
            }
        )

    query = """SELECT id_employee, name FROM employees;"""
    cursor.execute(query)
    employees = cursor.fetchall()
    employee_list = []
    for employee in employees:
        employee_list.append({"name": employee[1], "id_employee": employee[0]})

    query = """SELECT id_machinery, CONCAT(model,' / ',year) FROM machinery;"""
    cursor.execute(query)
    machinerybrands = cursor.fetchall()
    machinery_list = []
    for machinerybrand in machinerybrands:
        machinery_list.append(
            {"model": machinerybrand[1], "id_machinery": machinerybrand[0]}
        )
    db.close()
    return render_template(
        "maquinario.html",
        machinery_list=machinery_list,
        employee_list=employee_list,
        list_machinery=list_machinery,
        list_machineryusage=list_machineryusage,
        list_machinerybrand=list_machinerybrand,
        list_id_machinery_type=list_id_machinery_type,
    )


@app.route("/producao", methods=["GET"])
def producao():
    try:
        db.connect()
        cursor = db.get_cursor()
    except Exception as e:
        return render_template("erro404.html", msg=e)

    query = """SELECT * FROM grains;"""
    cursor.execute(query)
    list_grains = []
    grains = cursor.fetchall()

    for grain in grains:
        list_grains.append({"id_grain": grain[0], "name": grain[1], "type": grain[2]})

    query = """SELECT * FROM costtypes;"""
    cursor.execute(query)
    list_costtypes = []
    costtypes = cursor.fetchall()

    for costtype in costtypes:
        list_costtypes.append(
            {
                "id_cost_type": costtype[0],
                "name": costtype[1],
                "cost_value": costtype[2],
            }
        )

    query = """SELECT p.id_production_cost, p.cost_date, p.description, c.name FROM productioncosts AS p INNER JOIN costtypes AS c on p.id_cost_type_fk = c.id_cost_type;"""
    cursor.execute(query)
    list_productioncosts = []
    productioncosts = cursor.fetchall()

    for productioncost in productioncosts:
        list_productioncosts.append(
            {
                "id_production_cost": productioncost[0],
                "cost_date": productioncost[1],
                "description": productioncost[2],
                "cost_type_fk": productioncost[3],
            }
        )

    db.close()
    return render_template(
        "producao.html",
        list_grains=list_grains,
        list_costtypes=list_costtypes,
        list_productioncosts=list_productioncosts,
    )


@app.route("/bolsa", methods=["GET"])
def bolsa():
    try:
        db.connect()
        cursor = db.get_cursor()
    except Exception as e:
        return render_template("erro404.html", msg=e)
    query = """SELECT m.id_market_quotes,m.price_per_bag,m.quote_date,m.observation,CONCAT(g.name,' - ',g.type) FROM marketquotes AS m INNER JOIN grains AS g ON m.id_grain_fk = g.id_grain;"""
    cursor.execute(query)
    list_marketquotes = []
    marketquotes = cursor.fetchall()
    for marketquote in marketquotes:
        list_marketquotes.append(
            {
                "id_market_quotes": marketquote[0],
                "price_per_bag": marketquote[1],
                "quote_date": marketquote[2],
                "observation": marketquote[3],
                "grain": marketquote[4],
            }
        )
    return render_template(
        "bolsa.html",
        cotacao=money_coffe_requests(),
        list_marketquotes=list_marketquotes,
    )


@app.route("/maquinario-gerenciamento-uso", methods=["GET"])
def maquinario_gerenciamento_uso():
    id = request.form.get("id_machinery_usage")
    usage_date = request.form.get("usage_date")
    hours_usage = request.form.get("hours_usage")
    fuel_consumed = request.form.get("fuel_consumed")
    observation = request.form.get("observation")
    id_machinery_fk = request.form.get("id_machinery_fk")
    id_employee_fk = request.form.get("id_employee_fk")
    button = request.form.get("button")
    if button == "Adicionar":
        db.connect()
        cursor = db.get_cursor()
        query = f"INSERT INTO machineryusage (usage_date, hours_usage, fuel_consumed, observation, id_machinery_fk, id_employee_fk) VALUES ('{usage_date}', {int(hours_usage)}, {float(fuel_consumed)}, '{observation}', {int(id_machinery_fk)}, {int(id_employee_fk)});"
        cursor.execute(query)
        db.commit()
        db.close()
        print(query)
    elif button == "Remover":
        if id is not None:
            db.connect()
            cursor = db.get_cursor()
            query = f"DELETE FROM machineryusage WHERE id_machinery_usage = {int(id)};"
            cursor.execute(query)
            db.commit()
            db.close()
            print(query)
        else:
            print("ID is None, cannot remove machinery usage item.")
    return redirect("/maquinario")


@app.route("/maquinario-gerenciamento", methods=["GET"])
def maquinario_gerenciamento():
    id = request.form.get("id_machinery")
    model = request.form.get("model")
    year = request.form.get("year")
    total_worked_hours = request.form.get("total_worked_hours")
    total_fuel_consumption = request.form.get("total_fuel_consumption")
    brand_m = request.form.get("brand")
    type_m = request.form.get("type")
    button = request.form.get("button")
    if button == "Adicionar":
        db.connect()
        cursor = db.get_cursor()
        query = """"""
        cursor.execute(query)
        db.commit()
        db.close()


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


# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("erro404.html", msg="Página não encontrada."), 404


if __name__ == "__main__":
    app.run(debug=True)
