const stars = document.querySelectorAll('.star');
const notaInput = document.getElementById('nota');
const feedbackNegativo = document.getElementById('feedback-negativo');
const feedbackPositivo = document.getElementById('feedback-positivo');
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
  } else if (nota >= 4 && nota <= 5) {
    feedbackNegativo.classList.add('hidden');
    feedbackPositivo.classList.remove('hidden');
  } else {
    feedbackNegativo.classList.add('hidden');
    feedbackPositivo.classList.add('hidden');
  }
}

stars.forEach(star => {
  const value = parseInt(star.dataset.value);

  star.addEventListener('mouseenter', () => {
    updateStars(value);
  });

  star.addEventListener('mouseleave', () => {
    updateStars();
  });

  star.addEventListener('click', () => {
    selectedRating = value;
    notaInput.value = value;
    updateStars();
    atualizarFeedbackCampos(value);
  });
});
