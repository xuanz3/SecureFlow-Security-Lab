using System.Text;

namespace SecureFlow.Web.Security;

public sealed record FileScanResult(
    bool IsClean,
    string? Error,
    string? DetectedContentType);

public interface IFileSecurityScanner
{
    Task<FileScanResult> ScanAsync(
        Stream content,
        string extension,
        CancellationToken cancellationToken = default);
}

public sealed class FileSecurityScanner : IFileSecurityScanner
{
    private static readonly byte[] PdfSignature = "%PDF-"u8.ToArray();
    private static readonly byte[] PngSignature =
        [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
    private static readonly byte[] JpegSignature = [0xFF, 0xD8, 0xFF];
    private static readonly byte[] BlockedTestMarker =
        Encoding.UTF8.GetBytes("SECUREFLOW_TEST_BLOCK");
    private static readonly UTF8Encoding StrictUtf8 = new(false, true);

    public async Task<FileScanResult> ScanAsync(
        Stream content,
        string extension,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(content);

        if (!content.CanRead)
        {
            return new(false, "The uploaded content cannot be read.", null);
        }

        if (content.CanSeek)
        {
            content.Position = 0;
        }

        await using var copy = new MemoryStream();
        await content.CopyToAsync(copy, cancellationToken);
        var bytes = copy.ToArray();

        if (bytes.Length == 0)
        {
            return new(false, "The uploaded file is empty.", null);
        }

        if (bytes.AsSpan().IndexOf(BlockedTestMarker) >= 0)
        {
            return new(
                false,
                "The file was rejected by the local security scan.",
                null);
        }

        return extension.ToLowerInvariant() switch
        {
            ".pdf" when StartsWith(bytes, PdfSignature) =>
                new(true, null, "application/pdf"),
            ".png" when StartsWith(bytes, PngSignature) =>
                new(true, null, "image/png"),
            ".jpg" or ".jpeg" when StartsWith(bytes, JpegSignature) =>
                new(true, null, "image/jpeg"),
            ".txt" when IsSafeUtf8Text(bytes) =>
                new(true, null, "text/plain"),
            ".pdf" =>
                new(false, "The file signature does not match a PDF.", null),
            ".png" =>
                new(false, "The file signature does not match a PNG image.", null),
            ".jpg" or ".jpeg" =>
                new(false, "The file signature does not match a JPEG image.", null),
            ".txt" =>
                new(false, "The text file is not valid UTF-8 text.", null),
            _ =>
                new(false, "The file type is not supported by the security scan.", null)
        };
    }

    private static bool StartsWith(byte[] source, byte[] signature) =>
        source.AsSpan().StartsWith(signature);

    private static bool IsSafeUtf8Text(byte[] bytes)
    {
        if (bytes.AsSpan().IndexOf((byte)0) >= 0)
        {
            return false;
        }

        try
        {
            _ = StrictUtf8.GetString(bytes);
            return true;
        }
        catch (DecoderFallbackException)
        {
            return false;
        }
    }
}
