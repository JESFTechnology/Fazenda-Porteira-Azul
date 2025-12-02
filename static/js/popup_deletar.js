// modal-confirmation.js

// Variáveis para armazenar o contexto da deleção
let currentDeleteAction = null;

// Referências ao Modal e Botões
const modal = document.getElementById("deleteConfirmationModal");
const modalTitle = document.getElementById("modalTitle");
const modalBody = document.getElementById("modalBody");
const confirmButton = document.getElementById("confirmDeleteButton");
const cancelButton = document.getElementById("cancelDeleteButton");

/**
 * Função para configurar e mostrar o modal de confirmação.
 * @param {string} title Título do modal.
 * @param {string} body Mensagem do modal.
 * @param {Function} action Função a ser executada em caso de confirmação.
 */
function showDeleteModal(title, body, action) {
    modalTitle.textContent = title;
    modalBody.textContent = body;
    currentDeleteAction = action; // Armazena a função de ação
    modal.style.display = 'flex'; // Exibe o modal
}

// Oculta o modal ao clicar em Cancelar
cancelButton.addEventListener("click", () => {
    modal.style.display = 'none';
    currentDeleteAction = null; // Limpa a ação
});

// Executa a ação armazenada ao clicar no botão Deletar do modal
confirmButton.addEventListener("click", () => {
    if (currentDeleteAction) {
        currentDeleteAction(); // Executa a função de deleção
    }
    modal.style.display = 'none';
    currentDeleteAction = null; // Limpa a ação
});


// ========================================
// FUNCIONÁRIO - SISTEMA DE DELEÇÃO
// ========================================

// ===== DELETAR FUNCIONÁRIO =====
document.querySelectorAll("[id^='delete_employee_']").forEach(item => {
    item.addEventListener("click", event => {
        event.preventDefault();

        // Extrai o ID do elemento (formato: delete_employee_123)
        const id = item.id.split("_")[2];

        if (id !== null && !isNaN(id)) {
            // Define a função que será executada se o usuário confirmar
            const deleteAction = () => {
                // Cria um formulário temporário para fazer o POST
                const form = document.createElement("form");
                form.method = "POST";
                form.action = "funcionario-gerenciamento";

                // Cria campos ocultos
                const inputId = document.createElement("input");
                inputId.type = "hidden";
                inputId.name = "id_employee";
                inputId.value = id;

                const inputButton = document.createElement("input");
                inputButton.type = "hidden";
                inputButton.name = "button";
                inputButton.value = "Excluir";

                // Adiciona campos ao formulário
                form.appendChild(inputId);
                form.appendChild(inputButton);

                // Adiciona o formulário ao body e envia
                document.body.appendChild(form);
                form.submit();

                console.log("✓ Funcionário ID " + id + " deletado com sucesso!");
            };

            showDeleteModal(
                "Deletar Funcionário",
                "Você tem certeza que deseja remover este funcionário permanentemente?",
                deleteAction
            );
        }
    });
});


// ===== DELETAR TIPO DE USUÁRIO =====
document.querySelectorAll("[id^='delete_usertype_']").forEach(item => {
    item.addEventListener("click", event => {
        event.preventDefault();

        // Extrai o ID do elemento (formato: delete_usertype_123)
        const id = item.id.split("_")[2];

        if (id !== null && !isNaN(id)) {
            // Define a função que será executada se o usuário confirmar
            const deleteAction = () => {
                // Cria um formulário temporário para fazer o POST
                const form = document.createElement("form");
                form.method = "POST";
                form.action = "usertype-gerenciamento";

                // Cria campos ocultos
                const inputId = document.createElement("input");
                inputId.type = "hidden";
                inputId.name = "id_user_type";
                inputId.value = id;

                const inputButton = document.createElement("input");
                inputButton.type = "hidden";
                inputButton.name = "button";
                inputButton.value = "Excluir";

                // Adiciona campos ao formulário
                form.appendChild(inputId);
                form.appendChild(inputButton);

                // Adiciona o formulário ao body e envia
                document.body.appendChild(form);
                form.submit();

                console.log("✓ Tipo de usuário ID " + id + " deletado com sucesso!");
            };

            showDeleteModal(
                "Deletar Tipo de Usuário",
                "Você tem certeza que deseja remover este tipo de usuário permanentemente?",
                deleteAction
            );
        }
    });
});


/* ========================================
   ESTOQUE - SISTEMA DE DELEÇÃO
   ======================================== */

/*popup deletar init*/

    // ===== DELETAR ESTOQUE (MODIFICADO) =====
    document.querySelectorAll("[id^='delete_storage_']").forEach(item => {
        item.addEventListener("click", event => {
            event.preventDefault(); // Evita qualquer ação padrão do link/botão

            const id = item.id.split("_")[2];

            if (id !== null) {
                // Define a função que será executada se o usuário confirmar
                const deleteAction = () => {
                    const id_storage = document.getElementById("id_storage");
                    const btn_submit = document.getElementById("btn-submit");

                    // Executa a lógica de deleção original
                    id_storage.value = id;
                    btn_submit.value = "Remover";
                    btn_submit.click();
                };

                showDeleteModal(
                    "Deletar Estoque",
                    "Você tem certeza que deseja remover este estoque permanentemente?",
                    deleteAction
                );
            }
        });
    });

    // ===== DELETAR LOCAL (MODIFICADO) =====
    document.querySelectorAll("[id^='delete_local_storage_']").forEach(item => {
        item.addEventListener("click", event => {
            event.preventDefault(); // Evita qualquer ação padrão do link/botão

            const id = item.id.split("_")[3];

            if (id !== null) {
                // Define a função que será executada se o usuário confirmar
                const deleteAction = () => {
                    const id_storage_local = document.getElementById("id_storage_local");
                    const btn_submit_local = document.getElementById("btn-submit_local");

                    // Executa a lógica de deleção original
                    id_storage_local.value = id;
                    btn_submit_local.value = "Remover";
                    btn_submit_local.click();
                };

                showDeleteModal(
                    "Deletar Local de Estoque",
                    "Você tem certeza que deseja remover este local de estoque permanentemente?",
                    deleteAction
                );
            }
        });
    });
/*popup deletar fim*/


// ========================================
// MAQUINÁRIO - SISTEMA DE DELEÇÃO
// ========================================

// ===== DELETAR USO DE MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_use_']").forEach(item => {
    // Verifica se é um item de uso de maquinário (id_machinery_usage)
    const id = item.id.split("_")[3];

    // Se o ID for um número válido e maior que 0, é um uso de maquinário
    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery_usage = document.getElementById("id_machinery_usage");
                    const btn_submit = document.getElementById("btn-submit");

                    id_machinery_usage.value = id;
                    btn_submit.value = "Remover";
                    btn_submit.click();
                };

                showDeleteModal(
                    "Deletar Uso de Maquinário",
                    "Você tem certeza que deseja remover este registro de uso de maquinário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});



// ===== EDITAR USO DE MAQUINÁRIO =====
document.querySelectorAll("p[id^='edit_machinery_usage_']").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const usage_date = btn.dataset.usage_date;
        const hours_usage = btn.dataset.hours_usage;
        const fuel_consumed = btn.dataset.fuel_consumed;
        const observation = btn.dataset.observation;
        const id_machinery = btn.dataset.id_machinery;
        const id_employee = btn.dataset.id_employee;

        // Preenche o formulário
        document.getElementById("id_machinery_usage").value = id;
        document.getElementById("usage_date").value = usage_date;
        document.getElementById("hours_usage").value = hours_usage;
        document.getElementById("fuel_consumed").value = fuel_consumed;
        document.getElementById("observation").value = observation;
        document.getElementById("id_machinery_fk").value = id_machinery;
        document.getElementById("id_employee_fk").value = id_employee;

        // Altera o botão para "Editar"
        document.querySelectorAll("input[id='btn-submit'][value='Adicionar']").forEach(btn => {
            btn.value = "Editar";
        });

        console.log("✓ Uso de maquinário carregado para edição: ID " + id);
    });
});



// ===== DELETAR MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_all_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery = document.getElementById("id_machinery");
                    const btn_submit = document.querySelectorAll("input[id='btn-submit']")[1]; // Segundo btn-submit (maquinário)

                    id_machinery.value = id;
                    btn_submit.value = "Remover";
                    btn_submit.click();
                };

                showDeleteModal(
                    "Deletar Maquinário",
                    "Você tem certeza que deseja remover este maquinário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});



// ===== EDITAR MAQUINÁRIO =====
document.querySelectorAll("p[id^='edit_machinery_']").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const model = btn.dataset.model;
        const year = btn.dataset.year;
        const total_worked_hours = btn.dataset.total_worked_hours;
        const total_fuel_consumption = btn.dataset.total_fuel_consumption;
        const brand = btn.dataset.brand;
        const type = btn.dataset.type;

        // Preenche o formulário
        document.getElementById("id_machinery").value = id;
        document.getElementById("model").value = model;
        document.getElementById("year").value = year;
        document.getElementById("total_worked_hours").value = total_worked_hours;
        document.getElementById("total_fuel_consumption").value = total_fuel_consumption;

        // Seleciona as opções corretas nos selects
        document.querySelectorAll("select[name='brand']").forEach(select => {
            select.value = brand;
        });
        document.querySelectorAll("select[name='type']").forEach(select => {
            select.value = type;
        });

        // Altera o botão para "Editar"
        document.querySelectorAll("input[id='btn-submit'][value='Adicionar']").forEach(btn => {
            btn.value = "Editar";
        });

        console.log("✓ Maquinário carregado para edição: ID " + id);
    });
});



// ===== DELETAR MARCA DE MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_brand_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery_brand = document.getElementById("id_machinery_brand_form");
                    const btn_submit_brand = document.querySelectorAll("input[id='btn-submit']")[2]; // Terceiro btn-submit (marca)

                    id_machinery_brand.value = id;
                    btn_submit_brand.value = "Remover";
                    btn_submit_brand.click();
                };

                showDeleteModal(
                    "Deletar Marca de Maquinário",
                    "Você tem certeza que deseja remover esta marca de maquinário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});



// ===== EDITAR MARCA DE MAQUINÁRIO =====
document.querySelectorAll("p[id^='edit_brand_']").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const name = btn.dataset.name;

        // Preenche o formulário
        document.getElementById("id_machinery_brand_form").value = id;
        document.getElementById("brand_name").value = name;

        // Altera o botão para "Editar"
        document.querySelectorAll("input[id='btn-submit'][value='Adicionar']").forEach(btn => {
            btn.value = "Editar";
        });

        console.log("✓ Marca carregada para edição: ID " + id);
    });
});



// ===== DELETAR TIPO DE MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_type_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery_type = document.getElementById("id_machinery_type_form");
                    const btn_submit_type = document.querySelectorAll("input[id='btn-submit']")[3]; // Quarto btn-submit (tipo)

                    id_machinery_type.value = id;
                    btn_submit_type.value = "Remover";
                    btn_submit_type.click();
                };

                showDeleteModal(
                    "Deletar Tipo de Maquinário",
                    "Você tem certeza que deseja remover este tipo de maquinário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});