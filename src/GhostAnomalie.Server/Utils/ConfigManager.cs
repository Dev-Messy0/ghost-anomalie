using System.Text.Json;

namespace GhostAnomalie.Server.Utils
{
    public static class ConfigManager
    {
        private static readonly string ConfigFile = "ghost_config.json";

        public class Config
        {
            public int Port { get; set; } = 4444;
            public string Password { get; set; } = "admin123";
            public bool AutoStart { get; set; } = false;
            public bool SaveLogs { get; set; } = true;
            public string Theme { get; set; } = "Dark";
        }

        public static Config Load()
        {
            try
            {
                if (File.Exists(ConfigFile))
                {
                    var json = File.ReadAllText(ConfigFile);
                    return JsonSerializer.Deserialize<Config>(json) ?? new Config();
                }
            }
            catch { }
            return new Config();
        }

        public static void Save(Config config)
        {
            try
            {
                var json = JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(ConfigFile, json);
            }
            catch { }
        }
    }
}
