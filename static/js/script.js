if (localStorage.getItem("theme") == "dark") {
    console.log("Dark mode activated");
    document.getElementById("theme").innerText = "Tema: Escuro";
    document.getElementById("stylesheet_body").href =
        `./../static/css/dark-style.css`;
    document.getElementById("stylesheet_body_storage").href =
        `{{url_for('static', filename='css/dark-style-estoque.css')}}`;
} else {
    document.getElementById("theme").innerText = "Tema: Claro";
    document.getElementById("stylesheet_body").href =
        `./../static/css/style.css`;
    document.getElementById("stylesheet_body_storage").href =
        `{{url_for('static', filename='css/style-estoque.css')}}`;
}

document.getElementById("theme").addEventListener("click", () => {
    if (localStorage.getItem("theme") == "dark") {
        localStorage.setItem("theme", "light");
        document.getElementById("stylesheet_body").href =
            `./../static/css/style.css`;
        document.getElementById("stylesheet_body_storage").href =
            `{{url_for('static', filename='css/style-estoque.css')}}`;
        document.getElementById("theme").innerText = "Tema: Claro";
    } else {
        localStorage.setItem("theme", "dark");
        document.getElementById("stylesheet_body").href =
            `./../static/css/dark-style.css`;
        document.getElementById("stylesheet_body_storage").href =
            `{{url_for('static', filename='css/dark-style-estoque.css')}}`;
        document.getElementById("theme").innerText = "Tema: Escuro";
    } });