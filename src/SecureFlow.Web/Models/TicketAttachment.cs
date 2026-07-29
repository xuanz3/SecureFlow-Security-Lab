using System.ComponentModel.DataAnnotations;

namespace SecureFlow.Web.Models;

public sealed class TicketAttachment
{
    public Guid Id { get; set; } = Guid.NewGuid();

    public Guid TicketId { get; set; }

    public Ticket Ticket { get; set; } = null!;

    [Required, StringLength(255)]
    public string OriginalName { get; set; } = string.Empty;

    [Required, StringLength(80)]
    public string StoredName { get; set; } = string.Empty;

    [Required, StringLength(100)]
    public string ContentType { get; set; } = string.Empty;

    public long SizeBytes { get; set; }

    [Required]
    public string UploadedByUserId { get; set; } = string.Empty;

    public DateTimeOffset UploadedAtUtc { get; set; } = DateTimeOffset.UtcNow;
}
