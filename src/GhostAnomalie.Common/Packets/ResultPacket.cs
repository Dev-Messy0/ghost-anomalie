namespace GhostAnomalie.Common.Packets
{
    public class ResultPacket : PacketBase
    {
        public string CommandId { get; set; } = "";
        public bool Success { get; set; }
        public string Data { get; set; } = "";
        public string? Error { get; set; }

        public ResultPacket()
        {
            Type = PacketType.CommandResult;
        }

        public ResultPacket(string commandId, bool success, string data, string? error = null) : this()
        {
            CommandId = commandId;
            Success = success;
            Data = data;
            Error = error;
        }
    }
}
