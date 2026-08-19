using GhostAnomalie.Server.Forms;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

namespace GhostAnomalie.Server
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            var form = new MainForm();

            // === ICONE INTEGREE DIRECTEMENT DANS LE CODE ===
            form.Icon = GetEmbeddedIcon();

            Application.Run(form);
        }

        /// <summary>
        /// Crée une icône directement en mémoire (sans fichier externe)
        /// </summary>
        private static Icon GetEmbeddedIcon()
        {
            try
            {
                // Créer l'image en mémoire
                using (var bitmap = CreateGhostIcon())
                {
                    // Convertir en icône
                    return Icon.FromHandle(bitmap.GetHicon());
                }
            }
            catch
            {
                // En cas d'erreur, retourner une icône par défaut
                return SystemIcons.Application;
            }
        }

        /// <summary>
        /// Crée l'image du fantôme Ghost Anomalie
        /// </summary>
        private static Bitmap CreateGhostIcon()
        {
            int size = 256;
            var bitmap = new Bitmap(size, size, PixelFormat.Format32bppArgb);

            using (var g = Graphics.FromImage(bitmap))
            {
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                g.Clear(Color.Transparent);

                // 1. Cercle de fond (vert néon)
                var circleRect = new Rectangle(20, 20, size - 40, size - 40);
                using (var brush = new SolidBrush(Color.FromArgb(200, 0, 255, 136)))
                {
                    g.FillEllipse(brush, circleRect);
                }

                // 2. Bordure néon
                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 6))
                {
                    g.DrawEllipse(pen, circleRect);
                }

                // 3. Effet de lumière
                using (var brush = new SolidBrush(Color.FromArgb(60, 0, 255, 136)))
                {
                    g.FillEllipse(brush, 120, 100, 40, 80);
                }

                // 4. Corps du fantôme
                var ghostPath = new System.Drawing.Drawing2D.GraphicsPath();

                // Tête
                ghostPath.AddEllipse(60, 60, 136, 120);

                // Corps
                ghostPath.AddRectangle(new Rectangle(60, 140, 136, 60));

                // Bas du fantôme (vagues)
                ghostPath.AddLine(60, 200, 80, 210);
                ghostPath.AddLine(80, 210, 100, 200);
                ghostPath.AddLine(100, 200, 120, 210);
                ghostPath.AddLine(120, 210, 140, 200);
                ghostPath.AddLine(140, 200, 160, 210);
                ghostPath.AddLine(160, 210, 180, 200);
                ghostPath.AddLine(180, 200, 196, 210);

                // Remplir le fantôme
                using (var brush = new SolidBrush(Color.FromArgb(230, 255, 255, 255)))
                {
                    g.FillPath(brush, ghostPath);
                }

                // Contour du fantôme
                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 3))
                {
                    g.DrawPath(pen, ghostPath);
                }

                // 5. Yeux
                // Œil gauche
                g.FillEllipse(new SolidBrush(Color.FromArgb(0, 255, 136)), 85, 100, 25, 35);
                g.FillEllipse(new SolidBrush(Color.Black), 92, 110, 12, 18);

                // Œil droit
                g.FillEllipse(new SolidBrush(Color.FromArgb(0, 255, 136)), 145, 100, 25, 35);
                g.FillEllipse(new SolidBrush(Color.Black), 152, 110, 12, 18);

                // 6. Bouche
                using (var pen = new Pen(Color.FromArgb(0, 255, 136), 4))
                {
                    g.DrawArc(pen, 110, 145, 45, 25, 0, 180);
                }

                // 7. Reflet
                using (var brush = new SolidBrush(Color.FromArgb(80, 255, 255, 255)))
                {
                    g.FillEllipse(brush, 95, 70, 20, 20);
                    g.FillEllipse(brush, 155, 70, 15, 15);
                }

                // 8. Texte "GA"
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

                // 9. Anneau extérieur
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
