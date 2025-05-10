@echo off
echo Atualizando repositório local com a branch develop do remoto...
git checkout develop
git pull origin develop

echo Repositório atualizado com sucesso!
pause