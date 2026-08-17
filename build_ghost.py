# build_ghost.py - Compilateur Ghost Anomalie
import os
import sys
import subprocess
import shutil
import platform
import time
from datetime import datetime

# ===== CONFIGURATION =====
VERSION = "1.3.0"
NOM_APP = "GhostAnomalie"
AUTEUR = "🖤 Dev Messy"

# ===== COULEURS =====
class Couleurs:
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    JAUNE = '\033[93m'
    BLEU = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLANC = '\033[97m'
    GRAS = '\033[1m'
    FIN = '\033[0m'

def log(message, couleur=Couleurs.BLANC):
    """Affiche un message avec couleur"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{couleur}[{timestamp}] {message}{Couleurs.FIN}")

def afficher_banner():
    """Affiche la bannière"""
    print(f"""
{Couleurs.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {Couleurs.VERT}👻 GHOST ANOMALIE - COMPILATEUR ULTIME{Couleurs.CYAN}                    ║
║   {Couleurs.BLANC}v{VERSION} - Par {AUTEUR}{Couleurs.CYAN}                         ║
║   {Couleurs.JAUNE}📦 Transforme ghost.py en EXE prêt à l'emploi{Couleurs.CYAN}        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Couleurs.FIN}
    """)

def verifier_dependances():
    """Vérifie et installe les dépendances"""
    log("🔍 Vérification des dépendances...", Couleurs.BLEU)
    
    dependances = [
        "pillow",
        "pyinstaller",
        "opencv-python",
        "pyaudio",
        "pywin32",
        "psutil",
        "wmi",
        "cryptography"
    ]
    
    a_installer = []
    
    for dep in dependances:
        try:
            __import__(dep.replace("-", "_"))
            log(f"✅ {dep} - OK", Couleurs.VERT)
        except ImportError:
            log(f"❌ {dep} - Non installé", Couleurs.ROUGE)
            a_installer.append(dep)
    
    if a_installer:
        log(f"📦 Installation de {len(a_installer)} dépendances...", Couleurs.JAUNE)
        for dep in a_installer:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             capture_output=True, check=True)
                log(f"✅ {dep} installé", Couleurs.VERT)
            except Exception as e:
                log(f"❌ Erreur installation {dep}: {e}", Couleurs.ROUGE)
                return False
    
    log("✅ Toutes les dépendances sont OK !", Couleurs.VERT)
    return True

def verifier_fichier():
    """Vérifie que ghost.py existe"""
    if not os.path.exists("ghost.py"):
        log("❌ Fichier ghost.py introuvable !", Couleurs.ROUGE)
        log("📁 Assure-toi d'avoir ghost.py dans le dossier courant", Couleurs.JAUNE)
        return False
    
    taille = os.path.getsize("ghost.py") / 1024
    log(f"✅ ghost.py trouvé ({taille:.1f} KB)", Couleurs.VERT)
    return True

def creer_icone():
    """Crée une icône pour l'application"""
    try:
        log("🎨 Création de l'icône...", Couleurs.BLEU)
        
        if os.path.exists("ghost.ico"):
            log("✅ Icône déjà existante", Couleurs.VERT)
            return True
        
        try:
            from PIL import Image, ImageDraw
            
            # Créer une image 256x256
            img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Fantôme
            draw.ellipse((40, 40, 216, 200), fill=(0, 255, 136, 200))
            draw.ellipse((70, 100, 110, 140), fill=(5, 5, 15, 255))
            draw.ellipse((146, 100, 186, 140), fill=(5, 5, 15, 255))
            
            # Bouche
            draw.arc((90, 140, 166, 180), start=0, end=180, fill=(5, 5, 15, 255), width=10)
            
            # Sauvegarder
            img.save('ghost.ico', format='ICO', sizes=[(256, 256)])
            log("✅ Icône créée: ghost.ico", Couleurs.VERT)
            return True
            
        except Exception as e:
            log(f"⚠️ Impossible de créer l'icône: {e}", Couleurs.JAUNE)
            return True
            
    except Exception as e:
        log(f"⚠️ Erreur icône: {e}", Couleurs.JAUNE)
        return True

def compiler():
    """Compile ghost.py en EXE"""
    log("🔧 Compilation de ghost.py en EXE...", Couleurs.BLEU)
    
    # Nettoyer les builds précédents
    for dossier in ["build", "dist", "__pycache__"]:
        if os.path.exists(dossier):
            try:
                shutil.rmtree(dossier)
                log(f"🗑️ Dossier {dossier} nettoyé", Couleurs.JAUNE)
            except:
                pass
    
    # Fichier spec
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ghost.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL', 'PIL.ImageGrab', 'PIL.Image',
        'cv2',
        'pyaudio', 'wave',
        'win32api', 'win32con', 'win32gui', 'win32process', 
        'win32clipboard', 'win32ui', 'win32pdh', 'win32security',
        'win32file', 'win32event', 'win32service', 'win32serviceutil',
        'win32com.client',
        'wmi',
        'psutil',
        'cryptography', 'cryptography.fernet',
        'socket', 'threading', 'subprocess', 'os', 'sys', 'time',
        'datetime', 'json', 'base64', 'io', 'ctypes', 'struct',
        'zlib', 'random', 're', 'sqlite3', 'shutil', 'tempfile',
        'hashlib', 'ipaddress', 'urllib', 'requests',
        'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.filedialog',
        'tkinter.messagebox'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{NOM_APP}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ghost.ico' if os.path.exists('ghost.ico') else None,
)
"""
    
    # Écrire le spec file
    with open('ghost.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Commande PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--log-level", "INFO",
        "ghost.spec"
    ]
    
    log("⏳ Compilation en cours... (5-10 minutes)", Couleurs.JAUNE)
    log("📦 L'EXE sera dans le dossier 'dist/'", Couleurs.BLEU)
    
    start_time = time.time()
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                  text=True, bufsize=1)
        
        # Afficher la progression en temps réel
        for line in process.stdout:
            if "INFO" in line:
                log(line.strip(), Couleurs.BLANC)
            elif "WARNING" in line:
                log(line.strip(), Couleurs.JAUNE)
            elif "ERROR" in line:
                log(line.strip(), Couleurs.ROUGE)
        
        process.wait()
        
        if process.returncode == 0:
            temps = time.time() - start_time
            log(f"✅ Compilation réussie en {temps:.1f} secondes !", Couleurs.VERT)
            return True
        else:
            log(f"❌ Erreur de compilation (code: {process.returncode})", Couleurs.ROUGE)
            return False
            
    except Exception as e:
        log(f"❌ Erreur: {e}", Couleurs.ROUGE)
        return False

def optimiser_exe():
    """Optimise l'EXE généré"""
    try:
        exe_path = os.path.join("dist", f"{NOM_APP}.exe")
        
        if not os.path.exists(exe_path):
            return False
        
        taille = os.path.getsize(exe_path) / (1024*1024)
        log(f"📦 Taille de l'EXE: {taille:.1f} MB", Couleurs.BLEU)
        
        # UPX si disponible
        try:
            import upx
            log("📦 Compression UPX...", Couleurs.BLEU)
            # UPX est déjà inclus dans PyInstaller
        except:
            pass
        
        return True
        
    except Exception as e:
        log(f"⚠️ Erreur optimisation: {e}", Couleurs.JAUNE)
        return True

def creer_lanceur():
    """Crée un fichier lanceur avec les commandes"""
    try:
        contenu = f'''@echo off
echo ============================================
echo    👻 GHOST ANOMALIE - {VERSION}
echo    📦 Lancement du contrôleur...
echo ============================================
echo.
echo ✅ GhostAnomalie.exe généré avec succès !
echo 📁 Dossier: dist/
echo.
echo 🔥 Commandes:
echo    - Double-clique sur GhostAnomalie.exe
echo    - Ou exécute: start dist\\GhostAnomalie.exe
echo.
pause
start dist\\GhostAnomalie.exe
'''
        
        with open("Lancer_Ghost.bat", "w", encoding='utf-8') as f:
            f.write(contenu)
        
        log("✅ Fichier lanceur créé: Lancer_Ghost.bat", Couleurs.VERT)
        return True
    except:
        return False

def afficher_resultat():
    """Affiche le résultat final"""
    print(f"""
{Couleurs.VERT}╔═══════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {Couleurs.GRAS}🎉 GHOST ANOMALIE - COMPILATION TERMINÉE !{Couleurs.VERT}                ║
║                                                                   ║
║   {Couleurs.BLANC}📁 Fichier généré : {Couleurs.JAUNE}dist/{NOM_APP}.exe{Couleurs.BLANC}               ║
║                                                                   ║
║   {Couleurs.CYAN}🚀 Pour lancer :{Couleurs.BLANC}                                    ║
║   {Couleurs.JAUNE}   - Double-clique sur dist/{NOM_APP}.exe          ║
║   {Couleurs.JAUNE}   - Ou exécute Lancer_Ghost.bat                  ║
║                                                                   ║
║   {Couleurs.MAGENTA}📋 Commandes disponibles : 92 commandes{Couleurs.VERT}              ║
║   {Couleurs.CYAN}👥 Interface de contrôle + Générateur de client{Couleurs.VERT}        ║
║                                                                   ║
║   {Couleurs.ROUGE}⚠️  Usage ÉDUCATIF UNIQUEMENT !{Couleurs.VERT}                      ║
║   {Couleurs.ROUGE}⚠️  Utilise sur TES propres machines uniquement{Couleurs.VERT}      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Couleurs.FIN}
    """)

def menu():
    """Menu principal"""
    print(f"""
{Couleurs.CYAN}┌─────────────────────────────────────────────────────────┐
│  {Couleurs.GRAS}👻 GHOST ANOMALIE - COMPILATEUR{Couleurs.CYAN}                 │
├─────────────────────────────────────────────────────────┤
│  {Couleurs.BLANC}1. {Couleurs.VERT}Compiler ghost.py en EXE{Couleurs.BLANC}              │
│  {Couleurs.BLANC}2. {Couleurs.JAUNE}Vérifier les dépendances{Couleurs.BLANC}              │
│  {Couleurs.BLANC}3. {Couleurs.MAGENTA}Nettoyer les fichiers temporaires{Couleurs.BLANC}      │
│  {Couleurs.BLANC}4. {Couleurs.ROUGE}Quitter{Couleurs.BLANC}                             │
└─────────────────────────────────────────────────────────┘
    """)
    
    return input(f"{Couleurs.CYAN}➜ Choisis une option (1-4): {Couleurs.FIN}")

def nettoyer():
    """Nettoie les fichiers temporaires"""
    log("🧹 Nettoyage en cours...", Couleurs.BLEU)
    
    dossiers = ["build", "dist", "__pycache__", "*.spec"]
    for dossier in dossiers:
        try:
            if os.path.exists(dossier):
                shutil.rmtree(dossier)
                log(f"🗑️ {dossier} supprimé", Couleurs.JAUNE)
        except:
            pass
    
    log("✅ Nettoyage terminé", Couleurs.VERT)

def main():
    """Fonction principale"""
    # Effacer l'écran
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Afficher la bannière
    afficher_banner()
    
    while True:
        choix = menu()
        
        if choix == "1":
            log("🚀 Lancement de la compilation...", Couleurs.VERT)
            
            # Vérifier les prérequis
            if not verifier_fichier():
                continue
            
            if not verifier_dependances():
                continue
            
            if not creer_icone():
                continue
            
            # Compiler
            if compiler():
                optimiser_exe()
                creer_lanceur()
                afficher_resultat()
            else:
                log("❌ La compilation a échoué", Couleurs.ROUGE)
            
            input(f"{Couleurs.CYAN}\nAppuie sur Entrée pour continuer...{Couleurs.FIN}")
            
        elif choix == "2":
            verifier_dependances()
            input(f"{Couleurs.CYAN}\nAppuie sur Entrée pour continuer...{Couleurs.FIN}")
            
        elif choix == "3":
            nettoyer()
            input(f"{Couleurs.CYAN}\nAppuie sur Entrée pour continuer...{Couleurs.FIN}")
            
        elif choix == "4":
            log("👋 Au revoir !", Couleurs.MAGENTA)
            sys.exit(0)
            
        else:
            log("❌ Option invalide", Couleurs.ROUGE)
            time.sleep(1)
        
        # Effacer l'écran
        os.system('cls' if os.name == 'nt' else 'clear')
        afficher_banner()

if __name__ == "__main__":
    main()