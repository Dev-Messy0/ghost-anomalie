using System.Drawing;
using System.Windows.Forms;

namespace GhostAnomalie.Server.Controls
{
    public static class DarkTheme
    {
        // === COULEURS PRINCIPALES ===
        public static Color BackColor = Color.FromArgb(5, 5, 15);
        public static Color PanelColor = Color.FromArgb(10, 10, 26);
        public static Color ControlColor = Color.FromArgb(26, 26, 46);
        public static Color TextColor = Color.FromArgb(0, 255, 136);
        public static Color HighlightColor = Color.FromArgb(0, 200, 100);
        public static Color ErrorColor = Color.FromArgb(255, 50, 50);
        public static Color WarningColor = Color.FromArgb(255, 170, 0);
        public static Color SecondaryText = Color.FromArgb(170, 170, 170);
        public static Color BorderColor = Color.FromArgb(40, 40, 60);

        // === FONTS ===
        public static Font DefaultFont = new Font("Segoe UI", 9);
        public static Font TitleFont = new Font("Segoe UI", 12, FontStyle.Bold);
        public static Font MonospaceFont = new Font("Consolas", 9);
    }

    // ============================================================
    // BOUTON PERSONNALISÉ
    // ============================================================
    public class CustomButton : Button
    {
        public CustomButton()
        {
            this.FlatStyle = FlatStyle.Flat;
            this.FlatAppearance.BorderSize = 0;
            this.Cursor = Cursors.Hand;
            this.BackColor = DarkTheme.ControlColor;
            this.ForeColor = DarkTheme.TextColor;
            this.Font = DarkTheme.DefaultFont;
        }

        protected override void OnMouseEnter(EventArgs e)
        {
            base.OnMouseEnter(e);
            this.BackColor = DarkTheme.HighlightColor;
        }

        protected override void OnMouseLeave(EventArgs e)
        {
            base.OnMouseLeave(e);
            this.BackColor = DarkTheme.ControlColor;
        }

        protected override void OnPaint(PaintEventArgs pevent)
        {
            base.OnPaint(pevent);
            // Bordure subtile
            ControlPaint.DrawBorder(pevent.Graphics, this.ClientRectangle,
                DarkTheme.BorderColor, 1, ButtonBorderStyle.Solid,
                DarkTheme.BorderColor, 1, ButtonBorderStyle.Solid,
                DarkTheme.BorderColor, 1, ButtonBorderStyle.Solid,
                DarkTheme.BorderColor, 1, ButtonBorderStyle.Solid);
        }
    }

    // ============================================================
    // TEXTBOX PERSONNALISÉ
    // ============================================================
    public class CustomTextBox : TextBox
    {
        public CustomTextBox()
        {
            this.BackColor = DarkTheme.ControlColor;
            this.ForeColor = DarkTheme.TextColor;
            this.BorderStyle = BorderStyle.FixedSingle;
            this.Font = DarkTheme.DefaultFont;
        }

        protected override void OnEnter(EventArgs e)
        {
            base.OnEnter(e);
            this.BackColor = DarkTheme.HighlightColor;
            this.ForeColor = Color.Black;
        }

        protected override void OnLeave(EventArgs e)
        {
            base.OnLeave(e);
            this.BackColor = DarkTheme.ControlColor;
            this.ForeColor = DarkTheme.TextColor;
        }
    }

    // ============================================================
    // LISTVIEW PERSONNALISÉ
    // ============================================================
    public class CustomListView : ListView
    {
        public CustomListView()
        {
            this.BackColor = DarkTheme.BackColor;
            this.ForeColor = DarkTheme.TextColor;
            this.BorderStyle = BorderStyle.None;
            this.View = View.Details;
            this.FullRowSelect = true;
            this.GridLines = false;
            this.OwnerDraw = true;
            this.DrawItem += CustomListView_DrawItem;
            this.DrawColumnHeader += CustomListView_DrawColumnHeader;
            this.DrawSubItem += CustomListView_DrawSubItem;
        }

        private void CustomListView_DrawItem(object? sender, DrawListViewItemEventArgs e)
        {
            e.DrawBackground();
            e.DrawDefault = false;

            if (e.Item.Selected)
            {
                e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(26, 26, 46)), e.Bounds);
            }
            else if (e.ItemIndex % 2 == 0)
            {
                e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(10, 10, 20)), e.Bounds);
            }
            else
            {
                e.Graphics.FillRectangle(new SolidBrush(DarkTheme.BackColor), e.Bounds);
            }

            e.Graphics.DrawString(e.Item.Text, e.Item.Font, new SolidBrush(DarkTheme.TextColor),
                e.Bounds.X + 2, e.Bounds.Y + 2);
        }

        private void CustomListView_DrawColumnHeader(object? sender, DrawListViewColumnHeaderEventArgs e)
        {
            e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(20, 20, 40)), e.Bounds);
            e.Graphics.DrawString(e.Header.Text, e.Font, new SolidBrush(DarkTheme.TextColor),
                e.Bounds.X + 2, e.Bounds.Y + 2);
        }

        private void CustomListView_DrawSubItem(object? sender, DrawListViewSubItemEventArgs e)
        {
            if (e.Item.Selected)
            {
                e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(26, 26, 46)), e.Bounds);
            }
            else if (e.ItemIndex % 2 == 0)
            {
                e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(10, 10, 20)), e.Bounds);
            }
            else
            {
                e.Graphics.FillRectangle(new SolidBrush(DarkTheme.BackColor), e.Bounds);
            }

            e.Graphics.DrawString(e.SubItem.Text, e.Item.Font, new SolidBrush(DarkTheme.TextColor),
                e.Bounds.X + 2, e.Bounds.Y + 2);
        }
    }

    // ============================================================
    // TREEVIEW PERSONNALISÉ
    // ============================================================
    public class CustomTreeView : TreeView
    {
        public CustomTreeView()
        {
            this.BackColor = DarkTheme.BackColor;
            this.ForeColor = DarkTheme.TextColor;
            this.BorderStyle = BorderStyle.None;
            this.Font = DarkTheme.DefaultFont;
            this.LineColor = DarkTheme.BorderColor;
            this.HideSelection = false;
        }

        protected override void OnDrawNode(DrawTreeNodeEventArgs e)
        {
            if (e.Node.IsSelected)
            {
                e.Graphics.FillRectangle(new SolidBrush(Color.FromArgb(26, 26, 46)), e.Bounds);
            }
            else if (e.Node.IsVisible)
            {
                e.Graphics.FillRectangle(new SolidBrush(DarkTheme.BackColor), e.Bounds);
            }

            e.Graphics.DrawString(e.Node.Text, e.Node.TreeView.Font, new SolidBrush(DarkTheme.TextColor),
                e.Bounds.X + 2, e.Bounds.Y + 2);
        }
    }
}
