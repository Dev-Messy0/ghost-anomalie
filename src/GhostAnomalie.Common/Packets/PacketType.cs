namespace GhostAnomalie.Common.Packets
{
    public enum PacketType
    {
        // Connexion
        Handshake,
        Authentification,
        AuthentificationResponse,
        Disconnect,

        // Commandes
        Command,
        CommandResult,

        // Fichiers
        FileDownload,
        FileUpload,
        FileList,
        FileDelete,
        FileExecute,

        // Système
        SystemInfo,
        ProcessList,
        ProcessKill,

        // Surveillance
        Screenshot,
        KeyloggerStart,
        KeyloggerStop,
        KeyloggerGet,
        Webcam,
        Microphone,

        // Réseau
        NetworkScan,
        PortScan,
        WifiPasswords,

        // Client
        ClientInfo,
        ClientPing,
        ClientUpdate,
        ClientStatus
    }
}
