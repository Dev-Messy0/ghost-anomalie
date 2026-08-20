using GhostAnomalie.Server.Forms;
using System.Diagnostics;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Principal;

namespace GhostAnomalie.Server
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            // === 1. DEMANDER LES DROITS ADMIN ===
            if (!IsAdministrator())
            {
                RestartAsAdmin();
                return;
            }

            // === 2. FORCER LA COMPATIBILITÉ WINDOWS ===
            SetCompatibilityFlags();

            // === 3. LANCER L'APPLICATION ===
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            var form = new MainForm();
            form.Icon = GetEmbeddedIcon();
            Application.Run(form);
        }

        // ============================================================
        // DEMANDER LES DROITS ADMIN
        // ============================================================

        private static bool IsAdministrator()
        {
            try
            {
                var identity = WindowsIdentity.GetCurrent();
                var principal = new WindowsPrincipal(identity);
                return principal.IsInRole(WindowsBuiltInRole.Administrator);
            }
            catch
            {
                return false;
            }
        }

        private static void RestartAsAdmin()
        {
            try
            {
                var exePath = Assembly.GetExecutingAssembly().Location;
                var startInfo = new ProcessStartInfo(exePath)
                {
                    UseShellExecute = true,
                    Verb = "runas"
                };
                Process.Start(startInfo);
            }
            catch
            {
                // Si l'utilisateur refuse, essayer quand même
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                Application.Run(new MainForm());
            }
        }

        // ============================================================
        // COMPATIBILITÉ WINDOWS (SANS FICHIER EXTERNE)
        // ============================================================

        private static void SetCompatibilityFlags()
        {
            try
            {
                // Désactiver le DPI scaling
                SetProcessDPIAware();

                // Forcer la compatibilité avec toutes les versions de Windows
                var currentOS = Environment.OSVersion.Version;
                if (currentOS.Major >= 10)
                {
                    // Windows 10/11
                }
            }
            catch { }
        }

        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        // ============================================================
        // ICÔNE INTÉGRÉE
        // ============================================================

        private static Icon GetEmbeddedIcon()
        {
            try
            {
                using (var bitmap = CreateGhostIcon())
                {
                    return Icon.FromHandle(bitmap.GetHicon());
                }
            }
            catch
            {
                return SystemIcons.Application;
            }
        }

        private static Bitmap CreateGhostIcon()
        {
            int size = 256;
            var bitmap = new Bitmap(size, size, System.Drawing.Imaging.PixelFormat.Format32bppArgb);

            using (var g = Graphics.FromImage(bitmap))
            {
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                g.Clear(Color.Transparent);

                // Cercle néon
                var circleRect = new Rectangle(20, 20, size - 40, size - 40);
                using (var brush = new SolidBrush(Color.FromArgb(200, 0, 255, 136)))
                {
                    g.FillEllipse(brush, circleRect);
                }

                // Bordure
                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 6))
                {
                    g.DrawEllipse(pen, circleRect);
                }

                // Fantôme
                var ghostPath = new System.Drawing.Drawing2D.GraphicsPath();
                ghostPath.AddEllipse(60, 60, 136, 120);
                ghostPath.AddRectangle(new Rectangle(60, 140, 136, 60));
                ghostPath.AddLine(60, 200, 80, 210);
                ghostPath.AddLine(80, 210, 100, 200);
                ghostPath.AddLine(100, 200, 120, 210);
                ghostPath.AddLine(120, 210, 140, 200);
                ghostPath.AddLine(140, 200, 160, 210);
                ghostPath.AddLine(160, 210, 180, 200);
                ghostPath.AddLine(180, 200, 196, 210);

                using (var brush = new SolidBrush(Color.FromArgb(230, 255, 255, 255)))
                {
                    g.FillPath(brush, ghostPath);
                }

                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 3))
                {
                    g.DrawPath(pen, ghostPath);
                }

                // Yeux
                g.FillEllipse(new SolidBrush(Color.FromArgb(0, 255, 136)), 85, 100, 25, 35);
                g.FillEllipse(new SolidBrush(Color.Black), 92, 110, 12, 18);
                g.FillEllipse(new SolidBrush(Color.FromArgb(0, 255, 136)), 145, 100, 25, 35);
                g.FillEllipse(new SolidBrush(Color.Black), 152, 110, 12, 18);

                // Bouche
                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 4))
                {
                    g.DrawArc(pen, 110, 145, 45, 25, 0, 180);
                }

                // Reflet
                using (var brush = new SolidBrush(Color.FromArgb(80, 255, 255, 255)))
                {
                    g.FillEllipse(brush, 95, 70, 20, 20);
                    g.FillEllipse(brush, 155, 70, 15, 15);
                }

                // Texte "GA"
                using (var font = new Font("Arial Black", 28, FontStyle.Bold))
                using (var brush = new SolidBrush(Color.FromArgb(200, 0, 255, 136)))
                {
                    var format = new StringFormat
                    {
                        Alignment = StringAlignment.Center,
                        LineAlignment = StringAlignment.Center
                    };
                    g.DrawString("GA", font, brush, new Rectangle(0, 0, size, size), format);
                }

                // Anneau extérieur
                using (var pen = new Pen(Color.FromArgb(100, 0, 255, 136), 2))
                {
                    var outerRect = new Rectangle(10, 10, size - 20, size - 20);
                    g.DrawEllipse(pen, outerRect);
                }
            }

            return bitmap;
        }
    }
}
