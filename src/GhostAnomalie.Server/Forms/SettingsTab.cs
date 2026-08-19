using GhostAnomalie.Common.Utils;
using GhostAnomalie.Server.Controls;
using GhostAnomalie.Server.Utils;

namespace GhostAnomalie.Server.Forms
{
    public partial class SettingsTab : UserControl
    {
        private MainForm _mainForm;

        // === CHAMPS ===
        private CustomTextBox _txtDefaultPort;
        private CustomTextBox _txtDefaultPassword;
        private CheckBox _chkAutoStart;
        private CheckBox _chkSaveLogs;
        private CheckBox _chkDarkTheme;
        private CustomButton _btnSave;
        private CustomButton _btnReset;
        private RichTextBox _txtAbout;

        public SettingsTab()
        {
            InitializeComponent();
            LoadSettings();
        }

        public void Initialize(MainForm mainForm)
        {
            _mainForm = mainForm;
        }

        private void InitializeComponent()
        {
            this.BackColor = DarkTheme.BackColor;
            this.Padding = new Padding(20);

            // ===== TITLE =====
            var title = new Label
            {
                Text = "⚙️ PARAMÈTRES",
                Font = new Font("Segoe UI", 18, FontStyle.Bold),
                ForeColor = DarkTheme.TextColor,
                BackColor = Color.Transparent,
                Dock = DockStyle.Top,
                Height = 50,
                TextAlign = ContentAlignment.MiddleLeft
            };
            this.Controls.Add(title);

            // ===== MAIN PANEL =====
            var mainPanel = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 5,
                BackColor = Color.Transparent,
                Padding = new Padding(10)
            };

            mainPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30));
            mainPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70));

            // Port
            mainPanel.Controls.Add(CreateLabel("Port par defaut:"), 0, 0);
            _txtDefaultPort = new CustomTextBox
            {
                Text = Constants.DefaultPort.ToString(),
                Width = 150,
                Anchor = AnchorStyles.Left
            };
            mainPanel.Controls.Add(_txtDefaultPort, 1, 0);

            // Password
            mainPanel.Controls.Add(CreateLabel("Mot de passe par defaut:"), 0, 1);
            _txtDefaultPassword = new CustomTextBox
            {
                Text = Constants.DefaultPassword,
                Width = 200,
                Anchor = AnchorStyles.Left
            };
            mainPanel.Controls.Add(_txtDefaultPassword, 1, 1);

            // Options
            mainPanel.Controls.Add(CreateLabel("Options:"), 0, 2);
            var optionsPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent
            };

            _chkAutoStart = new CheckBox
            {
                Text = "Demarrer le serveur au lancement",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Dock = DockStyle.Top,
                Height = 30
            };

            _chkSaveLogs = new CheckBox
            {
                Text = "Sauvegarder les logs automatiquement",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Dock = DockStyle.Top,
                Height = 30
            };

            _chkDarkTheme = new CheckBox
            {
                Text = "Theme sombre (toujours active)",
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                Dock = DockStyle.Top,
                Height = 30,
                Checked = true,
                Enabled = false
            };

            optionsPanel.Controls.Add(_chkDarkTheme);
            optionsPanel.Controls.Add(_chkSaveLogs);
            optionsPanel.Controls.Add(_chkAutoStart);
            mainPanel.Controls.Add(optionsPanel, 1, 2);

            // Buttons
            mainPanel.Controls.Add(new Panel(), 0, 3);
            var btnPanel = new Panel
            {
                Dock = DockStyle.Fill,
                BackColor = Color.Transparent
            };

            _btnSave = new CustomButton
            {
                Text = "Sauvegarder",
                Width = 150,
                Height = 35,
                BackColor = DarkTheme.HighlightColor,
                ForeColor = Color.Black,
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };
            _btnSave.Click += BtnSave_Click;

            _btnReset = new CustomButton
            {
                Text = "Reinitialiser",
                Width = 150,
                Height = 35,
                BackColor = DarkTheme.ControlColor,
                ForeColor = DarkTheme.TextColor,
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                Location = new Point(160, 0)
            };
            _btnReset.Click += BtnReset_Click;

            btnPanel.Controls.Add(_btnSave);
            btnPanel.Controls.Add(_btnReset);
            mainPanel.Controls.Add(btnPanel, 1, 3);

            // About
            mainPanel.Controls.Add(CreateLabel("A propos:"), 0, 4);
            _txtAbout = new RichTextBox
            {
                Dock = DockStyle.Fill,
                BackColor = DarkTheme.BackColor,
                ForeColor = DarkTheme.SecondaryText,
                Font = new Font("Segoe UI", 10),
                ReadOnly = true,
                BorderStyle = BorderStyle.None,
                Text = $@"Ghost Anomalie v{Constants.Version}

{Constants.Author}

Securise - Furtif - Puissant

Utilisation EDUCATIF uniquement
Ne pas utiliser sur des machines sans consentement

Documentation: README.md
"
            };
            mainPanel.Controls.Add(_txtAbout, 1, 4);

            this.Controls.Add(mainPanel);
        }

        private Label CreateLabel(string text)
        {
            return new Label
            {
                Text = text,
                ForeColor = DarkTheme.SecondaryText,
                BackColor = Color.Transparent,
                AutoSize = true,
                TextAlign = ContentAlignment.MiddleLeft
            };
        }

        private void LoadSettings()
        {
            try
            {
                var config = ConfigManager.Load();
                _txtDefaultPort.Text = config.Port.ToString();
                _txtDefaultPassword.Text = config.Password;
                _chkAutoStart.Checked = config.AutoStart;
                _chkSaveLogs.Checked = config.SaveLogs;
            }
            catch { }
        }

        private void BtnSave_Click(object? sender, EventArgs e)
        {
            try
            {
                var config = new ConfigManager.Config
                {
                    Port = int.Parse(_txtDefaultPort.Text),
                    Password = _txtDefaultPassword.Text,
                    AutoStart = _chkAutoStart.Checked,
                    SaveLogs = _chkSaveLogs.Checked
                };

                ConfigManager.Save(config);
                MessageBox.Show("Parametres sauvegardes !", "Succes",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur: {ex.Message}", "Erreur",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnReset_Click(object? sender, EventArgs e)
        {
            _txtDefaultPort.Text = Constants.DefaultPort.ToString();
            _txtDefaultPassword.Text = Constants.DefaultPassword;
            _chkAutoStart.Checked = false;
            _chkSaveLogs.Checked = true;
            MessageBox.Show("Parametres reinitialises !", "Succes",
                MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
