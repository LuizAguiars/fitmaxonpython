@echo off
SETLOCAL

REM Caminho para o seu projeto
cd https://github.com/LuizAguiars/fitmaxonpython.git

echo [INFO] Alternando para a branch develop...
git checkout develop

echo [INFO] Adicionando alterações...
git add .

echo [INFO] Criando commit...
git commit -m "Tela_Feedback_front"

echo [INFO] Atualizando repositório local...
git fetch origin

REM Verifica se origin/main está à frente de origin/develop
git merge-base --is-ancestor origin/main origin/develop
IF %ERRORLEVEL% EQU 1 (
    echo [INFO] Fazendo merge de origin/main em develop...
    git merge origin/main
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERRO] Conflito durante o merge! Resolva os conflitos e commite antes de continuar.
        goto end
    )
) ELSE (
    echo [INFO] develop já está atualizado com main.
)

REM Rebase com origin/develop para evitar push rejeitado
echo [INFO] Rebase com origin/develop para evitar conflitos de push...
git pull origin develop --rebase
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Conflito durante o rebase! Resolva e tente novamente.
    goto end
)

REM Push final
echo [INFO] Enviando alterações para o GitHub...
git push origin develop
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Push falhou. Verifique se há conflitos ou mudanças remotas.
) ELSE (
    echo [SUCESSO] Push realizado na branch DEVELOP com sucesso!
)

:end
pause
ENDLOCAL
