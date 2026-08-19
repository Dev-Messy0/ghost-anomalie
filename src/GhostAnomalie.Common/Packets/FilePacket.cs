namespace GhostAnomalie.Common.Packets
{
    public class FilePacket : PacketBase
    {
        public string FileName { get; set; } = "";
        public string Path { get; set; } = "";
        public byte[]? Content { get; set; }
        public long Size { get; set; }
        public string? FileType { get; set; }
        public bool IsDirectory { get; set; }

        public FilePacket()
        {
            Type = PacketType.FileDownload;
        }

        public FilePacket(string path, byte[]? content = null, bool isDirectory = false) : this()
        {
            Path = path;
            FileName = System.IO.Path.GetFileName(path);
            Content = content;
            Size = content?.Length ?? 0;
            IsDirectory = isDirectory;
        }

        public FilePacket(PacketType type, string path, byte[]? content = null, bool isDirectory = false)
        {
            Type = type;
            Path = path;
            FileName = System.IO.Path.GetFileName(path);
            Content = content;
            Size = content?.Length ?? 0;
            IsDirectory = isDirectory;
        }
    }
}
