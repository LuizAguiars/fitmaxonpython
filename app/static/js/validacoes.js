// Validações de campos

// Validação de nome (permite apenas letras, espaços e apóstrofo)
function validarNome(nome) {
  // Remove espaços extras e formata conforme ABNT
  nome = nome.replace(/\s+/g, ' ').trim();
  // Verifica se tem pelo menos nome e sobrenome
  if (nome.split(' ').length < 2) return false;
  // Verifica se contém apenas letras, espaços e apóstrofo
  return /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ' ]+$/.test(nome);
}

// Validação de nome de unidade (permite letras, números, espaços e apóstrofo)
function validarNomeUnidade(nome) {
  nome = nome.replace(/\s+/g, ' ').trim();
  return /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9' ]+$/.test(nome) && nome.length > 0;
}

// Validação de especialidade (apenas letras e espaços)
function validarEspecialidade(especialidade) {
  especialidade = especialidade.replace(/\s+/g, ' ').trim();
  return /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+$/.test(especialidade) && especialidade.length > 0;
}

// Validação de endereço (letras, números, espaços e pontuação básica)
function validarEndereco(endereco) {
  endereco = endereco.replace(/\s+/g, ' ').trim();
  return /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9,.' -]+$/.test(endereco) && endereco.length > 0;
}

// Validação de email
function validarEmail(email) {
  const regex = /^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
}

// Validação de CPF
function validarCPF(cpf) {
  cpf = cpf.replace(/[^\d]/g, '');
  
  if (cpf.length !== 11) return false;
  
  // Verifica se todos os dígitos são iguais
  if (/^(\d)\1{10}$/.test(cpf)) return false;
  
  // Validação dos dígitos verificadores
  let soma = 0;
  let resto;
  
  for (let i = 1; i <= 9; i++) {
    soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
  }
  
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.substring(9, 10))) return false;
  
  soma = 0;
  for (let i = 1; i <= 10; i++) {
    soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
  }
  
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.substring(10, 11))) return false;
  
  return true;
}

// Validação de CEP
function validarCEP(cep) {
  cep = cep.replace(/[^\d]/g, '');
  return cep.length === 8;
}

// Validação de telefone
function validarTelefone(telefone) {
  telefone = telefone.replace(/[^\d]/g, '');
  return telefone.length >= 10 && telefone.length <= 11;
}

// Validação de data
function validarData(data) {
  const dataObj = new Date(data);
  if (isNaN(dataObj.getTime())) return false;
  
  // Verifica se a data não é futura
  const hoje = new Date();
  if (dataObj > hoje) return false;
  
  // Verifica se a pessoa tem pelo menos 14 anos (para cadastro)
  const idade = hoje.getFullYear() - dataObj.getFullYear();
  const m = hoje.getMonth() - dataObj.getMonth();
  if (m < 0 || (m === 0 && hoje.getDate() < dataObj.getDate())) {
    idade--;
  }
  return idade >= 14;
}

// Validação de valor monetário
function validarValor(valor) {
  valor = parseFloat(valor);
  return !isNaN(valor) && valor > 0;
}

// Validação de capacidade
function validarCapacidade(capacidade) {
  capacidade = parseInt(capacidade);
  return !isNaN(capacidade) && capacidade > 0;
}

// Validação de idade mínima genérica
function validarIdadeMinima(data, idadeMinima) {
  const dataObj = new Date(data);
  if (isNaN(dataObj.getTime())) return false;
  const hoje = new Date();
  let idade = hoje.getFullYear() - dataObj.getFullYear();
  const m = hoje.getMonth() - dataObj.getMonth();
  if (m < 0 || (m === 0 && hoje.getDate() < dataObj.getDate())) {
    idade--;
  }
  return idade >= idadeMinima;
}

// Aplicação das máscaras e validações nos campos
document.addEventListener("DOMContentLoaded", function() {
  // Validação de idade mínima apenas em campos com classe "validar-idade-personal"
  document.querySelectorAll('.validar-idade-personal').forEach(input => {
    input.addEventListener('change', function () {
      this.setCustomValidity(
        validarIdadeMinima(this.value, 20)
          ? ''
          : 'Personal deve ter pelo menos 20 anos completos.'
      );
    });
  });

  // Máscaras
  const mascaraCPF = (value) => {
    value = value.replace(/\D/g, '').slice(0, 11); // Limita a 11 dígitos
    return value
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  };

  const mascaraCEP = (value) => {
    return value
      .replace(/\D/g, '')
      .replace(/(\d{5})(\d)/, '$1-$2');
  };

  const mascaraTelefone = (value) => {
    return value
      .replace(/\D/g, '')
      .replace(/^(\d{2})(\d)/g, '($1) $2')
      .replace(/(\d)(\d{4})$/, '$1-$2');
  };

  // Aplicar máscaras e validações específicas
  document.querySelectorAll('input[name="cpf"]').forEach(input => {
    input.addEventListener('input', function() {
      this.value = mascaraCPF(this.value);
      this.setCustomValidity(validarCPF(this.value) ? '' : 'CPF inválido');
    });
  });

  document.querySelectorAll('input[name="cep"]').forEach(input => {
    input.addEventListener('input', function() {
      this.value = mascaraCEP(this.value);
      this.setCustomValidity(validarCEP(this.value) ? '' : 'CEP inválido');
    });
  });

  document.querySelectorAll('input[name="fone"]').forEach(input => {
    input.addEventListener('input', function() {
      this.value = mascaraTelefone(this.value);
      this.setCustomValidity(validarTelefone(this.value) ? '' : 'Telefone inválido');
    });
  });

  // Validações em tempo real
  document.querySelectorAll('input[name="nome"]').forEach(input => {
    const form = input.closest('form');
    const isUnidadeForm = form && (form.action.includes('unidade') || form.action.includes('gerenciar_unidade'));
    const isPersonalForm = form && (form.action.includes('personal') || form.action.includes('gestao_personal'));
    
    input.addEventListener('input', function() {
      if (isUnidadeForm) {
        this.value = this.value.replace(/[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9' ]/g, '');
        this.setCustomValidity(validarNomeUnidade(this.value) ? '' : 'Nome inválido');
      } else if (isPersonalForm) {
        this.value = this.value.replace(/[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ' ]/g, '');
        this.setCustomValidity(validarNome(this.value) ? '' : 'Nome inválido (digite nome e sobrenome)');
      } else {
        this.value = this.value.replace(/[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ' ]/g, '');
        this.setCustomValidity(validarNome(this.value) ? '' : 'Nome inválido (digite nome e sobrenome)');
      }
    });
  });

  document.querySelectorAll('input[name="email"]').forEach(input => {
    input.addEventListener('input', function() {
      this.setCustomValidity(validarEmail(this.value) ? '' : 'E-mail inválido');
    });
  });




  document.querySelectorAll('input[name="valor"]').forEach(input => {
    input.addEventListener('input', function() {
      this.setCustomValidity(validarValor(this.value) ? '' : 'Valor inválido');
    });
  });

  document.querySelectorAll('input[name="capacidade"]').forEach(input => {
    input.addEventListener('input', function() {
      this.value = this.value.replace(/[^0-9]/g, '');
      this.setCustomValidity(validarCapacidade(this.value) ? '' : 'Capacidade inválida');
    });
  });

  document.querySelectorAll('input[name="especialidade"]').forEach(input => {
    input.addEventListener('input', function() {
      const oldValue = this.value;
      this.value = this.value.replace(/[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]/g, '');
      if (oldValue !== this.value) {
        this.setCustomValidity('Especialidade deve conter apenas letras e espaços');
      } else {
        this.setCustomValidity(validarEspecialidade(this.value) ? '' : 'Especialidade inválida');
      }
    });
  });

  document.querySelectorAll('input[name="endereco"]').forEach(input => {
    input.addEventListener('input', function() {
      this.value = this.value.replace(/[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ0-9,.' -]/g, '');
      this.setCustomValidity(validarEndereco(this.value) ? '' : 'Endereço inválido');
    });
  });

  // Validação de formulários antes do envio
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      const campos = this.querySelectorAll('input, select');
      let formValido = true;

      campos.forEach(campo => {
        if (campo.hasAttribute('required') && !campo.value) {
          campo.setCustomValidity('Este campo é obrigatório');
          formValido = false;
        }

        const isUnidadeForm = form.action.includes('unidade') || form.action.includes('gerenciar_unidade');
        const isPersonalForm = form.action.includes('personal') || form.action.includes('gestao_personal');
        
        if (campo.name === 'nome') {
          if (isUnidadeForm) {
            if (!validarNomeUnidade(campo.value)) {
              campo.setCustomValidity('Nome inválido');
              formValido = false;
            }
          } else if (isPersonalForm) {
            if (!validarNome(campo.value)) {
              campo.setCustomValidity('Nome inválido (digite nome e sobrenome)');
              formValido = false;
            }
          } else if (!validarNome(campo.value)) {
            campo.setCustomValidity('Nome inválido');
            formValido = false;
          }
        }

        if (campo.name === 'especialidade' && !validarEspecialidade(campo.value)) {
          campo.setCustomValidity('Especialidade inválida');
          formValido = false;
        }

        if (campo.name === 'endereco' && !validarEndereco(campo.value)) {
          campo.setCustomValidity('Endereço inválido');
          formValido = false;
        }

        if (campo.name === 'email' && !validarEmail(campo.value)) {
          campo.setCustomValidity('E-mail inválido');
          formValido = false;
        }

        if (campo.name === 'cpf' && !validarCPF(campo.value)) {
          campo.setCustomValidity('CPF inválido');
          formValido = false;
        }

        if (campo.name === 'cep' && !validarCEP(campo.value)) {
          campo.setCustomValidity('CEP inválido');
          formValido = false;
        }

        if (campo.name === 'fone' && !validarTelefone(campo.value)) {
          campo.setCustomValidity('Telefone inválido');
          formValido = false;
        }

        if (campo.type === 'date' && !validarData(campo.value)) {
          campo.setCustomValidity('Data inválida');
          formValido = false;
        }

        if (campo.name === 'valor' && !validarValor(campo.value)) {
          campo.setCustomValidity('Valor inválido');
          formValido = false;
        }

        if (campo.name === 'capacidade' && !validarCapacidade(campo.value)) {
          campo.setCustomValidity('Capacidade inválida');
          formValido = false;
        }

        // Validação de idade mínima para personal
        if (isPersonalForm && campo.type === 'date' && campo.name === 'data_nascimento') {
          if (!validarIdadeMinima(campo.value, 20)) {
            campo.setCustomValidity('Personal deve ter pelo menos 20 anos completos.');
            formValido = false;
          }
        }
      });

      if (!formValido) {
        e.preventDefault();
      }
    });
  });
});
// validação de CEP 


document.addEventListener('DOMContentLoaded', () => {
    const cepInput = document.querySelector('input[name="cep"]');
    const logradouroInput = document.querySelector('input[name="logradouro"]');
    const bairroInput = document.querySelector('input[name="bairro"]');
    const cidadeInput = document.querySelector('input[name="cidade"]');
    const estadoInput = document.querySelector('input[name="estado"]');

    let ultimoCepInvalido = '';
    let tentativasCepInvalido = 0;

    function limparCampos() {
        logradouroInput.value = '';
        bairroInput.value = '';
        cidadeInput.value = '';
        estadoInput.value = '';
    }

    cepInput.addEventListener('blur', async () => {
        const cep = cepInput.value.replace(/\D/g, '');

        if (cep.length !== 8) {
            // Caso CEP incompleto ou inválido
            if (ultimoCepInvalido === cep) {
                tentativasCepInvalido++;
            } else {
                tentativasCepInvalido = 1;
                ultimoCepInvalido = cep;
            }

            if (tentativasCepInvalido === 1) {
                alert("⚠️ CEP inválido. Verifique e tente novamente.");
                limparCampos();
            }
            return;
        }

        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (data.erro) {
                if (ultimoCepInvalido === cep) {
                    tentativasCepInvalido++;
                } else {
                    tentativasCepInvalido = 1;
                    ultimoCepInvalido = cep;
                }

                if (tentativasCepInvalido === 1) {
                    alert("❌ CEP não encontrado. Verifique o número digitado.");
                    limparCampos();
                }
                return;
            }

            // Reset se CEP for válido
            ultimoCepInvalido = '';
            tentativasCepInvalido = 0;

            // Preenche os campos
            logradouroInput.value = data.logradouro;
            bairroInput.value = data.bairro;
            cidadeInput.value = data.localidade;
            estadoInput.value = data.uf;
        } catch (error) {
            alert("⚠️ Erro ao buscar o CEP. Verifique sua conexão.");
            limparCampos();
            console.error("Erro:", error);
        }
    });
});
// validação de CEP 

// validação de Numero de telefone
document.addEventListener('DOMContentLoaded', () => {
    const telInput = document.getElementById('telefone');

    telInput.addEventListener('input', () => {
        let valor = telInput.value.replace(/\D/g, ''); // Remove tudo que não for número

        if (valor.length > 11) valor = valor.slice(0, 11); // Limita a 11 dígitos

        if (valor.length <= 10) {
            // Formato: (99) 9999-9999
            valor = valor.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        } else {
            // Formato: (99) 99999-9999
            valor = valor.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
        }

        telInput.value = valor;
    });
});


document.addEventListener('DOMContentLoaded', function() {
  const menu = document.querySelector('.menu-responsivo');
  const overlay = document.querySelector('.menu-overlay');
  const btnAbrir = document.getElementById('btn-abrir-menu');
  const btnFechar = document.getElementById('btn-fechar-menu');

  if (btnAbrir && menu && overlay) {
    btnAbrir.addEventListener('click', function() {
      menu.classList.add('ativo');
      overlay.classList.add('ativo');
    });
  }
  if (btnFechar && menu && overlay) {
    btnFechar.addEventListener('click', function() {
      menu.classList.remove('ativo');
      overlay.classList.remove('ativo');
    });
  }
  if (overlay && menu) {
    overlay.addEventListener('click', function() {
      menu.classList.remove('ativo');
      overlay.classList.remove('ativo');
    });
  }
});