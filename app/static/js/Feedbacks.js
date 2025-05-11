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

function exibirMensagemEnvio() {
  // Criação da mensagem
  const mensagemEnvio = document.createElement('div');
  mensagemEnvio.textContent = "Feedback enviado com sucesso!";
  
  // Estilos da mensagem
  mensagemEnvio.style.backgroundColor = 'green';
  mensagemEnvio.style.color = 'white';
  mensagemEnvio.style.padding = '10px';
  mensagemEnvio.style.marginTop = '10px';
  mensagemEnvio.style.borderRadius = '5px';
  mensagemEnvio.style.textAlign = 'center';
  mensagemEnvio.style.fontSize = '16px';
  
  // Estilização para centralizar a mensagem
  mensagemEnvio.style.position = 'absolute';
  mensagemEnvio.style.top = '50%';
  mensagemEnvio.style.left = '50%';
  mensagemEnvio.style.transform = 'translate(-50%, -50%)';
  mensagemEnvio.style.zIndex = '1000';  // Garantir que a mensagem fique sobre outros elementos
  
  // Adicionando a mensagem ao corpo ou formulário
  document.body.appendChild(mensagemEnvio);
  
  // Exibir a mensagem por 3 segundos e depois removê-la
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

  // Enviar os dados via AJAX para o Flask
  fetch(feedbacksUrl, {
    method: 'POST',
    body: new FormData(form),  // Envia os dados do formulário
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro ao enviar os dados');
    }
    return response.text(); // Ou response.json() se o servidor retornar JSON
  })
  .then(data => {
    // Exibe a mensagem de sucesso após o envio
    exibirMensagemEnvio();
    
    // Limpar o formulário
    form.reset();
    updateStars();  // Isso garante que as estrelas sejam resetadas
    atualizarFeedbackCampos(0); // Reseta a visibilidade dos campos de feedback
    selectedRating = 0; // Reseta o rating
  })
  .catch(error => {
    console.error('Erro ao enviar os dados:', error);
    exibirMensagemEnvio();  // Se houver erro, ainda pode exibir a mensagem de falha
  });
});
