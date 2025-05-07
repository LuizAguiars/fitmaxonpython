@echo off
cd /d "C:\Users\Luiz Aguiar\Documents\fitmaxcompleto"
echo Verificando atualizacoes...

:: Buscar atualizações do repositório remoto
git fetch

:: Verificar se há commits na origem que não estão localmente
git status -uno | find "Your branch is behind" >nul
if %errorlevel%==0 (
    echo Ha atualizações disponiveis. Realizando pull...
    git pull
) else (
    echo Seu repositorio ja esta atualizado.
)

pause
