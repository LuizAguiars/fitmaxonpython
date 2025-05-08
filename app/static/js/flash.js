// flash.js

setTimeout(() => {
  const flashMessages = document.querySelectorAll(".flash-messages li");
  flashMessages.forEach(msg => {
    msg.style.transition = "opacity 0.5s ease-out";
    msg.style.opacity = 0;
    setTimeout(() => msg.remove(), 500);
  });
}, 4000); // 4 segundos



function abrirModal(id) {
  const modal = document.getElementById(id);
  modal.classList.add('active');
}


function abrirModalEditar(id) {
  const select = document.getElementById('selectEditar');
  select.value = id;
  preencherCamposEditar(); // já existente
  abrirModal('modalEditar');
}

function abrirModalRemover(id) {
  const select = document.querySelector('#modalRemover select[name="id"]');
  select.value = id;
  abrirModal('modalRemover');
}


function preencherCamposEditar() {
  const select = document.getElementById('selectEditar');
  const option = select.options[select.selectedIndex];

  document.getElementById('editNome').value = option.getAttribute('data-nome') || '';
  document.getElementById('editEndereco').value = option.getAttribute('data-endereco') || '';
  document.getElementById('editCapacidade').value = option.getAttribute('data-capacidade') || '';
  document.getElementById('editFone').value = option.getAttribute('data-fone') || '';
  document.getElementById('editCidade').value = option.getAttribute('data-cidade') || '';
  document.getElementById('editEstado').value = option.getAttribute('data-estado') || '';
  document.getElementById('editCep').value = option.getAttribute('data-cep') || '';
  document.getElementById('editRegiao').value = option.getAttribute('data-regiao') || '';
}



function preencherCamposEditarPersonal() {
  const select = document.getElementById('selectEditar');
  const option = select.options[select.selectedIndex];

  document.getElementById('editNome').value = option.getAttribute('data-nome') || '';
  document.getElementById('editEmail').value = option.getAttribute('data-email') || '';
  document.getElementById('editEspecialidade').value = option.getAttribute('data-especialidade') || '';
  document.getElementById('editUnidade').value = option.getAttribute('data-unidade') || '';
}

function preencherCamposEditarUsuario() {
  const select = document.getElementById('selectEditarUsuario');
  const option = select.options[select.selectedIndex];
  if (!option) return;
  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editEmail').value = option.dataset.email || '';
  document.getElementById('editEndereco').value = option.dataset.endereco || '';
  document.getElementById('editCEP').value = option.dataset.cep || '';
  document.getElementById('editSexo').value = option.dataset.sexo || '';
  document.getElementById('editStatus').value = option.dataset.status || '';
  document.getElementById('editPlano').value = option.dataset.plano || '';
  document.getElementById('editUnidade').value = option.dataset.unidade || '';
  document.getElementById('editPagamento').value = option.dataset.pagamento || '0';
}

function preencherCamposEditarEquipamento() {
  const select = document.getElementById('selectEditarEquipamento');
  const option = select.options[select.selectedIndex];
  if (!option) return;
  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editDescricao').value = option.dataset.descricao || '';

  // Converter data para formato yyyy-mm-dd caso esteja completa
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



function preencherCamposEditarPlano() {
  const select = document.getElementById('selectEditarPlano');
  const option = select.options[select.selectedIndex];

  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editDescricao').value = option.dataset.descricao || '';
  document.getElementById('editDuracao').value = option.dataset.duracao || '';
  document.getElementById('editValor').value = option.dataset.valor || '';
}

function abrirModal(id) {
  document.getElementById(id).classList.add('active');
}

function fecharModal(id) {
  document.getElementById(id).classList.remove('active');
}


function preencherCamposEditarPlano() {
  const select = document.getElementById('selectEditarPlano');
  const option = select.options[select.selectedIndex];

  if (!option) return;

  document.getElementById('editNome').value = option.dataset.nome || '';
  document.getElementById('editDescricao').value = option.dataset.descricao || '';
  document.getElementById('editDuracao').value = option.dataset.duracao || '';
  document.getElementById('editValor').value = option.dataset.valor || '';
}

function abrirModal(id) {
  document.getElementById(id).classList.add('active');
}

function fecharModal(id) {
  document.getElementById(id).classList.remove('active');
}

// Hover com imagem de fundo
const botoesImagem = document.querySelectorAll('.botao-imagem');
botoesImagem.forEach(btn => {
  const overlay = btn.querySelector('.imagem-overlay');
  btn.addEventListener('mouseenter', () => overlay.classList.add('active'));
  btn.addEventListener('mouseleave', () => overlay.classList.remove('active'));
});
