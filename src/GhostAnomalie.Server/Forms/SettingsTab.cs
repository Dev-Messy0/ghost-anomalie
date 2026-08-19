using GhostAnomalie.Common.Utils;
using GhostAnomalie.Server.Controls;
using GhostAnomalie.Server.Utils;  // ← AJOUTÉ

namespace GhostAnomalie.Server.Forms
{
    public partial class SettingsTab : UserControl
    {
        private MainForm _mainForm;

        // ... (le reste du code)

        private void LoadSettings()
        {
            try
            {
                var config = ConfigManager.Load();  // ← MAINtenant trouvé
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
                MessageBox.Show("✅ Paramètres sauvegardés !", "Succès",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"❌ Erreur: {ex.Message}", "Erreur",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
