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
    IFileUploadValidator fileValidator,
    IWebHostEnvironment environment,
    ILogger<TicketsController> logger) : Controller
{
    public async Task<IActionResult> Index()
    {
        var userId = RequireUserId();
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

        var userId = RequireUserId();
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

        if (!accessService.CanRead(ticket, RequireUserId(), User.IsInRole(AppRoles.Admin)))
        {
            LogAccessDenied(ticket.Id);
            return Forbid();
        }

        ViewBag.Attachments = await dbContext.TicketAttachments
            .AsNoTracking()
            .Where(attachment => attachment.TicketId == id)
            .OrderByDescending(attachment => attachment.UploadedAtUtc)
            .ToListAsync();

        return View(ticket);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> UploadAttachment(Guid id, IFormFile file)
    {
        var ticket = await dbContext.Tickets.SingleOrDefaultAsync(candidate => candidate.Id == id);
        if (ticket is null)
        {
            return NotFound();
        }

        var userId = RequireUserId();
        if (!accessService.CanModify(ticket, userId, User.IsInRole(AppRoles.Admin)))
        {
            LogAccessDenied(ticket.Id);
            return Forbid();
        }

        var validation = fileValidator.Validate(file.FileName, file.ContentType, file.Length);
        if (!validation.IsValid)
        {
            TempData["UploadError"] = validation.Error;
            return RedirectToAction(nameof(Details), new { id });
        }

        var storedName = $"{Guid.NewGuid():N}{validation.Extension}";
        var uploadRoot = Path.Combine(environment.ContentRootPath, "App_Data", "uploads");
        Directory.CreateDirectory(uploadRoot);
        var destination = Path.Combine(uploadRoot, storedName);

        await using (var stream = System.IO.File.Create(destination))
        {
            await file.CopyToAsync(stream);
        }

        dbContext.TicketAttachments.Add(new TicketAttachment
        {
            TicketId = ticket.Id,
            OriginalName = validation.SafeOriginalName,
            StoredName = storedName,
            ContentType = file.ContentType,
            SizeBytes = file.Length,
            UploadedByUserId = userId
        });
        await dbContext.SaveChangesAsync();

        logger.LogInformation(
            "SecurityAudit AttachmentUploaded UserId={UserId} TicketId={TicketId} StoredName={StoredName} SizeBytes={SizeBytes} CorrelationId={CorrelationId}",
            userId,
            ticket.Id,
            storedName,
            file.Length,
            HttpContext.TraceIdentifier);

        return RedirectToAction(nameof(Details), new { id });
    }

    public async Task<IActionResult> DownloadAttachment(Guid id)
    {
        var attachment = await dbContext.TicketAttachments
            .AsNoTracking()
            .Include(candidate => candidate.Ticket)
            .SingleOrDefaultAsync(candidate => candidate.Id == id);

        if (attachment is null)
        {
            return NotFound();
        }

        var userId = RequireUserId();
        if (!accessService.CanRead(attachment.Ticket, userId, User.IsInRole(AppRoles.Admin)))
        {
            LogAccessDenied(attachment.TicketId);
            return Forbid();
        }

        var path = Path.Combine(
            environment.ContentRootPath,
            "App_Data",
            "uploads",
            attachment.StoredName);

        if (!System.IO.File.Exists(path))
        {
            return NotFound();
        }

        logger.LogInformation(
            "SecurityAudit AttachmentDownloaded UserId={UserId} TicketId={TicketId} AttachmentId={AttachmentId} CorrelationId={CorrelationId}",
            userId,
            attachment.TicketId,
            attachment.Id,
            HttpContext.TraceIdentifier);

        return PhysicalFile(path, attachment.ContentType, attachment.OriginalName);
    }

    private string RequireUserId() =>
        userManager.GetUserId(User)
        ?? throw new InvalidOperationException("Authenticated user identifier is unavailable.");

    private void LogAccessDenied(Guid ticketId) =>
        logger.LogWarning(
            "SecurityAudit TicketAccessDenied UserId={UserId} TicketId={TicketId} CorrelationId={CorrelationId}",
            userManager.GetUserId(User),
            ticketId,
            HttpContext.TraceIdentifier);
}
