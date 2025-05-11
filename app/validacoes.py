#----------------------validação de cpf


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove pontuação

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False

    return True
#----------------------validação de cpf