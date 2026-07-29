using System.ComponentModel.DataAnnotations;

namespace SecureFlow.Web.Models;

public sealed class CreateTicketViewModel
{
    [Required, StringLength(120, MinimumLength = 4)]
    public string Title { get; set; } = string.Empty;

    [Required, StringLength(4000, MinimumLength = 10)]
    public string Description { get; set; } = string.Empty;
}
