@echo off
REM Altere para o diretório do seu projeto
cd /d C:\Users\gusta\Desktop\projetofitmax\fitmaxonpython

REM Adiciona todas as alterações
git add .

REM Comita com mensagem automática com data e hora
set DATAHORA=%date% %time%
git commit -m "novas instrucoes final %DATAHORA%"

git push

echo Push realizado na branch DEVELOP com sucesso!
pause
