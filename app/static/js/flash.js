// flash.js

setTimeout(() => {
  const flashMessages = document.querySelectorAll(".flash-messages li");
  flashMessages.forEach(msg => {
    msg.style.transition = "opacity 0.5s ease-out";
    msg.style.opacity = 0;
    setTimeout(() => msg.remove(), 500);
  });
}, 4000); // 4 segundos
