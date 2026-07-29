using SecureFlow.Web.Data;
using SecureFlow.Web.Models;

namespace SecureFlow.Web.Security;

public interface ISecurityAuditService
{
    Task RecordAsync(
        HttpContext httpContext,
        string eventType,
        string outcome,
        string? userId,
        string? objectType = null,
        string? objectId = null,
        CancellationToken cancellationToken = default);
}

public sealed class SecurityAuditService(
    ApplicationDbContext dbContext,
    ILogger<SecurityAuditService> logger) : ISecurityAuditService
{
    public async Task RecordAsync(
        HttpContext httpContext,
        string eventType,
        string outcome,
        string? userId,
        string? objectType = null,
        string? objectId = null,
        CancellationToken cancellationToken = default)
    {
        var auditEvent = new SecurityAuditEvent
        {
            EventType = eventType,
            Outcome = outcome,
            UserId = userId,
            ObjectType = objectType,
            ObjectId = objectId,
            CorrelationId = httpContext.TraceIdentifier,
            SourceAddress = httpContext.Connection.RemoteIpAddress?.ToString()
        };

        dbContext.SecurityAuditEvents.Add(auditEvent);
        await dbContext.SaveChangesAsync(cancellationToken);

        logger.LogInformation(
            "SecurityAudit EventType={EventType} Outcome={Outcome} UserId={UserId} ObjectType={ObjectType} ObjectId={ObjectId} CorrelationId={CorrelationId}",
            eventType,
            outcome,
            userId,
            objectType,
            objectId,
            httpContext.TraceIdentifier);
    }
}
