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

// Impede números e caracteres especiais no início do nome
document.querySelector('input[name="nome"]').addEventListener('input', function () {
  const campo = this;
  campo.value = campo.value.replace(/^[^a-zA-Zá-úÁ-ÚãÃõÕçÇ]+/, '');
});

// Aplica máscara ao CPF
document.querySelector('input[name="cpf"]').addEventListener('input', function () {
  let v = this.value.replace(/\D/g, "");
  if (v.length > 11) v = v.slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, "$1.$2");
  v = v.replace(/(\d{3})(\d)/, "$1.$2");
  v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  this.value = v;
});

// Aplica máscara ao CEP
document.querySelector('input[name="cep"]').addEventListener('input', function () {
  let v = this.value.replace(/\D/g, "");
  if (v.length > 8) v = v.slice(0, 8);
  v = v.replace(/(\d{5})(\d)/, "$1-$2");
  this.value = v;
});

// Formata nome antes de enviar
document.querySelector('form').addEventListener('submit', function (e) {
  const nomeInput = this.querySelector('input[name="nome"]');
  nomeInput.value = formatarNomeABNT(nomeInput.value);
});
