@echo off
REM Altere para o diretório do seu projeto
cd /d "D:\Users\luif\Desktop:\Projetofitmaxpython\fitmaxonpython"

REM Troca para a branch develop
git checkout develop

REM Adiciona todas as alterações
git add .

git commit -m "Tela Feedback front"

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
git push origin develop 

echo [SUCESSO] Push realizado na branch DEVELOP com sucesso!
pause

