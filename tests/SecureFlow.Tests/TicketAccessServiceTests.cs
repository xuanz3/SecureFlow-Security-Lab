using SecureFlow.Web.Models;
using SecureFlow.Web.Security;

namespace SecureFlow.Tests;

public sealed class TicketAccessServiceTests
{
    private readonly TicketAccessService _service = new();

    [Fact]
    public void OwnerCanReadOwnTicket()
    {
        var ticket = new Ticket { OwnerId = "alice" };
        Assert.True(_service.CanRead(ticket, "alice", isAdmin: false));
    }

    [Fact]
    public void UserCannotReadAnotherUsersTicket()
    {
        var ticket = new Ticket { OwnerId = "bob" };
        Assert.False(_service.CanRead(ticket, "alice", isAdmin: false));
    }

    [Fact]
    public void AdminCanReadAnotherUsersTicket()
    {
        var ticket = new Ticket { OwnerId = "bob" };
        Assert.True(_service.CanRead(ticket, "admin", isAdmin: true));
    }

    [Fact]
    public void UserCannotModifyAnotherUsersTicket()
    {
        var ticket = new Ticket { OwnerId = "bob" };
        Assert.False(_service.CanModify(ticket, "alice", isAdmin: false));
    }

    [Fact]
    public void NormalUserCannotUseAdminFunctions()
    {
        Assert.False(_service.CanUseAdminFunctions(isAdmin: false));
    }

    [Fact]
    public void AdminCanUseAdminFunctions()
    {
        Assert.True(_service.CanUseAdminFunctions(isAdmin: true));
    }
}
