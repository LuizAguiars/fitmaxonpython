// Validação dos campos do modal de informações físicas e envio via AJAX
function validarInfoFisicaModal() {
  let valido = true;
  let msg = '';
  const altura = document.querySelector('input[name="altura"]');
  const peso = document.querySelector('input[name="peso"]');
  const gordura = document.querySelector('input[name="gordura"]');
  const braquial = document.querySelector('input[name="braquial"]');
  const abdominal = document.querySelector('input[name="abdominal"]');
  const toracico = document.querySelector('input[name="toracico"]');
  const cintura = document.querySelector('input[name="cintura"]');
  const quadril = document.querySelector('input[name="quadril"]');
  const imc = document.querySelector('input[name="imc"]');

  // Altura
  if (altura.value && (altura.value < 0.5 || altura.value > 2.5)) {
    msg += 'Altura deve estar entre 0.5 e 2.5 metros.\n';
    valido = false;
  }
  // Peso
  if (peso.value && (peso.value < 20 || peso.value > 400)) {
    msg += 'Peso deve estar entre 20 e 400 kg.\n';
    valido = false;
  }
  // Gordura
  if (gordura.value && (gordura.value < 0 || gordura.value > 100)) {
    msg += 'Gordura deve estar entre 0 e 100%.\n';
    valido = false;
  }
  // Perímetros
  if (braquial.value && (braquial.value < 10 || braquial.value > 80)) {
    msg += 'Braço deve estar entre 10 e 80 cm.\n';
    valido = false;
  }
  if (abdominal.value && (abdominal.value < 30 || abdominal.value > 200)) {
    msg += 'Abdômen deve estar entre 30 e 200 cm.\n';
    valido = false;
  }
  if (toracico.value && (toracico.value < 30 || toracico.value > 200)) {
    msg += 'Tórax deve estar entre 30 e 200 cm.\n';
    valido = false;
  }
  if (cintura.value && (cintura.value < 30 || cintura.value > 200)) {
    msg += 'Cintura deve estar entre 30 e 200 cm.\n';
    valido = false;
  }
  if (quadril.value && (quadril.value < 30 || quadril.value > 200)) {
    msg += 'Quadril deve estar entre 30 e 200 cm.\n';
    valido = false;
  }
  if (imc.value && (imc.value < 10 || imc.value > 100)) {
    msg += 'IMC deve estar entre 10 e 100.\n';
    valido = false;
  }
  if (!valido) {
    alert(msg);
  }
  return valido;
}

// Envio do formulário do modal via AJAX
function enviarInfoFisicaModal(e) {
  e.preventDefault();
  if (!validarInfoFisicaModal()) return false;
  const form = e.target;
  const formData = new FormData(form);
  fetch(form.action, {
    method: 'POST',
    body: formData
  })
    .then(resp => resp.text())
    .then(html => {
      // Atualiza só a tabela de informações físicas
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const novaTabela = doc.querySelector('.minha-conta:nth-of-type(2)');
      if (novaTabela) {
        document.querySelector('.minha-conta:nth-of-type(2)').innerHTML = novaTabela.innerHTML;
      }
      fecharModal('modalInfoUsuario');
      // Feedback visual
      const msg = doc.querySelector('.flash-messages, .flash-message');
      if (msg) {
        document.body.insertAdjacentHTML('afterbegin', msg.outerHTML);
      }
    })
    .catch(() => {
      alert('Erro ao salvar informações físicas.');
    });
  return false;
}

// Preenche automaticamente o IMC ao digitar altura e peso
function atualizarIMCModal() {
  const altura = document.querySelector('#modalInfoUsuario input[name="altura"]');
  const peso = document.querySelector('#modalInfoUsuario input[name="peso"]');
  const imc = document.querySelector('#modalInfoUsuario input[name="imc"]');
  const imcClass = document.getElementById('imc-classificacao');
  if (altura && peso && imc) {
    const a = parseFloat(altura.value.replace(',', '.'));
    const p = parseFloat(peso.value.replace(',', '.'));
    if (a > 0 && p > 0) {
      const valor = p / (a * a);
      if (isFinite(valor)) {
        imc.value = valor.toFixed(2);
        if (imcClass) {
          const {texto, cor} = classificaIMCComCor(valor);
          imcClass.textContent = texto;
          imcClass.style.color = cor;
        }
      } else {
        imc.value = '';
        if (imcClass) { imcClass.textContent = ''; imcClass.style.color = ''; }
      }
    } else {
      imc.value = '';
      if (imcClass) { imcClass.textContent = ''; imcClass.style.color = ''; }
    }
  }
}

function classificaIMCComCor(imc) {
  if (imc < 16) return {texto: 'MAGREZA GRAVE', cor: '#d32f2f'};
  if (imc < 17) return {texto: 'MAGREZA MODERADA', cor: '#ff9800'};
  if (imc < 18.5) return {texto: 'MAGREZA LEVE', cor: '#ff9800'};
  if (imc < 25) return {texto: 'PESO NORMAL', cor: '#388e3c'};
  if (imc < 30) return {texto: 'SOBREPESO', cor: '#ff9800'};
  if (imc < 35) return {texto: 'OBESIDADE GRAU I', cor: '#d32f2f'};
  if (imc < 40) return {texto: 'OBESIDADE GRAU II (SEVERA)', cor: '#d32f2f'};
  return {texto: 'OBESIDADE GRAU III (MÓRBIDA)', cor: '#b71c1c'};
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#modalInfoUsuario form');
  if (form) {
    form.addEventListener('submit', enviarInfoFisicaModal);
  }
  const altura = document.querySelector('#modalInfoUsuario input[name="altura"]');
  const peso = document.querySelector('#modalInfoUsuario input[name="peso"]');
  if (altura) altura.addEventListener('input', atualizarIMCModal);
  if (peso) peso.addEventListener('input', atualizarIMCModal);
});
