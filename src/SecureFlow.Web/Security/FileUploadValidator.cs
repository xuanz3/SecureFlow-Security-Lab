namespace SecureFlow.Web.Security;

public sealed record FileValidationResult(
    bool IsValid,
    string? Error,
    string SafeOriginalName,
    string? Extension);

public interface IFileUploadValidator
{
    FileValidationResult Validate(string fileName, string contentType, long length);
}

public sealed class FileUploadValidator : IFileUploadValidator
{
    public const long MaximumBytes = 2 * 1024 * 1024;

    private static readonly IReadOnlyDictionary<string, string[]> Allowed =
        new Dictionary<string, string[]>(StringComparer.OrdinalIgnoreCase)
        {
            [".pdf"] = ["application/pdf"],
            [".png"] = ["image/png"],
            [".jpg"] = ["image/jpeg"],
            [".jpeg"] = ["image/jpeg"],
            [".txt"] = ["text/plain"]
        };

    public FileValidationResult Validate(string fileName, string contentType, long length)
    {
        var safeName = Path.GetFileName(fileName);
        var extension = Path.GetExtension(safeName);

        if (string.IsNullOrWhiteSpace(safeName) || string.IsNullOrWhiteSpace(extension))
        {
            return new(false, "A valid filename and extension are required.", safeName, null);
        }

        if (length <= 0 || length > MaximumBytes)
        {
            return new(false, "The file must be between 1 byte and 2 MB.", safeName, extension);
        }

        if (!Allowed.TryGetValue(extension, out var allowedTypes))
        {
            return new(false, "The file extension is not allowed.", safeName, extension);
        }

        if (!allowedTypes.Contains(contentType, StringComparer.OrdinalIgnoreCase))
        {
            return new(false, "The declared content type does not match the allowed type.", safeName, extension);
        }

        return new(true, null, safeName, extension.ToLowerInvariant());
    }
}
