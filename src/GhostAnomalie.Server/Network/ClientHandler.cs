using GhostAnomalie.Common.Packets;
using GhostAnomalie.Common.Utils;
using System.Net.Sockets;
using System.Text.Json;

namespace GhostAnomalie.Server.Network
{
    public class ClientHandler
    {
        private TcpClient _tcpClient;
        private NetworkStream? _stream;
        private MainForm _mainForm;
        private string _password;
        private bool _isAuthenticated = false;
        private bool _isRunning = true;

        public string ClientId { get; private set; } = "";
        public string IpAddress { get; private set; } = "";

        public ClientHandler(TcpClient tcpClient, MainForm mainForm, string password)
        {
            _tcpClient = tcpClient;
            _mainForm = mainForm;
            _password = password;

            var endpoint = tcpClient.Client.RemoteEndPoint as IPEndPoint;
            IpAddress = endpoint?.Address?.ToString() ?? "Unknown";
        }

        public async Task Handle()
        {
            try
            {
                _stream = _tcpClient.GetStream();
                var buffer = new byte[Constants.BufferSize];

                while (_isRunning && _tcpClient.Connected)
                {
                    var read = await _stream.ReadAsync(buffer, 0, buffer.Length);
                    if (read == 0) break;

                    var json = System.Text.Encoding.UTF8.GetString(buffer, 0, read);
                    var packet = PacketBase.FromString(json);

                    if (packet != null)
                    {
                        await ProcessPacket(packet);
                    }
                }
            }
            catch (Exception ex)
            {
                _mainForm.Log($"❌ Erreur client {ClientId}: {ex.Message}");
            }
            finally
            {
                Disconnect();
            }
        }

        private async Task ProcessPacket(PacketBase packet)
        {
            switch (packet.Type)
            {
                case PacketType.Authentification:
                    await ProcessAuth(packet as CommandPacket);
                    break;

                case PacketType.Command:
                    await ProcessCommand(packet as CommandPacket);
                    break;

                case PacketType.Disconnect:
                    _isRunning = false;
                    break;

                default:
                    _mainForm.Log($"⚠️ Type de paquet inconnu: {packet.Type}");
                    break;
            }
        }

        private async Task ProcessAuth(CommandPacket? packet)
        {
            if (packet == null) return;

            ClientId = packet.ClientId ?? "Unknown";

            // Vérifier le mot de passe
            var isAuthenticated = packet.Command == _password;

            var response = new ResultPacket
            {
                CommandId = packet.Id,
                Success = isAuthenticated,
                Data = isAuthenticated ? "Authentification réussie" : "Mot de passe incorrect"
            };

            await SendPacket(response);

            if (isAuthenticated)
            {
                _isAuthenticated = true;
                _mainForm.AddClient(this);
            }
            else
            {
                _isRunning = false;
                _tcpClient.Close();
            }
        }

        private async Task ProcessCommand(CommandPacket? packet)
        {
            if (!_isAuthenticated || packet == null) return;

            // Rediriger vers le MainForm pour traitement
            _mainForm.Log($"📥 Commande reçue de {ClientId}: {packet.Command}");

            // Ici on peut ajouter un système de réponse automatique
            // ou laisser le MainForm gérer l'envoi de la réponse
        }

        public async Task SendCommand(CommandPacket packet)
        {
            await SendPacket(packet);
        }

        private async Task SendPacket(PacketBase packet)
        {
            try
            {
                if (_stream == null || !_tcpClient.Connected) return;

                var json = packet.Serialize();
                var bytes = System.Text.Encoding.UTF8.GetBytes(json);
                await _stream.WriteAsync(bytes, 0, bytes.Length);
            }
            catch (Exception ex)
            {
                _mainForm.Log($"❌ Erreur envoi à {ClientId}: {ex.Message}");
            }
        }

        public void Disconnect()
        {
            _isRunning = false;
            _isAuthenticated = false;

            try
            {
                _stream?.Close();
                _tcpClient?.Close();
            }
            catch { }

            if (!string.IsNullOrEmpty(ClientId))
            {
                _mainForm.RemoveClient(ClientId);
            }
        }
    }
}
