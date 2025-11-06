class User:
    def __init__(self, id_user, username, email, id_user_type_fk, id_employee_fk):
        self.id_user = id_user
        self.username = username
        self.email = email
        self.id_user_type_fk = id_user_type_fk
        self.id_employee_fk = id_employee_fk

    def serialize(user):
        return {
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "id_user_type_fk": user.id_user_type_fk,
            "id_employee_fk": user.id_employee_fk,
        }

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __str__(self):
        return f"User(id_user={self.id_user}, username={self.username}, email={self.email}, id_user_type_fk={self.id_user_type_fk}, id_employee_fk={self.id_employee_fk})"
