@echo off
echo Atualizando repositorio local com a branch develop do remoto...
git checkout develop
git pull origin develop

echo Repositorio atualizado com sucesso!
pause