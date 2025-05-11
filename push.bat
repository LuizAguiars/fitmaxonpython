
@echo off


REM Troca para a branch develop
git checkout develop

REM Adiciona todas as alterações
git add .

REM Comita com mensagem automática com data e hora
set DATAHORA=%date% %time%

git commit -m "tela de minha conta funcionando e update na tabela user e feedbacks %DATAHORA%"



REM Atualiza repositório local
git fetch origin

REM Verifica se main está à frente da develop
git merge-base --is-ancestor origin/develop origin/main
IF %ERRORLEVEL% EQU 1 (
    echo [INFO] A branch develop está atrás da main. Fazendo merge...
    git merge origin/main -m "Merge automático da main para develop"
) ELSE (
    echo [INFO] A branch develop já está atualizada com a main.
)

REM Envia para a branch develop no remoto
git push origin develop --force

echo [SUCESSO] Push realizado na branch DEVELOP com sucesso!
pause