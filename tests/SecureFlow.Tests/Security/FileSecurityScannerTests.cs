using System.Text;
using SecureFlow.Web.Security;

namespace SecureFlow.Tests.Security;

public sealed class FileSecurityScannerTests
{
    private readonly FileSecurityScanner scanner = new();

    [Fact]
    public async Task AcceptsPdfWithPdfSignature()
    {
        var result = await ScanAsync(
            ".pdf",
            "%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF\n"u8.ToArray());

        Assert.True(result.IsClean);
        Assert.Equal("application/pdf", result.DetectedContentType);
    }

    [Fact]
    public async Task RejectsPdfWithHtmlContent()
    {
        var result = await ScanAsync(
            ".pdf",
            "<html>not a PDF</html>"u8.ToArray());

        Assert.False(result.IsClean);
        Assert.Contains("signature", result.Error, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public async Task AcceptsPngSignature()
    {
        var bytes = new byte[]
        {
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00
        };

        var result = await ScanAsync(".png", bytes);

        Assert.True(result.IsClean);
        Assert.Equal("image/png", result.DetectedContentType);
    }

    [Fact]
    public async Task AcceptsJpegSignature()
    {
        var result = await ScanAsync(
            ".jpg",
            [0xFF, 0xD8, 0xFF, 0xE0, 0x00]);

        Assert.True(result.IsClean);
        Assert.Equal("image/jpeg", result.DetectedContentType);
    }

    [Fact]
    public async Task AcceptsValidUtf8Text()
    {
        var result = await ScanAsync(
            ".txt",
            Encoding.UTF8.GetBytes("harmless portfolio text"));

        Assert.True(result.IsClean);
        Assert.Equal("text/plain", result.DetectedContentType);
    }

    [Fact]
    public async Task RejectsTextContainingNullBytes()
    {
        var result = await ScanAsync(".txt", [0x41, 0x00, 0x42]);

        Assert.False(result.IsClean);
    }

    [Fact]
    public async Task RejectsHarmlessSecurityTestMarker()
    {
        var result = await ScanAsync(
            ".txt",
            Encoding.UTF8.GetBytes("SECUREFLOW_TEST_BLOCK"));

        Assert.False(result.IsClean);
        Assert.Contains("security scan", result.Error, StringComparison.OrdinalIgnoreCase);
    }

    private async Task<FileScanResult> ScanAsync(
        string extension,
        byte[] bytes)
    {
        await using var stream = new MemoryStream(bytes);
        return await scanner.ScanAsync(stream, extension);
    }
}
