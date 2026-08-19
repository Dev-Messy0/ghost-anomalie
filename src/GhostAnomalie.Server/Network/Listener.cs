using GhostAnomalie.Common.Packets;
using GhostAnomalie.Common.Utils;
using System.Net;
using System.Net.Sockets;

namespace GhostAnomalie.Server.Network
{
    public class Listener
    {
        private TcpListener? _listener;
        private bool _isRunning;
        private MainForm _mainForm;
        private string _password = "";

        public Listener(MainForm mainForm)
        {
            _mainForm = mainForm;
        }

        public async Task Start(int port, string password)
        {
            _password = password;
            _isRunning = true;

            try
            {
                _listener = new TcpListener(IPAddress.Any, port);
                _listener.Start();
                _mainForm.Log($"📡 En écoute sur le port {port}");

                while (_isRunning)
                {
                    try
                    {
                        var client = await _listener.AcceptTcpClientAsync();
                        _ = Task.Run(() => HandleClient(client));
                    }
                    catch (Exception ex)
                    {
                        if (_isRunning)
                            _mainForm.Log($"❌ Erreur acceptation: {ex.Message}");
                    }
                }
            }
            catch (Exception ex)
            {
                _mainForm.Log($"❌ Erreur démarrage: {ex.Message}");
                throw;
            }
        }

        public void Stop()
        {
            _isRunning = false;
            _listener?.Stop();
        }

        private async Task HandleClient(TcpClient tcpClient)
        {
            var clientHandler = new ClientHandler(tcpClient, _mainForm, _password);
            await clientHandler.Handle();
        }
    }
}
