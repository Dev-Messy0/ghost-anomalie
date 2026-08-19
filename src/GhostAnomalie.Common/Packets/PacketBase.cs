using System.Text.Json;

namespace GhostAnomalie.Common.Packets
{
    public abstract class PacketBase
    {
        public PacketType Type { get; set; }
        public string Id { get; set; } = Guid.NewGuid().ToString();
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;

        public virtual string Serialize()
        {
            return JsonSerializer.Serialize(this);
        }

        public static T Deserialize<T>(string json) where T : PacketBase
        {
            return JsonSerializer.Deserialize<T>(json);
        }

        public byte[] ToBytes()
        {
            return Encoding.UTF8.GetBytes(Serialize());
        }

        public static PacketBase FromBytes(byte[] bytes)
        {
            try
            {
                var json = Encoding.UTF8.GetString(bytes);
                var packet = JsonSerializer.Deserialize<PacketBase>(json);
                return packet;
            }
            catch
            {
                return null;
            }
        }

        public static PacketBase FromString(string json)
        {
            try
            {
                return JsonSerializer.Deserialize<PacketBase>(json);
            }
            catch
            {
                return null;
            }
        }
    }
}
