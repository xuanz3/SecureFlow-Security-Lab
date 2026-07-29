using SecureFlow.Web.Security;

namespace SecureFlow.Tests;

public sealed class FileUploadValidatorTests
{
    private readonly FileUploadValidator _validator = new();

    [Fact]
    public void AllowsPdfWithinSizeLimit()
    {
        var result = _validator.Validate("report.pdf", "application/pdf", 1024);
        Assert.True(result.IsValid);
        Assert.Equal(".pdf", result.Extension);
    }

    [Fact]
    public void RejectsExecutableExtension()
    {
        var result = _validator.Validate("payload.exe", "application/octet-stream", 1024);
        Assert.False(result.IsValid);
    }

    [Fact]
    public void RejectsOversizedFile()
    {
        var result = _validator.Validate(
            "report.pdf",
            "application/pdf",
            FileUploadValidator.MaximumBytes + 1);
        Assert.False(result.IsValid);
    }

    [Fact]
    public void RejectsMismatchedContentType()
    {
        var result = _validator.Validate("image.png", "text/html", 1024);
        Assert.False(result.IsValid);
    }

    [Fact]
    public void RemovesPathTraversalFromOriginalName()
    {
        var result = _validator.Validate("../../report.pdf", "application/pdf", 1024);
        Assert.True(result.IsValid);
        Assert.Equal("report.pdf", result.SafeOriginalName);
    }

    [Fact]
    public void RejectsEmptyFile()
    {
        var result = _validator.Validate("report.pdf", "application/pdf", 0);
        Assert.False(result.IsValid);
    }
}
