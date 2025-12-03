// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                       POPUP_DELETAR.JS - COMPLETO                          ║
// ║        Sistema de Confirmação e Deleção para Todos os Módulos             ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== FUNÇÃO GLOBAL DE MODAL =====
function showDeleteModal(title, message, deleteAction) {
    const modal = document.getElementById("deleteConfirmationModal");
    if (!modal) {
        console.error("Modal 'deleteConfirmationModal' não encontrado!");
        return;
    }

    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalBody").textContent = message;

    const confirmBtn = document.getElementById("confirmDeleteButton");
    const cancelBtn = document.getElementById("cancelDeleteButton");

    const handleConfirm = () => {
        deleteAction();
        modal.style.display = "none";
        confirmBtn.removeEventListener("click", handleConfirm);
        cancelBtn.removeEventListener("click", handleCancel);
    };

    const handleCancel = () => {
        modal.style.display = "none";
        confirmBtn.removeEventListener("click", handleConfirm);
        cancelBtn.removeEventListener("click", handleCancel);
    };

    confirmBtn.addEventListener("click", handleConfirm);
    cancelBtn.addEventListener("click", handleCancel);

    modal.style.display = "flex";
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                            MÓDULO: ESTOQUE                                ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== DELETAR ESTOQUE =====
document.querySelectorAll("[id^='delete_storage_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_storage = document.getElementById("id_storage_form");
                    const btn_submit_storage = document.querySelectorAll("input[id='btn-submit']")[0]; // Primeiro btn-submit (estoque)

                    id_storage.value = id;
                    btn_submit_storage.value = "Remover";
                    btn_submit_storage.click();
                };

                showDeleteModal(
                    "Deletar Estoque",
                    "Você tem certeza que deseja remover este item de estoque permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ===== DELETAR LOCAL DE ARMAZENAMENTO =====
document.querySelectorAll("[id^='delete_local_storage_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_local_storage = document.getElementById("id_local_storage_form");
                    const btn_submit_local = document.querySelectorAll("input[id='btn-submit']")[1]; // Segundo btn-submit (local)

                    id_local_storage.value = id;
                    btn_submit_local.value = "Remover";
                    btn_submit_local.click();
                };

                showDeleteModal(
                    "Deletar Local de Armazenamento",
                    "Você tem certeza que deseja remover este local de armazenamento permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                         MÓDULO: FUNCIONÁRIO                               ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== DELETAR FUNCIONÁRIO =====
document.querySelectorAll("[id^='delete_employee_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "funcionario-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_employee";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

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
    }
});

// ===== DELETAR TIPO DE USUÁRIO =====
document.querySelectorAll("[id^='delete_usertype_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "usertype-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_user_type";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Tipo de Usuário ID " + id + " deletado com sucesso!");
                };

                showDeleteModal(
                    "Deletar Tipo de Usuário",
                    "Você tem certeza que deseja remover este tipo de usuário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                          MÓDULO: PRODUÇÃO                                 ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== DELETAR GRÃO =====
document.querySelectorAll("[id^='delete_grain_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "producao-grains-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_grain";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Grão ID " + id + " deletado com sucesso!");
                };

                showDeleteModal(
                    "Deletar Grão",
                    "Você tem certeza que deseja remover este grão permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ===== DELETAR TIPO DE CUSTO =====
document.querySelectorAll("[id^='delete_costtype_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "producao-costtype-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_cost_type";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Tipo de Custo ID " + id + " deletado com sucesso!");
                };

                showDeleteModal(
                    "Deletar Tipo de Custo",
                    "Você tem certeza que deseja remover este tipo de custo permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ===== DELETAR CUSTO DE PRODUÇÃO =====
document.querySelectorAll("[id^='delete_cost_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "producao-cost-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_production_cost";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Custo de Produção ID " + id + " deletado com sucesso!");
                };

                showDeleteModal(
                    "Deletar Custo de Produção",
                    "Você tem certeza que deseja remover este custo de produção permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ===== DELETAR TALHÃO =====
document.querySelectorAll("[id^='delete_crop_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "producao-crop-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_crop";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Talhão ID " + id + " deletado com sucesso!");
                };

                showDeleteModal(
                    "Deletar Talhão",
                    "Você tem certeza que deseja remover este talhão permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           MÓDULO: BOLSA/COTAÇÃO                           ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== DELETAR COTAÇÃO =====
document.querySelectorAll("[id^='delete_quote_']").forEach(item => {
    const id = item.id.split("_")[2];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const form = document.createElement("form");
                    form.method = "POST";
                    form.action = "bolsa-cotacao-gerenciamento";

                    const inputId = document.createElement("input");
                    inputId.type = "hidden";
                    inputId.name = "id_market_quotes";
                    inputId.value = id;

                    const inputButton = document.createElement("input");
                    inputButton.type = "hidden";
                    inputButton.name = "button";
                    inputButton.value = "Excluir";

                    form.appendChild(inputId);
                    form.appendChild(inputButton);

                    document.body.appendChild(form);
                    form.submit();

                    console.log("✓ Cotação ID " + id + " deletada com sucesso!");
                };

                showDeleteModal(
                    "Deletar Cotação",
                    "Você tem certeza que deseja remover esta cotação permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                         MÓDULO: MAQUINÁRIO                                ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// ===== DELETAR USO DE MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_use_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery_use = document.getElementById("id_machinery_use_form");
                    const btn_submit_use = document.querySelectorAll("input[id='btn-submit']")[0]; // Primeiro btn-submit (uso)

                    id_machinery_use.value = id;
                    btn_submit_use.value = "Remover";
                    btn_submit_use.click();
                };

                showDeleteModal(
                    "Deletar Uso de Maquinário",
                    "Você tem certeza que deseja remover este uso de maquinário permanentemente?",
                    deleteAction
                );
            }
        });
    }
});

// ===== DELETAR MAQUINÁRIO =====
document.querySelectorAll("[id^='delete_machinery_all_']").forEach(item => {
    const id = item.id.split("_")[3];

    if (id !== null && !isNaN(id)) {
        item.addEventListener("click", event => {
            event.preventDefault();

            if (id !== null) {
                const deleteAction = () => {
                    const id_machinery = document.getElementById("id_machinery_form");
                    const btn_submit_machinery = document.querySelectorAll("input[id='btn-submit']")[1]; // Segundo btn-submit (maquinário)

                    id_machinery.value = id;
                    btn_submit_machinery.value = "Remover";
                    btn_submit_machinery.click();
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

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           FIM DO ARQUIVO                                  ║
// ╚════════════════════════════════════════════════════════════════════════════╝

console.log("✅ popup_deletar.js carregado com sucesso!");
console.log("📊 Módulos carregados: ESTOQUE | FUNCIONÁRIO | PRODUÇÃO | BOLSA | MAQUINÁRIO");