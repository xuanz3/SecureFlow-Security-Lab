using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SecureFlow.Web.Data;
using SecureFlow.Web.Models;
using SecureFlow.Web.Security;

namespace SecureFlow.Web.Controllers;

[Authorize]
public sealed class TicketsController(
    ApplicationDbContext dbContext,
    UserManager<IdentityUser> userManager,
    ITicketAccessService accessService,
    ILogger<TicketsController> logger) : Controller
{
    public async Task<IActionResult> Index()
    {
        var userId = userManager.GetUserId(User)
            ?? throw new InvalidOperationException("Authenticated user identifier is unavailable.");

        var query = dbContext.Tickets.AsNoTracking();

        if (!User.IsInRole(AppRoles.Admin))
        {
            query = query.Where(ticket => ticket.OwnerId == userId);
        }

        var tickets = await query
            .OrderByDescending(ticket => ticket.CreatedAtUtc)
            .ToListAsync();

        return View(tickets);
    }

    [HttpGet]
    public IActionResult Create() => View(new Ticket());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(Ticket model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var userId = userManager.GetUserId(User)
            ?? throw new InvalidOperationException("Authenticated user identifier is unavailable.");

        var ticket = new Ticket
        {
            Title = model.Title.Trim(),
            Description = model.Description.Trim(),
            OwnerId = userId
        };

        dbContext.Tickets.Add(ticket);
        await dbContext.SaveChangesAsync();

        logger.LogInformation(
            "SecurityAudit TicketCreated UserId={UserId} TicketId={TicketId} CorrelationId={CorrelationId}",
            userId,
            ticket.Id,
            HttpContext.TraceIdentifier);

        return RedirectToAction(nameof(Details), new { id = ticket.Id });
    }

    public async Task<IActionResult> Details(Guid id)
    {
        var ticket = await dbContext.Tickets.AsNoTracking()
            .SingleOrDefaultAsync(candidate => candidate.Id == id);

        if (ticket is null)
        {
            return NotFound();
        }

        var userId = userManager.GetUserId(User)
            ?? throw new InvalidOperationException("Authenticated user identifier is unavailable.");

        if (!accessService.CanRead(ticket, userId, User.IsInRole(AppRoles.Admin)))
        {
            logger.LogWarning(
                "SecurityAudit TicketAccessDenied UserId={UserId} TicketId={TicketId} CorrelationId={CorrelationId}",
                userId,
                ticket.Id,
                HttpContext.TraceIdentifier);
            return Forbid();
        }

        return View(ticket);
    }
}
