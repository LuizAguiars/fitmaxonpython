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
}

function fecharModal(id) {
  document.getElementById(id).classList.remove('active');
}


// ---------------------- MODAIS DE EDIÇÃO ---------------------- //

// Usuário
function preencherCamposEditarUsuario() {
  const select = document.getElementById('selectEditarUsuario');
  const option = select.options[select.selectedIndex];
  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editEmail').value = option.dataset.email || '';
  document.getElementById('editEndereco').value = option.dataset.endereco || '';
  document.getElementById('editCEP').value = option.dataset.cep || '';
  document.getElementById('editNascimento').value = option.dataset.nascimento || '';
  document.getElementById("editNascimento").value = usuarioSelecionado.dataset.nascimento || '';

  document.getElementById('editSexo').value = option.dataset.sexo || '';
  document.getElementById('editStatus').value = option.dataset.status || '';
  document.getElementById('editPlano').value = option.dataset.plano || '';
  document.getElementById('editUnidade').value = option.dataset.unidade || '';
  document.getElementById('editPagamento').value = option.dataset.pagamento || '0';
}

// Personal
function preencherCamposEditarPersonal() {
  const select = document.getElementById('selectEditar');
  const option = select.options[select.selectedIndex];
  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editEmail').value = option.dataset.email || '';
  document.getElementById('editEspecialidade').value = option.dataset.especialidade || '';
  document.getElementById('editUnidade').value = option.dataset.unidade || '';
}

// Equipamento
function preencherCamposEditarEquipamento() {
  const select = document.getElementById('selectEditarEquipamento');
  const option = select.options[select.selectedIndex];
  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editDescricao').value = option.dataset.descricao || '';
  
  if (option.dataset.data) {
    const data = new Date(option.dataset.data);
    if (!isNaN(data)) {
      document.getElementById('editDataCompra').value = data.toISOString().split('T')[0];
    }
  }

  document.getElementById('editUnidade').value = option.dataset.unidade || '';
  document.getElementById('editStatus').value = option.dataset.status || '';
  document.getElementById('editTipo').value = option.dataset.tipo || '';
}

// Plano
function preencherCamposEditarPlano() {
  const select = document.getElementById('selectEditarPlano');
  const option = select.options[select.selectedIndex];
  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editDescricao').value = option.dataset.descricao || '';
  document.getElementById('editDuracao').value = option.dataset.duracao || '';
  document.getElementById('editValor').value = option.dataset.valor || '';
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


// ---------------------- HOVER EM BOTÕES COM IMAGEM ---------------------- //
const botoesImagem = document.querySelectorAll('.botao-imagem');
botoesImagem.forEach(btn => {
  const overlay = btn.querySelector('.imagem-overlay');
  btn.addEventListener('mouseenter', () => overlay.classList.add('active'));
  btn.addEventListener('mouseleave', () => overlay.classList.remove('active'));
});
