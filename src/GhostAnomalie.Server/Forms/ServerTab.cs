using GhostAnomalie.Common.Packets;
using GhostAnomalie.Common.Utils;
using GhostAnomalie.Server.Controls;
using GhostAnomalie.Server.Network;

namespace GhostAnomalie.Server.Forms
{
    public partial class ServerTab : UserControl
    {
        private MainForm _mainForm;
        private Listener _listener;

        // Contrôles
        private CustomTextBox _txtPort;
        private CustomTextBox _txtPassword;
        private CustomButton _btnStart;
        private CustomButton _btnStop;
        private CustomButton _btnDisconnect;
        private CustomButton _btnRefresh;
        private CustomListView _lstClients;
        private RichTextBox _txtLogs;
        private Label _lblClientsCount;
        private Label _lblStatus;

        private Dictionary<string, ClientHandler> _clients = new();
        private ClientHandler? _selectedClient;

        public ServerTab()
        {
            InitializeComponent();
        }

        public void Initialize(MainForm mainForm)
        {
            _mainForm = mainForm;
            _listener = mainForm.GetListener();
        }

        private void InitializeComponent()
        {
            this.BackColor = DarkTheme.BackColor;

            // ===== LEFT PANEL =====
            var leftPanel = new Panel
            {
                Dock = DockStyle.Left,
                Width = 350,
                BackColor = DarkTheme.PanelColor,
                Padding = new Padding(10)
            };

            // Config Group
            var configGroup = new GroupBox
            {
                Text = "⚙️ CONFIGURATION",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Top,
                Height = 150,
                Padding = new Padding(5)
            };

            var lblPort = new Label
            {
                Text = "🔌 Port:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 28),
                AutoSize = true
            };

            _txtPort = new CustomTextBox
            {
                Text = Constants.DefaultPort.ToString(),
                Location = new Point(80, 25),
                Width = 180
            };

            var lblPassword = new Label
            {
                Text = "🔑 Mot de passe:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 58),
                AutoSize = true
            };

            _txtPassword = new CustomTextBox
            {
                Text = Constants.DefaultPassword,
                Location = new Point(80, 55),
                Width = 180,
                UseSystemPasswordChar = true
            };

            _btnStart = new CustomButton
            {
                Text = "▶️ START SERVER",
                Location = new Point(10, 95),
                Width = 145,
                Height = 35,
                BackColor = Color.FromArgb(0, 200, 100),
                ForeColor = Color.FromArgb(5, 5, 15),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };
            _btnStart.Click += BtnStart_Click;

            _btnStop = new CustomButton
            {
                Text = "⏹️ STOP",
                Location = new Point(165, 95),
                Width = 145,
                Height = 35,
                BackColor = DarkTheme.ErrorColor,
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                Enabled = false
            };
            _btnStop.Click += BtnStop_Click;

            configGroup.Controls.Add(lblPort);
            configGroup.Controls.Add(_txtPort);
            configGroup.Controls.Add(lblPassword);
            configGroup.Controls.Add(_txtPassword);
            configGroup.Controls.Add(_btnStart);
            configGroup.Controls.Add(_btnStop);

            // Clients Group
            var clientsGroup = new GroupBox
            {
                Text = "👥 CLIENTS CONNECTÉS",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Fill,
                Padding = new Padding(5)
            };

            _lblClientsCount = new Label
            {
                Text = "👥 0 clients",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Dock = DockStyle.Bottom,
                Height = 25,
                TextAlign = ContentAlignment.MiddleLeft,
                Padding = new Padding(5, 0, 0, 0)
            };

            _lstClients = new CustomListView
            {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true
            };
            _lstClients.Columns.Add("Client", 150);
            _lstClients.Columns.Add("IP", 120);
            _lstClients.Columns.Add("Status", 80);
            _lstClients.SelectedIndexChanged += LstClients_SelectedIndexChanged;

            clientsGroup.Controls.Add(_lblClientsCount);
            clientsGroup.Controls.Add(_lstClients);

            // Action buttons
            var btnPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 45,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 5, 0, 5)
            };

            _btnDisconnect = new CustomButton
            {
                Text = "🔌 DÉCONNECTER",
                Dock = DockStyle.Left,
                Width = 120,
                Height = 30,
                BackColor = DarkTheme.ErrorColor,
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                Enabled = false
            };
            _btnDisconnect.Click += BtnDisconnect_Click;

            _btnRefresh = new CustomButton
            {
                Text = "🔄 RAFRAÎCHIR",
                Dock = DockStyle.Left,
                Width = 100,
                Height = 30,
                BackColor = DarkTheme.ControlColor,
                ForeColor = DarkTheme.TextColor
            };
            _btnRefresh.Click += BtnRefresh_Click;

            btnPanel.Controls.Add(_btnDisconnect);
            btnPanel.Controls.Add(_btnRefresh);

            leftPanel.Controls.Add(btnPanel);
            leftPanel.Controls.Add(clientsGroup);
            leftPanel.Controls.Add(configGroup);
            this.Controls.Add(leftPanel);

            // ===== RIGHT PANEL =====
            var rightPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = DarkTheme.BackColor,
                Padding = new Padding(10)
            };

            // Commands
            var cmdGroup = new GroupBox
            {
                Text = "⌨️ COMMANDES",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Top,
                Height = 80,
                Padding = new Padding(5)
            };

            var cmdPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent,
                Padding = new Padding(5)
            };

            var txtCommand = new CustomTextBox
            {
                Dock = DockStyle.Left,
                Width = cmdGroup.Width - 100,
                Height = 30,
                Font = DarkTheme.MonospaceFont
            };
            txtCommand.KeyPress += (s, e) => {
                if (e.KeyChar == (char)Keys.Enter)
                {
                    SendCommand(txtCommand.Text);
                    txtCommand.Clear();
                }
            };

            var btnSend = new CustomButton
            {
                Text = "🚀 Envoyer",
                Dock = DockStyle.Right,
                Width = 80,
                Height = 30,
                BackColor = DarkTheme.HighlightColor,
                ForeColor = Color.Black
            };
            btnSend.Click += (s, e) => {
                SendCommand(txtCommand.Text);
                txtCommand.Clear();
            };

            cmdPanel.Controls.Add(btnSend);
            cmdPanel.Controls.Add(txtCommand);
            cmdGroup.Controls.Add(cmdPanel);

            // Quick commands
            var quickGroup = new GroupBox
            {
                Text = "📋 COMMANDES RAPIDES",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Top,
                Height = 60,
                Padding = new Padding(5)
            };

            var quickPanel = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent,
                FlowDirection = FlowDirection.LeftToRight,
                WrapContents = true,
                Padding = new Padding(5)
            };

            string[] quickCommands = { "screenshot", "sysinfo", "ls", "shutdown", "restart", "lock", "ping" };
            foreach (var cmd in quickCommands)
            {
                var btn = new CustomButton
                {
                    Text = cmd,
                    Width = 90,
                    Height = 30,
                    BackColor = DarkTheme.ControlColor,
                    ForeColor = DarkTheme.TextColor,
                    Font = new Font("Segoe UI", 8)
                };
                btn.Click += (s, e) => SendCommand(cmd);
                quickPanel.Controls.Add(btn);
            }

            quickGroup.Controls.Add(quickPanel);

            // Logs
            var logGroup = new GroupBox
            {
                Text = "📝 LOGS",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Fill,
                Padding = new Padding(5)
            };

            _txtLogs = new RichTextBox
            {
                Dock = DockStyle.Fill,
                BackColor = DarkTheme.BackColor,
                ForeColor = DarkTheme.TextColor,
                Font = DarkTheme.MonospaceFont,
                ReadOnly = true,
                BorderStyle = BorderStyle.None
            };

            logGroup.Controls.Add(_txtLogs);

            rightPanel.Controls.Add(logGroup);
            rightPanel.Controls.Add(quickGroup);
            rightPanel.Controls.Add(cmdGroup);
            this.Controls.Add(rightPanel);
        }

        // ============================================================
        // ÉVÉNEMENTS
        // ============================================================

        private async void BtnStart_Click(object? sender, EventArgs e)
        {
            if (!int.TryParse(_txtPort.Text, out int port))
            {
                Log("❌ Port invalide");
                return;
            }

            var password = _txtPassword.Text;
            if (string.IsNullOrEmpty(password))
            {
                Log("❌ Mot de passe requis");
                return;
            }

            try
            {
                await _listener.Start(port, password);
                _btnStart.Enabled = false;
                _btnStop.Enabled = true;
                _mainForm.SetStatus("🟢 Serveur en ligne", true);
                Log($"✅ Serveur démarré sur le port {port}");
            }
            catch (Exception ex)
            {
                Log($"❌ Erreur: {ex.Message}");
            }
        }

        private void BtnStop_Click(object? sender, EventArgs e)
        {
            _listener.Stop();
            _btnStart.Enabled = true;
            _btnStop.Enabled = false;
            _mainForm.SetStatus("🔴 Serveur arrêté", false);
            Log("⏹️ Serveur arrêté");
        }

        private void BtnDisconnect_Click(object? sender, EventArgs e)
        {
            if (_selectedClient != null)
            {
                _selectedClient.Disconnect();
                _selectedClient = null;
                _btnDisconnect.Enabled = false;
                Log("🔌 Client déconnecté");
            }
        }

        private void BtnRefresh_Click(object? sender, EventArgs e)
        {
            UpdateClientsList();
        }

        private void LstClients_SelectedIndexChanged(object? sender, EventArgs e)
        {
            if (_lstClients.SelectedItems.Count > 0)
            {
                var item = _lstClients.SelectedItems[0];
                var clientId = item.SubItems[0].Text;
                _selectedClient = _mainForm.GetClient(clientId);
                _btnDisconnect.Enabled = _selectedClient != null;
            }
            else
            {
                _selectedClient = null;
                _btnDisconnect.Enabled = false;
            }
        }

        // ============================================================
        // MÉTHODES PUBLIQUES
        // ============================================================

        public void Log(string message)
        {
            if (_txtLogs.InvokeRequired)
            {
                _txtLogs.Invoke(() => Log(message));
                return;
            }

            var timestamp = DateTime.Now.ToString("HH:mm:ss");
            _txtLogs.AppendText($"[{timestamp}] {message}\n");
            _txtLogs.ScrollToCaret();

            if (_txtLogs.Lines.Length > 1000)
            {
                var lines = _txtLogs.Lines.Skip(100).ToArray();
                _txtLogs.Clear();
                _txtLogs.AppendText(string.Join("\n", lines));
            }
        }

        public void AddClient(ClientHandler client)
        {
            if (_lstClients.InvokeRequired)
            {
                _lstClients.Invoke(() => AddClient(client));
                return;
            }

            var item = new ListViewItem(client.ClientId);
            item.SubItems.Add(client.IpAddress);
            item.SubItems.Add("🟢 En ligne");
            _lstClients.Items.Add(item);
            UpdateClientsCount(_lstClients.Items.Count);
        }

        public void RemoveClient(string clientId)
        {
            if (_lstClients.InvokeRequired)
            {
                _lstClients.Invoke(() => RemoveClient(clientId));
                return;
            }

            foreach (ListViewItem item in _lstClients.Items)
            {
                if (item.SubItems[0].Text == clientId)
                {
                    _lstClients.Items.Remove(item);
                    break;
                }
            }

            UpdateClientsCount(_lstClients.Items.Count);
        }

        public void UpdateClientsCount(int count)
        {
            if (_lblClientsCount.InvokeRequired)
            {
                _lblClientsCount.Invoke(() => UpdateClientsCount(count));
                return;
            }

            _lblClientsCount.Text = $"👥 {count} clients";
        }

        public void UpdateClientsList()
        {
            if (_lstClients.InvokeRequired)
            {
                _lstClients.Invoke(() => UpdateClientsList());
                return;
            }

            var clients = _mainForm.GetClients();
            _lstClients.Items.Clear();

            foreach (var client in clients.Values)
            {
                var item = new ListViewItem(client.ClientId);
                item.SubItems.Add(client.IpAddress);
                item.SubItems.Add("🟢 En ligne");
                _lstClients.Items.Add(item);
            }

            UpdateClientsCount(_lstClients.Items.Count);
        }

        public ClientHandler GetSelectedClient()
        {
            return _selectedClient;
        }

        private void SendCommand(string command)
        {
            if (string.IsNullOrEmpty(command))
                return;

            if (_selectedClient == null)
            {
                Log("❌ Aucun client sélectionné");
                return;
            }

            var packet = new CommandPacket(command);
            _selectedClient.SendCommand(packet);
            Log($"📤 Commande envoyée: {command}");
        }
    }
}
