// utils: maiúsculas conforme ABNT
function formatarNomeABNT(nome) {
  return nome
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim()
    .split(' ')
    .map(p => p.charAt(0).toUpperCase() + p.slice(1))
    .join(' ');
}

// Máscara para telefone
function mascaraTelefoneHandler() {
  let v = this.value.replace(/\D/g, "");
  if (v.length > 11) v = v.slice(0, 11);
  v = v.replace(/^(\d{2})(\d)/, "($1) $2");
  v = v.replace(/(\d{5})(\d)/, "$1-$2");
  this.value = v;
}

// Máscara para CEP
function mascaraCEPHandler() {
  let v = this.value.replace(/\D/g, "");
  if (v.length > 8) v = v.slice(0, 8);
  v = v.replace(/(\d{5})(\d)/, "$1-$2");
  this.value = v;
}

// Aplica máscaras para todos inputs de telefone
function aplicarMascaraTelefoneEmTodos() {
  document.querySelectorAll('input[name="fone"]').forEach(function(input) {
    input.removeEventListener('input', mascaraTelefoneHandler);
    input.addEventListener('input', mascaraTelefoneHandler);
  });
}

// Aplica máscaras para todos inputs de CEP
function aplicarMascaraCEPEmTodos() {
  document.querySelectorAll('input[name="cep"]').forEach(function(input) {
    input.removeEventListener('input', mascaraCEPHandler);
    input.addEventListener('input', mascaraCEPHandler);
  });
}

// Aplica todas as máscaras ao carregar
document.addEventListener("DOMContentLoaded", function () {
  aplicarMascaraTelefoneEmTodos();
  aplicarMascaraCEPEmTodos();

  // Validação nome para impedir números/caracteres especiais no início
  const nomeInput = document.querySelector('input[name="nome"]');
  if (nomeInput) {
    nomeInput.addEventListener('input', function () {
      this.value = this.value.replace(/^[^a-zA-Zá-úÁ-ÚãÃõÕçÇ]+/, '');
    });
  }

  // Máscara CPF (se precisar)
  const cpfInput = document.querySelector('input[name="cpf"]');
  if (cpfInput) {
    cpfInput.addEventListener('input', function () {
      let v = this.value.replace(/\D/g, "");
      if (v.length > 11) v = v.slice(0, 11);
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d)/, "$1.$2");
      v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
      this.value = v;
    });
  }

  // Formata nome ao enviar o formulário
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      const nomeInput = this.querySelector('input[name="nome"]');
      if (nomeInput) {
        nomeInput.value = formatarNomeABNT(nomeInput.value);
      }
    });
  }
});
