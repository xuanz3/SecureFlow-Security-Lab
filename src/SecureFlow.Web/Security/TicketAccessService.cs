using SecureFlow.Web.Models;

namespace SecureFlow.Web.Security;

public interface ITicketAccessService
{
    bool CanRead(Ticket ticket, string userId, bool isAdmin);
    bool CanModify(Ticket ticket, string userId, bool isAdmin);
    bool CanUseAdminFunctions(bool isAdmin);
}

public sealed class TicketAccessService : ITicketAccessService
{
    public bool CanRead(Ticket ticket, string userId, bool isAdmin) =>
        isAdmin || string.Equals(ticket.OwnerId, userId, StringComparison.Ordinal);

    public bool CanModify(Ticket ticket, string userId, bool isAdmin) =>
        isAdmin || string.Equals(ticket.OwnerId, userId, StringComparison.Ordinal);

    public bool CanUseAdminFunctions(bool isAdmin) => isAdmin;
}
