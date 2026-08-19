namespace GhostAnomalie.Common.Packets
{
    public class CommandPacket : PacketBase
    {
        public string Command { get; set; } = "";
        public string[]? Args { get; set; }
        public string? ClientId { get; set; }

        public CommandPacket()
        {
            Type = PacketType.Command;
        }

        public CommandPacket(string command, string[]? args = null, string? clientId = null) : this()
        {
            Command = command;
            Args = args;
            ClientId = clientId;
        }

        public CommandPacket(PacketType type, string command, string[]? args = null, string? clientId = null)
        {
            Type = type;
            Command = command;
            Args = args;
            ClientId = clientId;
        }
    }
}
