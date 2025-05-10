const stars = document.querySelectorAll('.star');
const notaInput = document.getElementById('nota');
const feedbackNegativo = document.getElementById('feedback-negativo');
const feedbackPositivo = document.getElementById('feedback-positivo');
const form = document.getElementById('form-feedback');
const mensagemSucesso = document.getElementById('mensagem-sucesso');
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
  if (nota >= 1 && nota <= 3) {
    feedbackNegativo.classList.remove('hidden');
    feedbackPositivo.classList.add('hidden');
    comentarioInput.placeholder = "O que pode ser melhorado?";
  } else if (nota >= 4 && nota <= 5) {
    feedbackNegativo.classList.add('hidden');
    feedbackPositivo.classList.remove('hidden');
    comentarioInput.placeholder = "O que mais gostou?";
  } else {
    feedbackNegativo.classList.add('hidden');
    feedbackPositivo.classList.add('hidden');
    comentarioInput.placeholder = "Deixe um comentário!";
  }
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

  mensagemSucesso.classList.remove('hidden');
  form.reset();
  updateStars();
  atualizarFeedbackCampos(0);
  selectedRating = 0;
});