@echo off
echo ============================================
echo    👻 GHOST ANOMALIE - BUILD
echo ============================================
echo.

echo 📦 Restauration des dépendances...
dotnet restore GhostAnomalie.sln

echo.
echo 🔧 Compilation...
dotnet build GhostAnomalie.sln -c Release

echo.
echo 📦 Publication...
dotnet publish src/GhostAnomalie.Server/GhostAnomalie.Server.csproj -c Release -o publish -r win-x64 --self-contained false -p:DebugType=none -p:DebugSymbols=false

echo.
echo ✅ Build terminé !
echo 📁 Fichier: publish\GhostAnomalie.exe
pause
