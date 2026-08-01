using Microsoft.AspNetCore.Authorization;
using SecureFlow.Web.Controllers;
using SecureFlow.Web.Models;
using SecureFlow.Web.Security;

namespace SecureFlow.Tests.Security;

public sealed class AuthorizationBoundaryTests
{
    private readonly TicketAccessService service = new();

    [Fact]
    public void NonOwnerCannotReadAnotherUsersTicket()
    {
        var ticket = TicketOwnedBy("bob-user");

        Assert.False(service.CanRead(ticket, "alice-user", isAdmin: false));
    }

    [Fact]
    public void NonOwnerCannotModifyAnotherUsersTicket()
    {
        var ticket = TicketOwnedBy("bob-user");

        Assert.False(service.CanModify(ticket, "alice-user", isAdmin: false));
    }

    [Fact]
    public void OwnerCanReadAndModifyOwnTicket()
    {
        var ticket = TicketOwnedBy("alice-user");

        Assert.True(service.CanRead(ticket, "alice-user", isAdmin: false));
        Assert.True(service.CanModify(ticket, "alice-user", isAdmin: false));
    }

    [Fact]
    public void AdministratorCanReadAndModifyAnyTicket()
    {
        var ticket = TicketOwnedBy("bob-user");

        Assert.True(service.CanRead(ticket, "admin-user", isAdmin: true));
        Assert.True(service.CanModify(ticket, "admin-user", isAdmin: true));
    }

    [Fact]
    public void NormalUserCannotUseAdministratorFunctions()
    {
        Assert.False(service.CanUseAdminFunctions(isAdmin: false));
    }

    [Fact]
    public void AdministratorCanUseAdministratorFunctions()
    {
        Assert.True(service.CanUseAdminFunctions(isAdmin: true));
    }

    [Fact]
    public void TicketsControllerRequiresAuthentication()
    {
        var attribute = Assert.Single(
            typeof(TicketsController)
                .GetCustomAttributes(typeof(AuthorizeAttribute), inherit: true)
                .Cast<AuthorizeAttribute>());

        Assert.True(string.IsNullOrWhiteSpace(attribute.Roles));
    }

    [Fact]
    public void AdminControllerRequiresTheAdministratorRole()
    {
        var attribute = Assert.Single(
            typeof(AdminController)
                .GetCustomAttributes(typeof(AuthorizeAttribute), inherit: true)
                .Cast<AuthorizeAttribute>());

        Assert.Equal(AppRoles.Admin, attribute.Roles);
    }

    private static Ticket TicketOwnedBy(string ownerId) =>
        new()
        {
            Title = "Authorisation regression ticket",
            Description = "Fictional ticket used only for an automated unit test.",
            OwnerId = ownerId
        };
}
