using System.ComponentModel.DataAnnotations;
using SecureFlow.Web.Models;

namespace SecureFlow.Tests;

public sealed class CreateTicketViewModelTests
{
    [Fact]
    public void ValidInputPassesValidation()
    {
        var model = new CreateTicketViewModel
        {
            Title = "Unable to access payroll portal",
            Description = "This fictional ticket has enough content for validation."
        };

        Assert.Empty(Validate(model));
    }

    [Fact]
    public void ShortTitleFailsValidation()
    {
        var model = new CreateTicketViewModel
        {
            Title = "Bad",
            Description = "This fictional ticket has enough content for validation."
        };

        Assert.Contains(Validate(model), result =>
            result.MemberNames.Contains(nameof(CreateTicketViewModel.Title)));
    }

    [Fact]
    public void ShortDescriptionFailsValidation()
    {
        var model = new CreateTicketViewModel
        {
            Title = "Valid title",
            Description = "Too short"
        };

        Assert.Contains(Validate(model), result =>
            result.MemberNames.Contains(nameof(CreateTicketViewModel.Description)));
    }

    private static IReadOnlyCollection<ValidationResult> Validate(object model)
    {
        var results = new List<ValidationResult>();
        Validator.TryValidateObject(
            model,
            new ValidationContext(model),
            results,
            validateAllProperties: true);
        return results;
    }
}
