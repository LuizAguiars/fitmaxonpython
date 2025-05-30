document.addEventListener("DOMContentLoaded", function () {
    const acaoInput = document.getElementById("acao");
    const modal = document.getElementById("modal");
    const selectID = document.getElementById("personalSelect");
  
    function abrirModal(acao) {
        modal.classList.remove("hidden");
        acaoInput.value = acao;
  
        if (acao === "incluir") {
            selectID.classList.add("hidden");
            limparCampos();
        } else {
            selectID.classList.remove("hidden");
            preencherCampos(selectID.value);
        }
    }
  
    function fecharModal() {
        modal.classList.add("hidden");
    }
  
    function preencherCampos(idSelecionado) {
        const option = document.querySelector(`#personalSelect option[value="${idSelecionado}"]`);
        if (option) {
            document.getElementById("nome").value = option.dataset.nome;
            document.getElementById("email").value = option.dataset.email;
            document.getElementById("especialidade").value = option.dataset.especialidade;
            document.getElementById("id_unidade").value = option.dataset.unidade;
            document.getElementById("fone").value = option.dataset.fone || ""; // Se você tiver telefone nos dados
            document.getElementById("cep").value = option.dataset.cep || "";   // Se tiver cep também
        }
    }
  
    function limparCampos() {
        document.getElementById("nome").value = "";
        document.getElementById("email").value = "";
        document.getElementById("especialidade").value = "";
        document.getElementById("id_unidade").selectedIndex = 0;
        document.getElementById("fone").value = "";
        document.getElementById("cep").value = "";
    }
  
    // Máscaras reutilizáveis
    function mascaraTelefoneHandler() {
      let v = this.value.replace(/\D/g, "");
      if (v.length > 11) v = v.slice(0, 11);
      v = v.replace(/^(\d{2})(\d)/, "($1) $2");
      v = v.replace(/(\d{5})(\d)/, "$1-$2");
      this.value = v;
    }
  
    function mascaraCEPHandler() {
      let v = this.value.replace(/\D/g, "");
      if (v.length > 8) v = v.slice(0, 8);
      v = v.replace(/(\d{5})(\d)/, "$1-$2");
      this.value = v;
    }
  
    // Aplica máscaras em todos inputs no DOM para telefone e CEP
    document.querySelectorAll('input[name="fone"], input#fone').forEach(function(input) {
      input.removeEventListener('input', mascaraTelefoneHandler);
      input.addEventListener('input', mascaraTelefoneHandler);
    });
  
    document.querySelectorAll('input[name="cep"], input#cep').forEach(function(input) {
      input.removeEventListener('input', mascaraCEPHandler);
      input.addEventListener('input', mascaraCEPHandler);
    });
  
    // listeners globais para modal
    window.abrirModal = abrirModal;
    window.fecharModal = fecharModal;
  
    // Atualiza campos ao mudar seleção
    selectID.addEventListener("change", function () {
        preencherCampos(this.value);
    });
  
    const table = document.querySelector('table');
    const headers = table.querySelectorAll('th');
    const filterableFields = ['Nome', 'Capacidade', 'Plano', 'ID', 'Data de Compra', 'Duração (meses)'];
  
    headers.forEach((header, index) => {
        const headerText = header.textContent.trim();
  
        if (!filterableFields.includes(headerText)) {
            return; // Ignorar campos que não são filtráveis
        }
  
        let icon = header.querySelector('span');
        if (!icon) {
            icon = document.createElement('span');
            icon.style.marginLeft = '8px';
            header.appendChild(icon);
        }
  
        header.addEventListener('click', () => {
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const isAscending = header.dataset.sortDirection === 'asc';
  
            rows.sort((a, b) => {
                const cellA = a.cells[index].textContent.trim().toLowerCase();
                const cellB = b.cells[index].textContent.trim().toLowerCase();
  
                if (cellA < cellB) return isAscending ? -1 : 1;
                if (cellA > cellB) return isAscending ? 1 : -1;
                return 0;
            });
  
            header.dataset.sortDirection = isAscending ? 'desc' : 'asc';
  
            const tbody = table.querySelector('tbody');
            rows.forEach(row => tbody.appendChild(row));
  
            // Atualizar ícone
            icon.textContent = isAscending ? '▼' : '▲';
        });
    });
  });
