// feedbacks.js atualizado com transição suave via .mostrar
const stars = document.querySelectorAll('.star');
const notaInput = document.getElementById('nota');
const feedbackNegativo = document.getElementById('feedback-negativo');
const feedbackPositivo = document.getElementById('feedback-positivo');
const form = document.getElementById('form-feedback');
const comentarioInput = document.getElementById('comentario');
let selectedRating = 0;

function updateStars(hoverValue = 0) {
  stars.forEach(star => {
    const value = parseInt(star.dataset.value);
    star.classList.remove('hovered', 'selected');
    if (hoverValue > 0 && value <= hoverValue) {
      star.classList.add('hovered');
    } else if (selectedRating > 0 && value <= selectedRating) {
      star.classList.add('selected');
    }
  });
}

function atualizarFeedbackCampos(nota) {
  feedbackNegativo.classList.remove('mostrar');
  feedbackPositivo.classList.remove('mostrar');

  if (nota >= 1 && nota <= 3) {
    feedbackNegativo.classList.add('mostrar');
    comentarioInput.placeholder = "O que pode ser melhorado?";
  } else if (nota >= 4 && nota <= 5) {
    feedbackPositivo.classList.add('mostrar');
    comentarioInput.placeholder = "O que mais gostou?";
  } else {
    comentarioInput.placeholder = "Deixe um comentário!";
  }
}

function exibirMensagemEnvio() {
  const mensagemEnvio = document.createElement('div');
  mensagemEnvio.textContent = "Feedback enviado com sucesso!";
  mensagemEnvio.style.backgroundColor = 'green';
  mensagemEnvio.style.color = 'white';
  mensagemEnvio.style.padding = '10px';
  mensagemEnvio.style.marginTop = '10px';
  mensagemEnvio.style.borderRadius = '5px';
  mensagemEnvio.style.textAlign = 'center';
  mensagemEnvio.style.fontSize = '16px';
  mensagemEnvio.style.position = 'absolute';
  mensagemEnvio.style.top = '50%';
  mensagemEnvio.style.left = '50%';
  mensagemEnvio.style.transform = 'translate(-50%, -50%)';
  mensagemEnvio.style.zIndex = '1000';

  document.body.appendChild(mensagemEnvio);

  setTimeout(() => {
    mensagemEnvio.remove();
  }, 4000);
}

stars.forEach(star => {
  const value = parseInt(star.dataset.value);

  star.addEventListener('mouseenter', () => updateStars(value));
  star.addEventListener('mouseleave', () => updateStars());
  star.addEventListener('click', () => {
    selectedRating = value;
    notaInput.value = value;
    updateStars();
    atualizarFeedbackCampos(value);
  });
});

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const nota = notaInput.value;
  const comentario = comentarioInput.value;

  const motivos = [...document.querySelectorAll('input[name="motivos[]"]:checked')].map(c => c.value);
  const elogios = [...document.querySelectorAll('input[name="elogios[]"]:checked')].map(c => c.value);

  console.log('Nota:', nota);
  console.log('Comentário:', comentario);
  console.log('Motivos:', motivos);
  console.log('Elogios:', elogios);

  fetch(feedbacksUrl, {
    method: 'POST',
    body: new FormData(form),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro ao enviar os dados');
    }
    return response.text();
  })
  .then(data => {
    exibirMensagemEnvio();
    form.reset();
    updateStars();
    atualizarFeedbackCampos(0);
    selectedRating = 0;
  })
  .catch(error => {
    console.error('Erro ao enviar os dados:', error);
    exibirMensagemEnvio();
  });
});
