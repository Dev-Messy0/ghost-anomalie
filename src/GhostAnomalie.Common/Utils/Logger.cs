namespace GhostAnomalie.Common.Utils
{
    public class Logger
    {
        private static readonly object _lock = new object();
        private static string _logFile = $"logs/ghost_{DateTime.Now:yyyyMMdd}.log";

        public static void Log(string message)
        {
            try
            {
                Directory.CreateDirectory("logs");
                lock (_lock)
                {
                    File.AppendAllText(_logFile, $"[{DateTime.Now:HH:mm:ss}] {message}\n");
                }
            }
            catch { }
        }

        public static void Log(string message, Exception ex)
        {
            Log($"{message}: {ex.Message}\n{ex.StackTrace}");
        }

        public static void Info(string message)
        {
            Log($"[INFO] {message}");
        }

        public static void Error(string message)
        {
            Log($"[ERROR] {message}");
        }

        public static void Warning(string message)
        {
            Log($"[WARNING] {message}");
        }

        public static void Success(string message)
        {
            Log($"[SUCCESS] {message}");
        }
    }
}
