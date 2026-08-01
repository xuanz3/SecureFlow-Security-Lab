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
    IQuarantinedFileService quarantineService,
    ISecurityAuditService auditService,
    IWebHostEnvironment environment) : Controller
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
    public IActionResult Create() => View(new CreateTicketViewModel());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CreateTicketViewModel model)
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

        await auditService.RecordAsync(
            HttpContext,
            "TicketCreated",
            "Success",
            userId,
            "Ticket",
            ticket.Id.ToString());

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

        var userId = RequireUserId();
        if (!accessService.CanRead(ticket, userId, User.IsInRole(AppRoles.Admin)))
        {
            await RecordAccessDeniedAsync(userId, ticket.Id);
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
    [RequestSizeLimit(FileUploadValidator.MaximumRequestBytes)]
    [RequestFormLimits(
        MultipartBodyLengthLimit = FileUploadValidator.MaximumRequestBytes)]
    public async Task<IActionResult> UploadAttachment(Guid id, IFormFile? file)
    {
        var ticket = await dbContext.Tickets
            .SingleOrDefaultAsync(candidate => candidate.Id == id);
        if (ticket is null)
        {
            return NotFound();
        }

        var userId = RequireUserId();
        if (!accessService.CanModify(ticket, userId, User.IsInRole(AppRoles.Admin)))
        {
            await RecordAccessDeniedAsync(userId, ticket.Id);
            return Forbid();
        }

        if (file is null)
        {
            TempData["UploadError"] = "Select a file to upload.";
            return RedirectToAction(nameof(Details), new { id });
        }

        var validation = fileValidator.Validate(
            file.FileName,
            file.ContentType,
            file.Length);
        if (!validation.IsValid)
        {
            await auditService.RecordAsync(
                HttpContext,
                "AttachmentUpload",
                "Rejected",
                userId,
                "Ticket",
                ticket.Id.ToString());
            TempData["UploadError"] = validation.Error;
            return RedirectToAction(nameof(Details), new { id });
        }

        var storedName = $"{Guid.NewGuid():N}{validation.Extension}";
        var release = await quarantineService.InspectAndReleaseAsync(
            file,
            validation.Extension!,
            storedName,
            HttpContext.RequestAborted);

        if (!release.IsReleased)
        {
            await auditService.RecordAsync(
                HttpContext,
                "AttachmentScan",
                "Rejected",
                userId,
                "Ticket",
                ticket.Id.ToString());
            TempData["UploadError"] = release.Error;
            return RedirectToAction(nameof(Details), new { id });
        }

        dbContext.TicketAttachments.Add(new TicketAttachment
        {
            TicketId = ticket.Id,
            OriginalName = validation.SafeOriginalName,
            StoredName = storedName,
            ContentType = release.DetectedContentType!,
            SizeBytes = file.Length,
            UploadedByUserId = userId
        });
        await dbContext.SaveChangesAsync();

        await auditService.RecordAsync(
            HttpContext,
            "AttachmentScan",
            "Clean",
            userId,
            "Ticket",
            ticket.Id.ToString());

        await auditService.RecordAsync(
            HttpContext,
            "AttachmentUpload",
            "Success",
            userId,
            "Ticket",
            ticket.Id.ToString());

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
        if (!accessService.CanRead(
                attachment.Ticket,
                userId,
                User.IsInRole(AppRoles.Admin)))
        {
            await RecordAccessDeniedAsync(userId, attachment.TicketId);
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

        await auditService.RecordAsync(
            HttpContext,
            "AttachmentDownload",
            "Success",
            userId,
            "Attachment",
            attachment.Id.ToString());

        return PhysicalFile(
            path,
            attachment.ContentType,
            attachment.OriginalName);
    }

    private string RequireUserId() =>
        userManager.GetUserId(User)
        ?? throw new InvalidOperationException(
            "Authenticated user identifier is unavailable.");

    private Task RecordAccessDeniedAsync(string userId, Guid ticketId) =>
        auditService.RecordAsync(
            HttpContext,
            "TicketAccess",
            "Denied",
            userId,
            "Ticket",
            ticketId.ToString());
}
