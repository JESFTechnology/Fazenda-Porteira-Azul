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


# -------------------------
# Helpers
# -------------------------
def _to_int_or_none(val):
    if val is None or val == "" or str(val).lower() == "none":
        return None
    try:
        return int(val)
    except Exception:
        try:
            return int(float(val))
        except Exception:
            return None


def _to_float_or_none(val):
    if val is None or val == "" or str(val).lower() == "none":
        return None
    try:
        return float(val)
    except Exception:
        return None


# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET"])
def login():
    try:
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
    user, success = db.auth_with_email_and_password(email, password)
    if success and user:
        session["logged_in"] = True
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["email"] = user[2]
        session["id_user_type_fk"] = user[4]
        session["id_employee_fk"] = user[5]
        return redirect("/main")
    return render_template("login.html", error=user)


@app.route("/main", methods=["GET"])
def main():
    return render_template(
        "main.html", username=session.get("username"), list_materials=[]
    )


# -------------------------
# Estoque
# -------------------------
@app.route("/estoque", methods=["GET"])
def estoque():
    try:
        db.connect()
        cursor = db.get_cursor()
        query = """
        SELECT s.id_storage AS id, CONCAT(g.name, " ", g.`type`) AS name,
           s.quantity_bags, sl.name AS local, s.id_grain_fk, s.id_location_fk
        FROM storage s
        LEFT JOIN storagelocations sl ON sl.id_storage_location = s.id_location_fk
        LEFT JOIN grains g ON g.id_grain = s.id_grain_fk
        ORDER BY s.id_storage DESC;
        """
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

        cursor.execute("SELECT id_storage_location, name FROM storagelocations;")
        locations = [
            {"id_storage_location": r[0], "name": r[1]} for r in cursor.fetchall()
        ]

        cursor.execute("SELECT id_grain, name, type FROM grains;")
        grains = cursor.fetchall()
        list_grains = [{"id_grain": g[0], "name": f"{g[1]} {g[2]}"} for g in grains]

        return render_template(
            "estoque.html",
            list_storage=list_storage,
            locations=locations,
            list_grains=list_grains,
            list_storage_local=locations,
        )
    except Exception as e:
        return render_template("erro404.html", msg=e)
    finally:
        try:
            db.close()
        except:
            pass


@app.route("/estoque-gerenciamento", methods=["POST"])
def estoque_gerenciamento():
    id_storage = request.form.get("id_storage")
    grain = request.form.get("grain")
    amount = request.form.get("amount")
    location = request.form.get("location")
    button = request.form.get("button")

    id_val = _to_int_or_none(id_storage)
    grain_val = _to_int_or_none(grain)
    amount_val = _to_int_or_none(amount)
    location_val = _to_int_or_none(location)

    try:
        db.connect()
        cursor = db.get_cursor()

        if button == "Adicionar":
            query = "INSERT INTO storage (id_grain_fk, quantity_bags, id_location_fk, entry_date) VALUES (%s, %s, %s, NOW());"
            cursor.execute(query, (grain_val, amount_val, location_val))
            db.commit()

        elif button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM storage WHERE id_storage = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Editar", "Salvar"):
            if id_val is not None:
                query = "UPDATE storage SET id_grain_fk = %s, id_location_fk = %s, quantity_bags = %s WHERE id_storage = %s;"
                cursor.execute(query, (grain_val, location_val, amount_val, id_val))
                db.commit()

    except Exception as e:
        print("estoque_gerenciamento error:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/estoque")


@app.route("/estoque-local-gerenciamento", methods=["POST"])
def estoque_local_gerenciamento():
    id_location = request.form.get("id_storage")
    nome_local = request.form.get("nome_local")
    button = request.form.get("button")

    id_val = _to_int_or_none(id_location)

    try:
        db.connect()
        cursor = db.get_cursor()

        if button == "Adicionar":
            query = "INSERT INTO storagelocations (name) VALUES (%s);"
            cursor.execute(query, (nome_local,))
            db.commit()

        elif button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM storagelocations WHERE id_storage_location = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Editar", "Salvar"):
            if id_val is not None:
                query = "UPDATE storagelocations SET name = %s WHERE id_storage_location = %s;"
                cursor.execute(query, (nome_local, id_val))
                db.commit()

    except Exception as e:
        print("estoque_local_gerenciamento error:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/estoque")


# -------------------------
# Funcionário
# -------------------------
@app.route("/funcionario", methods=["GET"])
def funcionario():
    try:
        db.connect()
        cursor = db.get_cursor()
        query = """
        SELECT u.id_user AS id, e.name, u.email, ut.description, u.activity
        FROM users AS u INNER JOIN usertype AS ut ON ut.id_user_type = u.id_user_type_fk INNER JOIN employees AS e ON e.id_employee = u.id_employee_fk;
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        list_employees = [
            {"id": emp[0], "name": emp[1], "email": emp[2], "desc": emp[3], "activity":  "Ativo " if int(emp[4]) == 1 else "Inativo"}
            for emp in employees
        ]
        query = """
        SELECT employees.id_employee, employees.NAME, employees.cpf, employees.job, employees.base_salary, employees.weekly_hours, employees.hire_date, crops.name, crops.id_crop 
        FROM employees INNER JOIN crops ON id_crop_fk=crops.id_crop;
        """
        cursor.execute(query)
        employees_no_perfil = cursor.fetchall()
        list_employees_no_perfil = [
            {
                "id_employee": usr[0],
                "name": usr[1],
                "cpf": usr[2],
                "job": usr[3],
                "base_salary": usr[4],
                "weekly_hours": usr[5],
                "hire_date": usr[6],
                "name_crop_fk": usr[7],
                "id_crop_fk":usr[8]
            }
            for usr in employees_no_perfil
        ]

        query = """
        SELECT id_user_type, DESCRIPTION FROM usertype;
        """
        cursor.execute(query)
        usertype = cursor.fetchall()
        list_usertype = [
            {"id_user_type": usr[0], "description": usr[1]} for usr in usertype
        ]

        query = """
        SELECT id_crop, name FROM crops;
        """
        cursor.execute(query)
        usertype = cursor.fetchall()
        list_crop = [
            {"id_crop": usr[0], "description": usr[1]} for usr in usertype
        ]

        return render_template(
            "funcionario.html",
            list_employees=list_employees,
            list_employees_no_perfil=list_employees_no_perfil,
            list_usertype=list_usertype,
            locations=list_crop
        )
    except Exception as e:
        return render_template("erro404.html", msg=e)
    finally:
        try:
            db.close()
        except:
            pass


@app.route("/funcionario-gerenciamento", methods=["POST"])
def funcionario_gerenciamento():
    """
    Rota para gerenciar funcionários (INSERT, UPDATE, DELETE)
    """
    id_employee = request.form.get("id_employee")
    name = request.form.get("name")
    cpf = request.form.get("cpf")
    job = request.form.get("job")
    salary = request.form.get("salary")
    weekly_hours = request.form.get("weekly_hours")
    hire_date = request.form.get("hire_date")
    crop_location = request.form.get("crop_location")
    button = request.form.get("button")

    id_val = _to_int_or_none(id_employee)
    salary_val = _to_float_or_none(salary)
    weekly_hours_val = _to_int_or_none(weekly_hours)
    crop_location_val = _to_int_or_none(crop_location)

    try:
        db.connect()
        cursor = db.get_cursor()

        if button == "Adicionar":
            # INSERT novo funcionário
            query = """
                INSERT INTO employees (name, cpf, job, base_salary, weekly_hours, hire_date, id_crop_fk)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            params = (name, cpf, job, salary_val, weekly_hours_val, hire_date, crop_location_val)
            cursor.execute(query, params)
            db.commit()
            print(f"✅ Funcionário '{name}' adicionado com sucesso!")

        elif button in ("Remover", "Excluir"):
            # DELETE funcionário
            if id_val is not None:
                query = "DELETE FROM employees WHERE id_employee = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Editar", "Salvar"):
            # UPDATE funcionário
            if id_val is not None:
                query = """
                    UPDATE employees
                    SET name = %s,
                        cpf = %s,
                        job = %s,
                        base_salary = %s,
                        weekly_hours = %s,
                        hire_date = %s,
                        id_crop_fk = %s
                    WHERE id_employee = %s;
                """
                params = (name, cpf, job, salary_val, weekly_hours_val, hire_date, crop_location_val, id_val)
                cursor.execute(query, params)
                db.commit()

    except Exception as e:
        pass
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/funcionario")


@app.route("/usertype-gerenciamento", methods=["POST"])
def usertype_gerenciamento():
    """
    Rota para gerenciar tipos de usuário (INSERT, UPDATE, DELETE)
    """
    id_user_type = request.form.get("id_user_type")
    description = request.form.get("description")
    button = request.form.get("button")

    id_val = _to_int_or_none(id_user_type)

    try:
        db.connect()
        cursor = db.get_cursor()

        if button == "Adicionar":
            # INSERT novo tipo de usuário
            query = "INSERT INTO usertype (DESCRIPTION) VALUES (%s);"
            cursor.execute(query, (description,))
            db.commit()

        elif button in ("Remover", "Excluir"):
            # DELETE tipo de usuário
            if id_val is not None:
                query = "DELETE FROM usertype WHERE id_user_type = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Editar", "Salvar"):
            # UPDATE tipo de usuário
            if id_val is not None:
                query = "UPDATE usertype SET DESCRIPTION = %s WHERE id_user_type = %s;"
                cursor.execute(query, (description, id_val))
                db.commit()

    except Exception as e:
        pass
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/funcionario")


# -------------------------
# Maquinário (GET)
# -------------------------
@app.route("/maquinario", methods=["GET"])
def maquinario():
    try:
        db.connect()
        cursor = db.get_cursor()

        # usage
        query = """
        SELECT mu.id_machinery_usage, mu.usage_date, mu.hours_usage, mu.fuel_consumed, mu.observation,
               CONCAT(m.model, " / ", m.`year`) AS machinery, e.name AS employees,
               mu.id_machinery_fk, mu.id_employee_fk
        FROM machineryusage AS mu
        INNER JOIN machinery AS m ON mu.id_machinery_fk = m.id_machinery
        INNER JOIN employees AS e ON e.id_employee = mu.id_employee_fk;
        """
        cursor.execute(query)
        list_machineryusage = []
        for row in cursor.fetchall():
            list_machineryusage.append(
                {
                    "id_machinery_usage": row[0],
                    "usage_date": row[1],
                    "hours_usage": row[2],
                    "fuel_consumed": row[3],
                    "observation": row[4],
                    "machinery": row[5],
                    "employees": row[6],
                    "id_machinery_fk": row[7],
                    "id_employee_fk": row[8],
                }
            )

        # brands
        cursor.execute("SELECT id_machinery_brand, name FROM machinerybrand;")
        list_machinerybrand = [
            {"id_machinery_brand": r[0], "name": r[1]} for r in cursor.fetchall()
        ]

        # types
        cursor.execute("SELECT id_machinery_type, name FROM machinerytype;")
        list_id_machinery_type = [
            {"id_machinery_type": r[0], "name": r[1]} for r in cursor.fetchall()
        ]

        # machinery list
        query = """
        SELECT m.id_machinery, m.model, m.`year`, m.total_worked_hours, m.total_fuel_consumption,
               mb.id_machinery_brand, mt.id_machinery_type, mb.name AS machinery_brand, mt.name AS machinery_type
        FROM machinery m
        INNER JOIN machinerybrand AS mb ON m.id_machinery_brand_fk = mb.id_machinery_brand
        INNER JOIN machinerytype AS mt ON m.id_machinery_type_fk = mt.id_machinery_type;
        """
        cursor.execute(query)
        list_machinery = []
        for row in cursor.fetchall():
            list_machinery.append(
                {
                    "id_machinery": row[0],
                    "model": row[1],
                    "year": row[2],
                    "total_worked_hours": row[3],
                    "total_fuel_consumption": row[4],
                    "machinery_brand_fk": row[7],  # name
                    "machinery_type_fk": row[8],  # name
                    "brand_id": row[5],
                    "type_id": row[6],
                }
            )

        # employee list for selects
        cursor.execute("SELECT id_employee, name FROM employees;")
        employee_list = [{"name": r[1], "id_employee": r[0]} for r in cursor.fetchall()]

        # machinery selects
        cursor.execute("SELECT id_machinery, CONCAT(model,' / ',year) FROM machinery;")
        machinery_list = [
            {"model": r[1], "id_machinery": r[0]} for r in cursor.fetchall()
        ]

        return render_template(
            "maquinario.html",
            machinery_list=machinery_list,
            employee_list=employee_list,
            list_machinery=list_machinery,
            list_machineryusage=list_machineryusage,
            list_machinerybrand=list_machinerybrand,
            list_id_machinery_type=list_id_machinery_type,
        )
    except Exception as e:
        return render_template("erro404.html", msg=e)
    finally:
        try:
            db.close()
        except:
            pass


# -------------------------
# Maquinário (USO) - POST (Insert / Update / Delete)
# -------------------------
@app.route("/maquinario-gerenciamento-uso", methods=["POST"])
def maquinario_gerenciamento_uso():
    id_val = _to_int_or_none(request.form.get("id_machinery_usage"))
    usage_date = request.form.get("usage_date") or None
    hours_usage = _to_float_or_none(request.form.get("hours_usage"))
    fuel_consumed = _to_float_or_none(request.form.get("fuel_consumed"))
    observation = request.form.get("observation") or None
    id_machinery_fk = _to_int_or_none(request.form.get("id_machinery_fk"))
    id_employee_fk = _to_int_or_none(request.form.get("id_employee_fk"))
    button = request.form.get("button")

    try:
        db.connect()
        cursor = db.get_cursor()

        if button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM machineryusage WHERE id_machinery_usage = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif id_val is not None:
            # Edit / Save
            query = """
                UPDATE machineryusage
                SET usage_date = %s,
                    hours_usage = %s,
                    fuel_consumed = %s,
                    observation = %s,
                    id_machinery_fk = %s,
                    id_employee_fk = %s
                WHERE id_machinery_usage = %s;
            """
            params = (
                usage_date,
                hours_usage,
                fuel_consumed,
                observation,
                id_machinery_fk,
                id_employee_fk,
                id_val,
            )
            cursor.execute(query, params)
            db.commit()

        else:
            # Insert
            query = """
                INSERT INTO machineryusage (usage_date, hours_usage, fuel_consumed, observation, id_machinery_fk, id_employee_fk)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            params = (
                usage_date,
                hours_usage,
                fuel_consumed,
                observation,
                id_machinery_fk,
                id_employee_fk,
            )
            cursor.execute(query, params)
            db.commit()

    except Exception as e:
        print("Error maquinario_gerenciamento_uso:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/maquinario")


# -------------------------
# Maquinário (CRUD) - POST (Insert / Update)
# -------------------------
@app.route("/maquinario-gerenciamento", methods=["POST"])
def maquinario_gerenciamento():
    id_val = _to_int_or_none(request.form.get("id_machinery"))
    model = request.form.get("model") or None
    year = _to_int_or_none(request.form.get("year"))
    total_worked_hours = _to_float_or_none(request.form.get("total_worked_hours"))
    total_fuel_consumption = _to_float_or_none(
        request.form.get("total_fuel_consumption")
    )
    brand_m = _to_int_or_none(request.form.get("brand"))
    type_m = _to_int_or_none(request.form.get("type"))
    button = request.form.get("button")

    try:
        db.connect()
        cursor = db.get_cursor()

        if id_val is not None and (
            button in ("Editar", "Salvar", "Salvar/Editar", "Salvar ") or button is None
        ):
            # Update
            query = """
                UPDATE machinery
                SET model = %s,
                    year = %s,
                    total_worked_hours = %s,
                    total_fuel_consumption = %s,
                    id_machinery_brand_fk = %s,
                    id_machinery_type_fk = %s
                WHERE id_machinery = %s;
            """
            params = (
                model,
                year,
                total_worked_hours,
                total_fuel_consumption,
                brand_m,
                type_m,
                id_val,
            )
            cursor.execute(query, params)
            db.commit()

        elif button in ("Adicionar", "Add", None) and id_val is None:
            # Insert
            query = """
                INSERT INTO machinery (model, year, total_worked_hours, total_fuel_consumption, id_machinery_brand_fk, id_machinery_type_fk)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            params = (
                model,
                year,
                total_worked_hours,
                total_fuel_consumption,
                brand_m,
                type_m,
            )
            cursor.execute(query, params)
            db.commit()

    except Exception as e:
        print("Error maquinario_gerenciamento:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/maquinario")


# -------------------------
# Brand (CRUD)
# -------------------------
@app.route("/maquinario-gerenciamento-brand", methods=["POST"])
def maquinario_gerenciamento_brand():
    id_val = _to_int_or_none(request.form.get("id_machinery_brand"))
    name = request.form.get("name")
    button = request.form.get("button")

    try:
        db.connect()
        cursor = db.get_cursor()

        if button in ("Adicionar", "Add"):
            query = "INSERT INTO machinerybrand (name) VALUES (%s);"
            cursor.execute(query, (name,))
            db.commit()

        elif button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM machinerybrand WHERE id_machinery_brand = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Salvar", "Editar", "Save"):
            if id_val is not None:
                query = (
                    "UPDATE machinerybrand SET name = %s WHERE id_machinery_brand = %s;"
                )
                cursor.execute(query, (name, id_val))
                db.commit()

    except Exception as e:
        print("maquinario_gerenciamento_brand error:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/maquinario")


# -------------------------
# Type (CRUD)
# -------------------------
@app.route("/maquinario-gerenciamento-type", methods=["POST"])
def maquinario_gerenciamento_type():
    id_val = _to_int_or_none(request.form.get("id_machinery_type"))
    name = request.form.get("name")
    button = request.form.get("button")

    try:
        db.connect()
        cursor = db.get_cursor()

        if button in ("Adicionar", "Add"):
            query = "INSERT INTO machinerytype (name) VALUES (%s);"
            cursor.execute(query, (name,))
            db.commit()

        elif button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM machinerytype WHERE id_machinery_type = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Salvar", "Editar", "Save"):
            if id_val is not None:
                query = (
                    "UPDATE machinerytype SET name = %s WHERE id_machinery_type = %s;"
                )
                cursor.execute(query, (name, id_val))
                db.commit()

    except Exception as e:
        print("maquinario_gerenciamento_type error:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/maquinario")


# -------------------------
# Cotação (CRUD)
# -------------------------
@app.route("/cotacao-gerenciamento", methods=["POST"])
def cotacao_gerenciamento():
    id_val = _to_int_or_none(request.form.get("id_market_quotes"))
    price_per_bag = _to_float_or_none(request.form.get("price_per_bag"))
    quote_date = request.form.get("quote_date")
    observation = request.form.get("observation")
    id_grain_fk = _to_int_or_none(request.form.get("id_grain_fk"))
    button = request.form.get("button")

    try:
        db.connect()
        cursor = db.get_cursor()

        if button in ("Adicionar", "Add"):
            query = "INSERT INTO marketquotes (price_per_bag, quote_date, observation, id_grain_fk) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (price_per_bag, quote_date, observation, id_grain_fk))
            db.commit()

        elif button in ("Remover", "Excluir"):
            if id_val is not None:
                query = "DELETE FROM marketquotes WHERE id_market_quotes = %s;"
                cursor.execute(query, (id_val,))
                db.commit()

        elif button in ("Salvar", "Editar", "Save"):
            if id_val is not None:
                query = "UPDATE marketquotes SET price_per_bag = %s, quote_date = %s, observation = %s, id_grain_fk = %s WHERE id_market_quotes = %s;"
                cursor.execute(
                    query, (price_per_bag, quote_date, observation, id_grain_fk, id_val)
                )
                db.commit()

    except Exception as e:
        print("cotacao_gerenciamento error:", e)
    finally:
        try:
            db.close()
        except:
            pass

    return redirect("/bolsa")


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
    query = """SELECT id_crop,name,area_hectares,current_season FROM crops;"""
    cursor.execute(query)
    list_cropies = []
    cropies = cursor.fetchall()
    for crops in cropies:
        list_cropies.append(
            {
                "id_crop": crops[0],
                "name": crops[1],
                "area_hectares": crops[2],
                "current_season": crops[3],
            }
        )

    db.close()
    return render_template(
        "producao.html",
        list_grains=list_grains,
        list_costtypes=list_costtypes,
        list_productioncosts=list_productioncosts,
        list_cropies=list_cropies,
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
    query = """SELECT * FROM grains;"""
    cursor.execute(query)
    list_grains = []
    grains = cursor.fetchall()
    for grain in grains:
        list_grains.append({"id_grain": grain[0], "name": grain[1], "type": grain[2]})

    return render_template(
        "bolsa.html",
        cotacao=money_coffe_requests(),
        list_marketquotes=list_marketquotes,
        list_grains=list_grains,
    )


# -------------------------
# Exit / Data / Contact
# -------------------------
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
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            db.close()
        except:
            pass


@app.route("/contato", methods=["GET"])
def contato():
    return render_template("contato.html")


# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("erro404.html", msg="Página não encontrada."), 404


if __name__ == "__main__":
    app.run(debug=True)