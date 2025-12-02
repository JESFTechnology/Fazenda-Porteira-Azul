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


/* Colocar no estoque */


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