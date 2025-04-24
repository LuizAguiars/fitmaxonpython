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
      }
  }

  function limparCampos() {
      document.getElementById("nome").value = "";
      document.getElementById("email").value = "";
      document.getElementById("especialidade").value = "";
      document.getElementById("id_unidade").selectedIndex = 0;
  }

  // listeners globais
  window.abrirModal = abrirModal;
  window.fecharModal = fecharModal;

  // escuta mudança no dropdown para editar
  selectID.addEventListener("change", function () {
      preencherCampos(this.value);
  });
});
