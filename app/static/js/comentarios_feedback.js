document.addEventListener('DOMContentLoaded', function() {
  const select = document.getElementById('unidade-select');
  const filtroNota = document.getElementById('filtro-nota');
  const filtroUsuario = document.getElementById('filtro-usuario');
  const filtroQtd = document.getElementById('filtro-quantidade');
  const lista = document.getElementById('comentarios-lista');
  const paginacao = document.getElementById('comentarios-paginacao');
  let paginaAtual = 1;

  function renderComentarios(comentarios, total, porPagina) {
    lista.innerHTML = '';
    if (!comentarios.length) {
      lista.innerHTML = '<li style="padding: 24px 0; text-align:center; color:#888; font-size:1.08rem;"><em>Nenhum comentário encontrado.</em></li>';
      paginacao.innerHTML = '';
      return;
    }
    comentarios.forEach(c => {
      const li = document.createElement('li');
      li.style.background = 'rgba(20,24,38,0.06)';
      li.style.borderRadius = '12px';
      li.style.marginBottom = '18px';
      li.style.padding = '18px 22px 12px 22px';
      li.style.boxShadow = '0 1px 8px 0 rgba(0,0,0,0.07)';
      // Estrelas de 5 a 1
      let estrelas = '';
      let nota = Math.max(1, Math.min(5, Number(c.nota_user)));
      for (let i = 0; i < 5; i++) estrelas += i < nota ? '★' : '☆';
      li.innerHTML = `
        <div style="display:flex; align-items:center; gap:12px; margin-bottom: 6px;">
          <span style="font-size:1.35rem; color:#ffc107; font-weight:700;">${estrelas}<span style='color:#bbb; font-size:1.1rem; margin-left:4px;'>${nota}/5</span></span>
          <span style="color:#001f5b; font-weight:600;">${c.nome_unidade || ''}</span>
          <span style="color:#888; font-size:0.98rem;">${c.nome_usuario ? '('+c.nome_usuario+')' : ''}</span>
        </div>
        <p style="font-size:1.13rem; color:#222; margin:0 0 6px 0;"><em>${c.Comentario}</em></p>
      `;
      lista.appendChild(li);
    });
    // Paginação melhorada
    paginacao.innerHTML = '';
    const totalPaginas = Math.ceil(total / porPagina);
    if (totalPaginas > 1) {
      let paginas = [];
      if (totalPaginas <= 5) {
        for (let p = 1; p <= totalPaginas; p++) paginas.push(p);
      } else {
        if (paginaAtual > 2) paginas.push(1);
        if (paginaAtual > 3) paginas.push('...');
        for (let p = Math.max(1, paginaAtual - 1); p <= Math.min(totalPaginas, paginaAtual + 1); p++) paginas.push(p);
        if (paginaAtual < totalPaginas - 2) paginas.push('...');
        if (paginaAtual < totalPaginas - 1) paginas.push(totalPaginas);
      }
      // Botão anterior
      const btnPrev = document.createElement('button');
      btnPrev.textContent = '<';
      btnPrev.disabled = paginaAtual === 1;
      btnPrev.style.padding = '6px 12px';
      btnPrev.style.borderRadius = '6px';
      btnPrev.style.border = '1px solid #263159';
      btnPrev.style.background = '#f7f8fa';
      btnPrev.style.color = '#001f5b';
      btnPrev.style.fontWeight = 'bold';
      btnPrev.onclick = () => { paginaAtual = Math.max(1, paginaAtual - 1); carregarComentarios(); };
      paginacao.appendChild(btnPrev);
      // Números
      paginas.forEach(p => {
        if (p === '...') {
          const span = document.createElement('span');
          span.textContent = '...';
          span.style.margin = '0 6px';
          span.style.color = '#888';
          paginacao.appendChild(span);
        } else {
          const btn = document.createElement('button');
          btn.textContent = p;
          btn.style.padding = '6px 14px';
          btn.style.borderRadius = '6px';
          btn.style.border = '1px solid #263159';
          btn.style.background = p === paginaAtual ? '#001f5b' : '#f7f8fa';
          btn.style.color = p === paginaAtual ? '#fff' : '#001f5b';
          btn.style.fontWeight = 'bold';
          btn.style.cursor = 'pointer';
          btn.disabled = p === paginaAtual;
          btn.onclick = () => { paginaAtual = p; carregarComentarios(); };
          paginacao.appendChild(btn);
        }
      });
      // Botão próximo
      const btnNext = document.createElement('button');
      btnNext.textContent = '>';
      btnNext.disabled = paginaAtual === totalPaginas;
      btnNext.style.padding = '6px 12px';
      btnNext.style.borderRadius = '6px';
      btnNext.style.border = '1px solid #263159';
      btnNext.style.background = '#f7f8fa';
      btnNext.style.color = '#001f5b';
      btnNext.style.fontWeight = 'bold';
      btnNext.onclick = () => { paginaAtual = Math.min(totalPaginas, paginaAtual + 1); carregarComentarios(); };
      paginacao.appendChild(btnNext);
    }
  }

  function carregarComentarios() {
    const unidadeId = select.value;
    const nota = filtroNota.value;
    const usuario = filtroUsuario.value;
    const qtd = parseInt(filtroQtd.value) || 10;
    let url = `/api/feedback_comentarios/${unidadeId}?`;
    if (nota) url += `nota=${encodeURIComponent(nota)}&`;
    if (usuario) url += `usuario=${encodeURIComponent(usuario)}&`;
    url += `limit=${qtd}&page=${paginaAtual}`;
    fetch(url)
      .then(res => res.json())
      .then(res => {
        renderComentarios(res.comentarios, res.total, qtd);
      })
      .catch(() => {
        lista.innerHTML = '<li><em>Erro ao carregar comentários.</em></li>';
        paginacao.innerHTML = '';
      });
  }

  select.addEventListener('change', () => { paginaAtual = 1; carregarComentarios(); });
  filtroNota.addEventListener('change', () => { paginaAtual = 1; carregarComentarios(); });
  filtroUsuario.addEventListener('input', () => { paginaAtual = 1; carregarComentarios(); });
  filtroQtd.addEventListener('change', () => { paginaAtual = 1; carregarComentarios(); });

  // Gatilho inicial
  carregarComentarios();
});
