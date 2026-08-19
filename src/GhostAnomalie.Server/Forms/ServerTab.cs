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
