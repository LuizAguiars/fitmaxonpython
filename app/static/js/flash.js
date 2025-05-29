// ---------------------- FLASH MESSAGES ---------------------- //
setTimeout(() => {
  const flashMessages = document.querySelectorAll(".flash-messages li, .flash-message");
  flashMessages.forEach(msg => {
    msg.style.transition = "opacity 0.5s ease-out";
    msg.style.opacity = 0;
    setTimeout(() => msg.remove(), 500);
  });
}, 4000); // 4 segundos

// ---------------------- MODAIS GENÉRICOS ---------------------- //
function abrirModal(id) {
  document.getElementById(id).classList.add('active');
  document.getElementById(id).classList.add('active');
}

function fecharModal(id) {
  document.getElementById(id).classList.remove('active');
}

// ---------------------- MODAIS COM INFORMAÇÕES DIRETAS ---------------------- //

// Abrir modal editar unidade via linha de tabela
function abrirModalEditar(id) {
  const linha = document.querySelector(`tr[data-id='${id}']`);
  if (!linha) return;

  document.getElementById('editId').value = id;
  document.getElementById('editNome').value = linha.dataset.nome || '';
  document.getElementById('editEndereco').value = linha.dataset.endereco || '';
  document.getElementById('editCapacidade').value = linha.dataset.capacidade || '';
  document.getElementById('editFone').value = linha.dataset.fone || '';
  document.getElementById('editCidade').value = linha.dataset.cidade || '';
  document.getElementById('editEstado').value = linha.dataset.estado || '';
  document.getElementById('editCep').value = linha.dataset.cep || '';
  document.getElementById('editRegiao').value = linha.dataset.regiao || '';

  document.getElementById('infoId').textContent = id;
  document.getElementById('infoNome').textContent = linha.dataset.nome || '';
  document.getElementById('infoEndereco').textContent = linha.dataset.endereco || '';

  abrirModal('modalEditar');
}

// Abrir modal remover unidade
function abrirModalRemover(id) {
  const linha = document.querySelector(`tr[data-id='${id}']`);
  if (!linha) return;

  document.getElementById('removerIdInput').value = id;
  document.getElementById('removerId').textContent = id;
  document.getElementById('removerNome').textContent = linha.dataset.nome || '';
  document.getElementById('removerEndereco').textContent = linha.dataset.endereco || '';

  abrirModal('modalRemover');
}

function abrirModalEditarPersonal(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('editId').value = id;
    document.getElementById('editNome').value = linha.dataset.nome || '';
    document.getElementById('editEmail').value = linha.dataset.email || '';
    document.getElementById('editEspecialidade').value = linha.dataset.especialidade || '';
    document.getElementById('editUnidade').value = linha.dataset.unidade || '';

    document.getElementById('infoId').textContent = id;
    document.getElementById('infoNome').textContent = linha.dataset.nome || '';

    abrirModal('modalEditar');
}

function abrirModalRemoverPersonal(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('removerIdInput').value = id;
    document.getElementById('removerId').textContent = id;
    document.getElementById('removerNome').textContent = linha.dataset.nome || '';

    abrirModal('modalRemover');
}

function abrirModalEditarUsuario(id) {
  const linha = document.querySelector(`tr[data-id='${id}']`);
  if (!linha) return;

  document.getElementById('editId').value = id;
  document.getElementById('editNome').value = linha.dataset.nome || '';
  document.getElementById('editEmail').value = linha.dataset.email || '';
  document.getElementById('editTelefone').value = linha.dataset.telefone || '';
  document.getElementById('editLogradouro').value = linha.dataset.logradouro || '';
  document.getElementById('editNumero').value = linha.dataset.numero || '';
  document.getElementById('editBairro').value = linha.dataset.bairro || '';
  document.getElementById('editCidade').value = linha.dataset.cidade || '';
  document.getElementById('editEstado').value = linha.dataset.estado || '';
  document.getElementById('editCEP').value = linha.dataset.cep || '';
  document.getElementById('editSexo').value = linha.dataset.sexo || '';
  document.getElementById('editStatus').value = linha.dataset.status || '';
  document.getElementById('editPagamento').value = linha.dataset.pagamento || '0';
  document.getElementById('editUnidade').value = linha.dataset.unidade || '';
  document.getElementById('editPlano').value = linha.dataset.plano || '';
  document.getElementById('editNascimento').value = linha.dataset.nascimento || '';

  document.getElementById('infoId').textContent = id;
  document.getElementById('infoNome').textContent = linha.dataset.nome || '';
  document.getElementById('infoEmail').textContent = linha.dataset.email || '';

  abrirModal('modalEditar');
}

function abrirModalRemoverUsuario(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('removerIdInput').value = id;
    document.getElementById('removerId').textContent = id;
    document.getElementById('removerNome').textContent = linha.dataset.nome || '';

    abrirModal('modalRemover');
}

function abrirModalEditarEquipamento(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('editId').value = id;
    document.getElementById('editNome').value = linha.dataset.nome || '';
    document.getElementById('editDescricao').value = linha.dataset.descricao || '';

    // Formatar a data de compra (DD/MM/YYYY para YYYY-MM-DD)
    const dataCompra = linha.dataset.compra;
    if (dataCompra) {
        const partesData = dataCompra.split('/');
        if (partesData.length === 3) {
            const ano = partesData[2];
            const mes = partesData[1].padStart(2, '0');
            const dia = partesData[0].padStart(2, '0');
            document.getElementById('editDataCompra').value = `${ano}-${mes}-${dia}`;
        } else {
            document.getElementById('editDataCompra').value = '';
        }
    } else {
        document.getElementById('editDataCompra').value = '';
    }

    // Preencher os selects com os IDs
    const unidadeSelect = document.getElementById('editUnidade');
    if (unidadeSelect) {
        unidadeSelect.value = linha.dataset.idunidade || '';
    }

    const statusSelect = document.getElementById('editStatus');
    if (statusSelect) {
        statusSelect.value = linha.dataset.idstatus || '';
    }

    const tipoSelect = document.getElementById('editTipo');
    if (tipoSelect) {
        tipoSelect.value = linha.dataset.idtipo || '';
    }

    document.getElementById('infoId').textContent = id;
    document.getElementById('infoNome').textContent = linha.dataset.nome || '';

    abrirModal('modalEditar');
}

function abrirModalRemoverEquipamento(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('removerIdInput').value = id;
    document.getElementById('removerId').textContent = id;
    document.getElementById('removerNome').textContent = linha.dataset.nome || '';

    abrirModal('modalRemover');
}

function abrirModalEditarPlano(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('editNome').value = linha.dataset.nomeplano || '';
    document.getElementById('editDescricao').value = linha.dataset.descricao || '';
    document.getElementById('editDuracao').value = linha.dataset.duracao || '';
    document.getElementById('editValor').value = linha.dataset.valorplano || '';

    abrirModal('modalEditar');
}

function abrirModalRemoverPlano(id) {
    const linha = document.querySelector(`tr[data-id='${id}']`);
    if (!linha) return;

    document.getElementById('removerIdInput').value = id;
    document.getElementById('removerNomePlano').textContent = linha.dataset.nomeplano || '';

    abrirModal('modalRemover');
}


// ---------------------- HOVER EM BOTÕES COM IMAGEM ---------------------- //
const botoesImagem = document.querySelectorAll('.botao-imagem');
botoesImagem.forEach(btn => {
  const overlay = btn.querySelector('.imagem-overlay');
  btn.addEventListener('mouseenter', () => overlay.classList.add('active'));
  btn.addEventListener('mouseleave', () => overlay.classList.remove('active'));
});

// ---------------------- ORDENAR TABELAS COM ÍCONES ---------------------- //
document.addEventListener('DOMContentLoaded', () => {
  const tables = document.querySelectorAll('table');

  tables.forEach(table => {
    const headers = table.querySelectorAll('th');
    const filterableFields = ['Nome', 'Capacidade', 'Plano', 'ID', 'Data de Compra', 'Duração (meses)'];
    let sortDirection = {};

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
        const isAscending = sortDirection[index] === 'asc';

        rows.sort((a, b) => {
          const cellA = a.cells[index].textContent.trim().toLowerCase();
          const cellB = b.cells[index].textContent.trim().toLowerCase();

          if (cellA < cellB) return isAscending ? -1 : 1;
          if (cellA > cellB) return isAscending ? 1 : -1;
          return 0;
        });

        sortDirection[index] = isAscending ? 'desc' : 'asc';

        const tbody = table.querySelector('tbody');
        rows.forEach(row => tbody.appendChild(row));

        // Atualizar ícone
        icon.textContent = isAscending ? '▼' : '▲';
      });

      header.addEventListener('mouseenter', () => {
        icon.style.visibility = 'visible';
      });

      header.addEventListener('mouseleave', () => {
        icon.style.visibility = 'hidden';
      });
    });
  });
});




