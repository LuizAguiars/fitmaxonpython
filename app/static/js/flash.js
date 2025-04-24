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

function fecharModal(id) {
  const modal = document.getElementById(id);
  modal.classList.remove('active');
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



