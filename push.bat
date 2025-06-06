
@echo off


REM Troca para a branch develop
git checkout develop

REM Adiciona todas as alteracoes
git add .

REM Comita com mensagem automatica com data e hora
set DATAHORA=%date% %time%

git commit -m "Ajuste no modal editar personal e na data de emissao do certificado %DATAHORA%"



REM Atualiza repositorio local
git fetch origin

REM Verifica se main esta a frente da develop
git merge-base --is-ancestor origin/develop origin/main
IF %ERRORLEVEL% EQU 1 (
    echo [INFO] A branch develop está atrás da main. Fazendo merge...
    git merge origin/main -m "Merge automatico da main para develop"
) ELSE (
    echo [INFO] A branch develop já está atualizada com a main.
)

REM Envia para a branch develop no remoto
git push origin develop 

echo [SUCESSO] Push realizado na branch DEVELOP com sucesso!
pause