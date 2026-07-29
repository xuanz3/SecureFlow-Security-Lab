using System.ComponentModel.DataAnnotations;

namespace SecureFlow.Web.Models;

public sealed class SecurityAuditEvent
{
    public long Id { get; set; }

    [Required, StringLength(80)]
    public string EventType { get; set; } = string.Empty;

    [Required, StringLength(30)]
    public string Outcome { get; set; } = string.Empty;

    [StringLength(450)]
    public string? UserId { get; set; }

    [StringLength(80)]
    public string? ObjectType { get; set; }

    [StringLength(100)]
    public string? ObjectId { get; set; }

    [Required, StringLength(100)]
    public string CorrelationId { get; set; } = string.Empty;

    [StringLength(45)]
    public string? SourceAddress { get; set; }

    public DateTimeOffset OccurredAtUtc { get; set; } = DateTimeOffset.UtcNow;
}
