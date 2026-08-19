using System.Security.Cryptography;
using System.Text;

namespace GhostAnomalie.Common.Utils
{
    public static class Encryption
    {
        private static readonly byte[] Salt = Encoding.UTF8.GetBytes("GhostAnomalieSalt2024");
        private static readonly byte[] IV = Encoding.UTF8.GetBytes("GhostAnomalieIV2024");

        public static string Encrypt(string plainText, string password)
        {
            using var aes = Aes.Create();
            using var deriveBytes = new Rfc2898DeriveBytes(password, Salt, 10000, HashAlgorithmName.SHA256);
            aes.Key = deriveBytes.GetBytes(32);
            aes.IV = IV;

            using var encryptor = aes.CreateEncryptor();
            var plainBytes = Encoding.UTF8.GetBytes(plainText);
            var encrypted = encryptor.TransformFinalBlock(plainBytes, 0, plainBytes.Length);

            return Convert.ToBase64String(encrypted);
        }

        public static string Decrypt(string cipherText, string password)
        {
            try
            {
                using var aes = Aes.Create();
                using var deriveBytes = new Rfc2898DeriveBytes(password, Salt, 10000, HashAlgorithmName.SHA256);
                aes.Key = deriveBytes.GetBytes(32);
                aes.IV = IV;

                using var decryptor = aes.CreateDecryptor();
                var cipherBytes = Convert.FromBase64String(cipherText);
                var decrypted = decryptor.TransformFinalBlock(cipherBytes, 0, cipherBytes.Length);

                return Encoding.UTF8.GetString(decrypted);
            }
            catch
            {
                return string.Empty;
            }
        }
    }
}
