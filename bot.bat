@echo off
title Lanceur Discord Bot - xxwfufu
cd /d "%~dp0"

echo [*] Activation de l'environnement Python...
:: Facultatif si tu utilises un venv :
:: call venv\Scripts\activate

echo [*] Lancement du bot...
python main.py

echo.
echo Le bot s'est arrêté. Appuie sur une touche pour fermer...
pause >nul
