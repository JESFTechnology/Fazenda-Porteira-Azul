<script>
        /*popup inicio*/

        const popup = document.getElementById("popup_edit");
        const closePopup = document.getElementById("close_popup");

        document.querySelectorAll(".btn_edit").forEach(btn => {
            btn.addEventListener("click", () => {
            document.getElementById("edit_id").value = btn.dataset.id;
            document.getElementById("edit_name").value = btn.dataset.name;
            document.getElementById("edit_quantity_bags").value = btn.dataset.quantity;
            document.getElementById("edit_local").value = btn.dataset.local;

            popup.style.display = "block";
            });
        });

        closePopup.onclick = () => popup.style.display = "none";
        window.onclick = e => { if(e.target == popup) popup.style.display = "none"; };

        /*popup fim*/
        document.querySelectorAll("[id^='edit_storage_']").forEach(item => {
            item.addEventListener("click", event => {
                const id = item.id.split("_")[2];
                if (id) {
                    const id_storage = document.getElementById("id_storage");
                    id_storage.value = id;

                    const amount_storage = document.getElementById("amount_storage")
                    amount_storage.value = parseInt(document.getElementById(`quantity_bags_${id}`).innerText);
                    
                    
                    const btn_submit = document.getElementById("btn-submit");
                    btn_submit.value = "Editar";

                    const list_grains = {{ list_grains | tojson }};
                    const grain_storage = document.getElementById("form_grain_storage");
                    const selected_id_grain = parseInt(item.id.split("_")[3]);
                    grain_storage.innerHTML = list_grains.map(g =>
                        `<option value="${g.id_grain}" ${g.id_grain === selected_id_grain ? 'selected' : ''}>${g.name}</option>`
                    ).join('');

                    const list_locations = {{ locations | tojson }};
                    const local_storage = document.getElementById("form_local_storage");
                    const selected_id_local = parseInt(item.id.split("_")[4]);
                    local_storage.innerHTML = list_locations.map(l =>
                        `<option value="${l.id_storage_location}" ${l.id_storage_location === selected_id_local ? 'selected' : ''}>${l.name}</option>`
                    ).join('');
                }
            });
        });

        document.getElementById("form_grain_storage").innerHTML = `
            {% for grain in list_grains %}
                <option value="{{ grain.id_grain }}">{{ grain.name }}</option>
            {% endfor %}
        `;

        document.getElementById("form_local_storage").innerHTML = `
            {% for location in locations %}
                <option value="{{ location.id_storage_location }}">{{ location.name }}</option>
            {% endfor %}
        `

        document.querySelectorAll("[id^='delete_storage_']").forEach(item => {
            item.addEventListener("click", event => {
                alert("O item será removido do estoque.");
                const id = item.id.split("_")[2];
                if (id !== null) {
                    const id_storage = document.getElementById("id_storage");
                    id_storage.value = id;
                    const btn_submit = document.getElementById("btn-submit");
                    btn_submit.value = "Remover";
                    btn_submit.click();
                }
            });
        });

        document.getElementById("theme").addEventListener("click", () => {
            if (localStorage.getItem("theme") === "dark") {
                localStorage.setItem("theme", "light");
            } else {
                localStorage.setItem("theme", "dark");
            }
            location.reload();
        });

        console.log(localStorage.getItem("theme"))
        if (localStorage.getItem("theme") == "dark") {
            console.log("Dark mode activated");
            document.getElementById("theme").innerText = "Tema: Escuro";
            document.getElementById("stylesheet_body").href =
                `{{url_for('static', filename='css/dark-style.css')}}`;
            document.getElementById("stylesheet_body_storage").href =
                `{{url_for('static', filename='css/dark-style-estoque.css')}}`;
        } else {
            document.getElementById("theme").innerText = "Tema: Claro";
            document.getElementById("stylesheet_body").href =
                `{{url_for('static', filename='css/style.css')}}`;
            document.getElementById("stylesheet_body_storage").href =
                `{{url_for('static', filename='css/style-estoque.css')}}`;
        }
    </script>