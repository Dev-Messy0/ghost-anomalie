# 👻 Ghost Anomalie - Advanced Remote Administration Tool

> **⚠️ IMPORTANT: This tool is for EDUCATIONAL PURPOSES ONLY. Use only on your own devices or with explicit written consent.**

[![Version](https://img.shields.io/badge/version-1.3.0-brightgreen.svg)](https://github.com/Dev-Messy0/ghost-anomalie)
[![License](https://img.shields.io/badge/license-EDUCATIONAL%20ONLY-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands Reference](#commands-reference)
- [Security & Legal](#security--legal)
- [Disclaimer](#disclaimer)
- [FAQ](#faq)
- [License](#license)

---

## 🔍 Overview

**Ghost Anomalie** is a comprehensive remote administration and cybersecurity education tool designed for:

- System administrators managing multiple machines
- Cybersecurity students learning about RATs and network security
- Penetration testing on authorized systems
- Educational demonstrations in controlled environments

### What Makes Ghost Anomalie Different?

| Feature | Description |
|---------|-------------|
| 🖥️ **Complete Control** | Full remote desktop, file management, and system control |
| 🔐 **Education First** | Built to teach cybersecurity concepts safely |
| 🚀 **92+ Commands** | Every feature you need to understand RAT functionality |
| 📦 **All-in-One** | Controller + Client generator in a single EXE |
| 👻 **Stealth Options** | Learn how persistence and hiding techniques work |
| 🎯 **Real-World Skills** | Practice security concepts in a controlled environment |

---

## ⚡ Features

### 🖥️ Remote Control
- **Real-time Desktop Streaming** - Watch and control remote screens
- **Mouse & Keyboard Control** - Full input emulation
- **Application Launcher** - Run programs remotely (visible/hidden)
- **Multiple Monitor Support** - Switch between displays

### 🔐 Security Testing
- **Keylogger** - Understand how input capture works
- **Password Extraction** - Educational WiFi & browser password recovery
- **Clipboard Monitoring** - Learn data interception techniques
- **Screen Recording** - Capture sessions for analysis

### 📁 File Management
- **Full File Browser** - Navigate remote file systems
- **Upload/Download** - Transfer files securely
- **Search & Filter** - Find specific files quickly
- **Archive Support** - Compress/Decompress folders

### 🎥 Surveillance Tools
- **Webcam Access** - Test camera security (with user consent)
- **Microphone Recording** - Understand audio surveillance risks
- **File Monitoring** - Detect new/modified files in real-time

### 🛡️ Security Features
- **Persistent Installation** - Learn how malware maintains access
- **Process Hiding** - Understand stealth techniques
- **Anti-Debug Protection** - See how malware avoids analysis
- **Anti-VM Detection** - Detect virtual environments

### 🌐 Network Tools
- **Network Scanner** - Discover devices on local networks
- **Port Scanner** - Identify open ports and services
- **WiFi Management** - View and connect to wireless networks
- **DNS Tools** - Flush cache and troubleshoot DNS

---

## 📦 Installation

### Prerequisites
- **Windows 10/11** or **Linux** (with Wine)
- **Python 3.8+** (for development)
- **Administrator privileges** (for some features)

### Method 1: Pre-compiled EXE (Recommended)
```bash
# 1. Download the latest release from GitHub
# 2. Extract the ZIP file
# 3. Run GhostAnomalie.exe
# 4. No installation required - portable application!
```

Method 2: From Source

```bash
# 1. Clone the repository
git clone https://github.com/Dev-Messy0/ghost-anomalie.git
cd ghost-anomalie

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python ghost.py

# 4. Or compile to EXE
python build_ghost.py
```

Method 3: Quick Setup with Script

```bash
# Windows
compile.bat

# Linux/Mac
python build_ghost.py
```

---

🚀 Quick Start

Step 1: Launch the Controller

```
1. Double-click GhostAnomalie.exe
2. The main interface will open
3. You'll see the "OFFLINE" status
```

Step 2: Configure Server

```
1. Enter your IP address (or 127.0.0.1 for local testing)
2. Set a port (default: 4444)
3. Choose a password (default: admin123)
4. Click "START SERVER"
5. Status changes to "ONLINE"
```

Step 3: Generate a Client

```
1. In the GENERATOR section:
   - Enter a name for the client
   - Choose a filename for the EXE (e.g., WindowsUpdate)
   - Select your options (Persistance, Stealth, etc.)
2. Click "GENERATE CLIENT .EXE"
3. Wait for compilation (5-10 minutes)
4. The EXE appears in the "clients/" folder
```

Step 4: Deploy and Control

```
1. Copy the generated EXE to the target machine
2. Run the EXE (it installs silently)
3. The client appears in the "CONNECTED CLIENTS" list
4. Select it and start sending commands!
```

---

📋 Commands Reference

🖥️ System Commands

Command Description
screenshot Capture remote screen
sysinfo Get system information
cmd <command> Execute system command
shutdown Shutdown remote PC
restart Restart remote PC
lock Lock workstation
logoff Log off user
hibernate Hibernate PC

📁 File Commands

Command Description
ls [path] List files in directory
cd <path> Change directory
pwd Print working directory
mkdir <name> Create folder
rm <path> Delete file/folder
mv <old> <new> Move/rename
download <file> Download file
upload <name> <content> Upload file

🖱️ Mouse & Keyboard

Command Description
souris_move <x> <y> Move mouse (0-1)
`souris_click <1 2
`souris_scroll <up down>`
souris_glisser <x1> <y1> <x2> <y2> Drag and drop
clavier_texte <text> Type text
clavier_touche <key> Press key

🎯 Advanced Commands

Command Description
bureau_start Start desktop streaming
bureau_stop Stop streaming
bureau_ecrans List monitors
ecran_noir Activate black screen
rotation <angle> Rotate screen
camera_start Start webcam
camera_photo Take photo
camera_stealth Stealth photo
micro_start Start microphone
micro_record <sec> Record audio
keylogger_start Start keylogger
keylogger_stop Stop keylogger
clipboard_get Get clipboard
clipboard_set <text> Set clipboard
pass_wifi Extract WiFi passwords
pass_chrome Extract Chrome passwords
pass_all Extract all passwords
crypto_wallets Find crypto wallets
network_scan Scan local network
port_scan <ip> <ports> Scan ports
arp_scan ARP scan
wifi_list List WiFi networks
dns_flush Flush DNS cache
processus_list List processes
processus_kill <PID> Kill process
service_list List services
service_start <name> Start service
service_stop <name> Stop service
app_lancer <app> Launch application
app_cacher_tout Hide all windows
app_montrer_tout Show all windows
app_fenetres List windows
record_start Start screen recording
record_stop Stop recording
surveillance_start Start surveillance
surveillance_stop Stop surveillance
search_files <pattern> Search files

🛡️ Security & Stealth

Command Description
hide Hide process
persist Add persistence
uac_bypass Bypass UAC
polymorph Change file hash
inject <process> Inject into process
update <url> Auto-update
selfdestruct Self-destruct
anti_vm Detect VM
anti_debug Detect debugger
anti_av Detect antivirus

🎮 Fun Commands

Command Description
popup <message> Show popup
speak <text> Text-to-speech
website <url> Open website
beep Beep
cd_eject Eject CD drive
cd_close Close CD drive
mouse_disable Disable mouse
mouse_enable Enable mouse
keyboard_disable Disable keyboard
keyboard_enable Enable keyboard
volume_set <level> Set volume
volume_mute Mute volume

💡 Total: 92+ commands available!

---

🔒 Security & Legal

⚠️ Important Legal Notice

This software is provided for EDUCATIONAL PURPOSES ONLY.

By using this software, you agree to:

1. Use only on systems you own or have explicit written permission to test
2. Not use for malicious purposes including but not limited to:
   · Unauthorized access
   · Data theft
   · Identity theft
   · Financial fraud
   · Cyber espionage
   · Any illegal activity
3. Follow all applicable laws in your jurisdiction

📜 Laws by Region

Country Law Penalty
USA CFAA Up to 20 years, $250,000
UK Computer Misuse Act Up to 10 years, unlimited fine
France Loi Godfrain Up to 5 years, €300,000
Gabon Loi N°001/2019 Up to 10 years, 300,000,000 FCFA
Canada PIPEDA Up to 10 years
Australia Cybercrime Act Up to 10 years

🛡️ Responsible Use

✅ DO:

· Test on your own devices
· Use in CTF competitions
· Learn cybersecurity concepts
· Practice in virtual labs
· Get written permission for testing
· Use for security research

❌ DO NOT:

· Use on others' devices without permission
· Steal personal information
· Spy on others
· Spread malware
· Use for financial gain
· Bypass security measures maliciously

---

📖 Educational Resources

What You Can Learn

1. Remote Administration Concepts
   · Client-server architecture
   · Network communication
   · Command execution
2. Security Vulnerabilities
   · How RATs work
   · Detection methods
   · Prevention techniques
3. Cybersecurity Skills
   · Penetration testing
   · Incident response
   · Digital forensics
4. Network Security
   · TCP/IP fundamentals
   · Port scanning
   · Network monitoring

Recommended Certifications

· CEH - Certified Ethical Hacker
· OSCP - Offensive Security Certified Professional
· Security+ - CompTIA Security+
· CISSP - Certified Information Systems Security Professional

---

❓ FAQ

Q: Is it legal to use Ghost Anomalie?

A: Yes, if you use it on YOUR OWN devices or with written authorization. Use on devices without consent is illegal.

Q: Does it work on Linux/Mac?

A: The client only works on Windows. The controller can run on Linux/Mac with Wine.

Q: How can I protect myself from this type of tool?

A: Use antivirus, firewall, strong passwords, and avoid running unknown files.

Q: Can I modify the code?

A: Yes, for personal educational use. Redistribution must include this license.

Q: What if I find a bug?

A: Open an issue on GitHub or contact us via email.

Q: Is this a virus?

A: No, it's an educational tool. However, antivirus software may flag it because of its functionality.

Q: Can I use this commercially?

A: No, commercial use is strictly prohibited.

---

🤝 Contributing

We welcome contributions that improve the educational value of this project!

Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

What We Accept

· Bug fixes
· Security improvements
· Documentation updates
· Educational content
· New educational features

What We Don't Accept

· Malicious features
· Illegal functionality
· Anti-security features
· Privacy violations

---

📄 License

```
GHOST ANOMALIE - Educational License v1.0

Copyright (c) 2026 Dev Messy

Permission is hereby granted for EDUCATIONAL PURPOSES ONLY.
The software may be used, studied, and modified for:
- Personal learning
- Security research
- Authorized penetration testing

Commercial use is strictly prohibited.
Redistribution must include this license.
No warranty is provided, use at your own risk.

This software is NOT for malicious purposes.
Any illegal use is the sole responsibility of the user.
```

---

⭐ Support

· Documentation: Wiki
· Issues: GitHub Issues
· Discussions: GitHub Discussions

---

🙏 Acknowledgments

· The cybersecurity community for continuous learning
· Open source contributors
· Ethical hackers who make the internet safer

---

🔗 Useful Links

· OWASP - Open Web Application Security Project
· CEH - Certified Ethical Hacker
· TryHackMe - Learn cybersecurity
· HackTheBox - Practice pentesting
· Cybrary - Free cybersecurity courses

---

📊 Version History

Version Date Changes
1.3.0 2026 Complete rewrite, 92 commands, EXE generator
1.0.0 2025 Initial release

---

👻 Remember: With great power comes great responsibility. Use this knowledge to protect, not to harm.

---

🏁 Quick Links

⬆ Back to Top |
Features |
Installation |
Commands |
Security |
License

---

Made with ❤️ for the cybersecurity community

**Structure finale :**
bash```
Ghost_Anomalie/
├── ghost.py
├── build_ghost.py
├── compile.bat
├── README.md     
├── FRANÇAIS.md
├── SECURITY.md
├── requirements.txt
└── LICENSE
```