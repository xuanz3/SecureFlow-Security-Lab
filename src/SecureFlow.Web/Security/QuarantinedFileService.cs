namespace SecureFlow.Web.Security;

public sealed record QuarantineReleaseResult(
    bool IsReleased,
    string? Error,
    string? DetectedContentType);

public interface IQuarantinedFileService
{
    Task<QuarantineReleaseResult> InspectAndReleaseAsync(
        IFormFile file,
        string extension,
        string storedName,
        CancellationToken cancellationToken = default);
}

public sealed class QuarantinedFileService(
    IFileSecurityScanner scanner,
    IWebHostEnvironment environment,
    ILogger<QuarantinedFileService> logger) : IQuarantinedFileService
{
    public async Task<QuarantineReleaseResult> InspectAndReleaseAsync(
        IFormFile file,
        string extension,
        string storedName,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(file);

        var applicationData = Path.Combine(environment.ContentRootPath, "App_Data");
        var quarantineRoot = Path.Combine(applicationData, "quarantine");
        var releaseRoot = Path.Combine(applicationData, "uploads");
        Directory.CreateDirectory(quarantineRoot);
        Directory.CreateDirectory(releaseRoot);

        var quarantinePath = Path.Combine(
            quarantineRoot,
            $"{Guid.NewGuid():N}.pending");
        var releasedPath = Path.Combine(releaseRoot, storedName);

        try
        {
            await using (var destination = new FileStream(
                quarantinePath,
                FileMode.CreateNew,
                FileAccess.Write,
                FileShare.None,
                bufferSize: 81920,
                options: FileOptions.Asynchronous | FileOptions.SequentialScan))
            {
                await file.CopyToAsync(destination, cancellationToken);
            }

            await using var source = new FileStream(
                quarantinePath,
                FileMode.Open,
                FileAccess.Read,
                FileShare.Read,
                bufferSize: 81920,
                options: FileOptions.Asynchronous | FileOptions.SequentialScan);

            var scan = await scanner.ScanAsync(
                source,
                extension,
                cancellationToken);

            if (!scan.IsClean)
            {
                logger.LogWarning(
                    "A quarantined upload was rejected by the local scanner.");
                return new(false, scan.Error, null);
            }

            File.Move(quarantinePath, releasedPath, overwrite: false);
            return new(true, null, scan.DetectedContentType);
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (Exception exception)
        {
            logger.LogError(
                exception,
                "The quarantined upload could not be inspected and released.");
            return new(
                false,
                "The file could not be safely processed.",
                null);
        }
        finally
        {
            if (File.Exists(quarantinePath))
            {
                File.Delete(quarantinePath);
            }
        }
    }
}
