using System.ComponentModel.DataAnnotations;

namespace SecureFlow.Web.Models;

public sealed class Ticket
{
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required, StringLength(120, MinimumLength = 4)]
    public string Title { get; set; } = string.Empty;

    [Required, StringLength(4000, MinimumLength = 10)]
    public string Description { get; set; } = string.Empty;

    public TicketStatus Status { get; set; } = TicketStatus.Open;

    [Required]
    public string OwnerId { get; set; } = string.Empty;

    public DateTimeOffset CreatedAtUtc { get; set; } = DateTimeOffset.UtcNow;

    public DateTimeOffset UpdatedAtUtc { get; set; } = DateTimeOffset.UtcNow;
}
