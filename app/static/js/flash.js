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
    document.getElementById('editEndereco').value = linha.dataset.endereco || '';
    document.getElementById('editCEP').value = linha.dataset.cep || '';
    document.getElementById('editSexo').value = linha.dataset.sexo || '';
    document.getElementById('editStatus').value = linha.dataset.status || '';
    document.getElementById('editPagamento').value = linha.dataset.pagamento || '0'; // Valor padrão caso não exista
    document.getElementById('editUnidade').value = linha.dataset.unidade || '';
    document.getElementById('editPlano').value = linha.dataset.plano || '';

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

    // Formatar a data para o input type="date" (YYYY-MM-DD)
    const dataCompra = linha.dataset.compra;
    if (dataCompra) {
        const partesData = dataCompra.split('/');
        if (partesData.length === 3) {
            const dataFormatada = `${partesData[2]}-${partesData[1]}-${partesData[0]}`;
            document.getElementById('editDataCompra').value = dataFormatada;
        }
    } else {
        document.getElementById('editDataCompra').value = '';
    }

    document.getElementById('editUnidade').value = linha.dataset.nomeunidade || ''; // Usando nome da unidade aqui, ajuste se precisar do ID
    document.getElementById('editStatus').value = linha.dataset.statusequipamento || '';
    document.getElementById('editTipo').value = linha.dataset.tipoequipamento || '';

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