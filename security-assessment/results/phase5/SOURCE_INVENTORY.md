# Phase 5 Source Inventory

Generated from the tracked repository at the start of Phase 5.

This inventory records control locations before remediation. It deliberately
excludes `.env`, local credentials, database contents and untracked files.

## Object-level authorisation

| File | Line | Matched source |
|---|---:|---|
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 38 | `userId: null);` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 74 | `[Authorize]` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 79 | `var userId = userManager.GetUserId(User);` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 85 | `userId);` |
| `src/SecureFlow.Web/Controllers/AdminController.cs` | 9 | `[Authorize(Roles = AppRoles.Admin)]` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 11 | `[Authorize]` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 12 | `public sealed class TicketsController(` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 22 | `var userId = RequireUserId();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 27 | `query = query.Where(ticket => ticket.OwnerId == userId);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 49 | `var userId = RequireUserId();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 54 | `OwnerId = userId` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 64 | `userId,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 81 | `var userId = RequireUserId();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 82 | `if (!accessService.CanRead(ticket, userId, User.IsInRole(AppRoles.Admin)))` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 84 | `await RecordAccessDeniedAsync(userId, ticket.Id);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 85 | `return Forbid();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 90 | `.Where(attachment => attachment.TicketId == id)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 107 | `var userId = RequireUserId();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 108 | `if (!accessService.CanModify(ticket, userId, User.IsInRole(AppRoles.Admin)))` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 110 | `await RecordAccessDeniedAsync(userId, ticket.Id);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 111 | `return Forbid();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 121 | `userId,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 140 | `TicketId = ticket.Id,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 145 | `UploadedByUserId = userId` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 153 | `userId,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 172 | `var userId = RequireUserId();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 173 | `if (!accessService.CanRead(attachment.Ticket, userId, User.IsInRole(AppRoles.Admin)))` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 175 | `await RecordAccessDeniedAsync(userId, attachment.TicketId);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 176 | `return Forbid();` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 194 | `userId,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 201 | `private string RequireUserId() =>` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 202 | `userManager.GetUserId(User)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 205 | `private Task RecordAccessDeniedAsync(string userId, Guid ticketId) =>` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 210 | `userId,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 212 | `ticketId.ToString());` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 21 | `entity.HasIndex(ticket => new { ticket.OwnerId, ticket.CreatedAtUtc });` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 24 | `entity.Property(ticket => ticket.OwnerId).HasMaxLength(450);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 30 | `entity.HasIndex(attachment => attachment.TicketId);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 34 | `entity.Property(attachment => attachment.UploadedByUserId).HasMaxLength(450);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 37 | `.HasForeignKey(attachment => attachment.TicketId)` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 157 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 163 | `b.HasIndex("UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 179 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 185 | `b.HasIndex("UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 192 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 198 | `b.HasKey("UserId", "RoleId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 207 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 219 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 237 | `.HasForeignKey("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 246 | `.HasForeignKey("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 261 | `.HasForeignKey("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 270 | `.HasForeignKey("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 81 | `UserId = table.Column<string>(type: "text", nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 89 | `name: "FK_AspNetUserClaims_AspNetUsers_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 90 | `column: x => x.UserId,` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 103 | `UserId = table.Column<string>(type: "text", nullable: false)` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 109 | `name: "FK_AspNetUserLogins_AspNetUsers_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 110 | `column: x => x.UserId,` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 120 | `UserId = table.Column<string>(type: "text", nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 125 | `table.PrimaryKey("PK_AspNetUserRoles", x => new { x.UserId, x.RoleId });` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 133 | `name: "FK_AspNetUserRoles_AspNetUsers_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 134 | `column: x => x.UserId,` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 144 | `UserId = table.Column<string>(type: "text", nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 151 | `table.PrimaryKey("PK_AspNetUserTokens", x => new { x.UserId, x.LoginProvider, x.Name });` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 153 | `name: "FK_AspNetUserTokens_AspNetUsers_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 154 | `column: x => x.UserId,` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 172 | `name: "IX_AspNetUserClaims_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 174 | `column: "UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 177 | `name: "IX_AspNetUserLogins_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 179 | `column: "UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 157 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 163 | `b.HasIndex("UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 179 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 185 | `b.HasIndex("UserId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 192 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 198 | `b.HasKey("UserId", "RoleId");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 207 | `b.Property<string>("UserId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 219 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 238 | `b.Property<string>("OwnerId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 256 | `b.HasIndex("OwnerId", "CreatedAtUtc");` |
| — | — | 72 additional matches omitted |

## Administrator authorisation

| File | Line | Matched source |
|---|---:|---|
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 74 | `[Authorize]` |
| `src/SecureFlow.Web/Controllers/AdminController.cs` | 9 | `[Authorize(Roles = AppRoles.Admin)]` |
| `src/SecureFlow.Web/Controllers/AdminController.cs` | 10 | `public sealed class AdminController(ApplicationDbContext dbContext) : Controller` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 11 | `[Authorize]` |

## Upload validation and storage

| File | Line | Matched source |
|---|---:|---|
| `.github/workflows/ci.yml` | 49 | `--logger "trx;LogFileName=secureflow-tests.trx" \` |
| `infrastructure/docker/Dockerfile` | 20 | `RUN mkdir -p /app/App_Data/uploads && chown -R appuser:appgroup /app/App_Data` |
| `infrastructure/docker/compose.yml` | 41 | `- secureflow-uploads:/app/App_Data/uploads` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 16 | `IFileUploadValidator fileValidator,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 88 | `ViewBag.Attachments = await dbContext.TicketAttachments` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 90 | `.Where(attachment => attachment.TicketId == id)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 91 | `.OrderByDescending(attachment => attachment.UploadedAtUtc)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 99 | `public async Task<IActionResult> UploadAttachment(Guid id, IFormFile file)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 114 | `var validation = fileValidator.Validate(file.FileName, file.ContentType, file.Length);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 119 | `"AttachmentUpload",` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 138 | `dbContext.TicketAttachments.Add(new TicketAttachment` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 143 | `ContentType = file.ContentType,` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 151 | `"AttachmentUpload",` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 160 | `public async Task<IActionResult> DownloadAttachment(Guid id)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 162 | `var attachment = await dbContext.TicketAttachments` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 167 | `if (attachment is null)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 173 | `if (!accessService.CanRead(attachment.Ticket, userId, User.IsInRole(AppRoles.Admin)))` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 175 | `await RecordAccessDeniedAsync(userId, attachment.TicketId);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 183 | `attachment.StoredName);` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 192 | `"AttachmentDownload",` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 195 | `"Attachment",` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 196 | `attachment.Id.ToString());` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 198 | `return PhysicalFile(path, attachment.ContentType, attachment.OriginalName);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 11 | `public DbSet<TicketAttachment> TicketAttachments => Set<TicketAttachment>();` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 27 | `builder.Entity<TicketAttachment>(entity =>` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 29 | `entity.HasKey(attachment => attachment.Id);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 30 | `entity.HasIndex(attachment => attachment.TicketId);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 31 | `entity.Property(attachment => attachment.OriginalName).HasMaxLength(255);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 32 | `entity.Property(attachment => attachment.StoredName).HasMaxLength(80);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 33 | `entity.Property(attachment => attachment.ContentType).HasMaxLength(100);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 34 | `entity.Property(attachment => attachment.UploadedByUserId).HasMaxLength(450);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 35 | `entity.HasOne(attachment => attachment.Ticket)` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 37 | `.HasForeignKey(attachment => attachment.TicketId)` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 15 | `[Migration("20260729121034_AddAttachmentsAndAudit")]` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 16 | `partial class AddAttachmentsAndAudit` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 312 | `modelBuilder.Entity("SecureFlow.Web.Models.TicketAttachment", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 318 | `b.Property<string>("ContentType")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 351 | `b.ToTable("TicketAttachments");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 405 | `modelBuilder.Entity("SecureFlow.Web.Models.TicketAttachment", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 10 | `public partial class AddAttachmentsAndAudit : Migration` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 36 | `name: "TicketAttachments",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 43 | `ContentType = table.Column<string>(type: "character varying(100)", maxLength: 100, nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 50 | `table.PrimaryKey("PK_TicketAttachments", x => x.Id);` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 52 | `name: "FK_TicketAttachments_Tickets_TicketId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 70 | `name: "IX_TicketAttachments_TicketId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 71 | `table: "TicketAttachments",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 82 | `name: "TicketAttachments");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 309 | `modelBuilder.Entity("SecureFlow.Web.Models.TicketAttachment", b =>` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 315 | `b.Property<string>("ContentType")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 348 | `b.ToTable("TicketAttachments");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 402 | `modelBuilder.Entity("SecureFlow.Web.Models.TicketAttachment", b =>` |
| `src/SecureFlow.Web/Models/TicketAttachment.cs` | 5 | `public sealed class TicketAttachment` |
| `src/SecureFlow.Web/Models/TicketAttachment.cs` | 20 | `public string ContentType { get; set; } = string.Empty;` |
| `src/SecureFlow.Web/Program.cs` | 67 | `builder.Services.AddSingleton<IFileUploadValidator, FileUploadValidator>();` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 9 | `public interface IFileUploadValidator` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 11 | `FileValidationResult Validate(string fileName, string contentType, long length);` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 14 | `public sealed class FileUploadValidator : IFileUploadValidator` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 28 | `public FileValidationResult Validate(string fileName, string contentType, long length)` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 30 | `var safeName = Path.GetFileName(fileName);` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 35 | `return new(false, "A valid filename and extension are required.", safeName, null);` |
| `src/SecureFlow.Web/Security/FileUploadValidator.cs` | 48 | `if (!allowedTypes.Contains(contentType, StringComparer.OrdinalIgnoreCase))` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 5 | `var attachments = ViewBag.Attachments as IReadOnlyCollection<TicketAttachment>` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 6 | `?? Array.Empty<TicketAttachment>();` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 21 | `<h2>Protected attachments</h2>` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 26 | `<form asp-action="UploadAttachment" asp-route-id="@Model.Id" method="post" enctype="multipart/form-data">` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 32 | `@if (attachments.Count > 0)` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 35 | `@foreach (var attachment in attachments)` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 38 | `<a asp-action="DownloadAttachment" asp-route-id="@attachment.Id">@attachment.OriginalName</a>` |
| `src/SecureFlow.Web/Views/Tickets/Details.cshtml` | 39 | `— @attachment.SizeBytes bytes` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 4878 | `const DefaultContentType = {` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 4943 | `}, DefaultContentType);` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 5016 | `const AttachmentMap = {` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 5287 | `const attachment = AttachmentMap[placement.toUpperCase()];` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 5288 | `return createPopper(this._element, tip, this._getPopperConfig(attachment));` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 5305 | `_getPopperConfig(attachment) {` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 5307 | `placement: attachment,` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js.map` | 1 | `{"version":3,"file":"bootstrap.bundle.js","sources":["../../js/src/dom/data.js","../../js/src/util/index.js","../../js/src/dom/event-handler.js","../../js/src/dom/manipulator.js...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.min.js.map` | 1 | `{"version":3,"names":["elementMap","Map","Data","set","element","key","instance","has","instanceMap","get","size","console","error","Array","from","keys","remove","delete","TRAN...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.esm.js` | 3035 | `const DefaultContentType = {` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.esm.js` | 3100 | `}, DefaultContentType);` |
| — | — | 31 additional matches omitted |

## Authentication and rate limiting

| File | Line | Matched source |
|---|---:|---|
| `.github/workflows/publish-image.yml` | 34 | `uses: docker/login-action@dbcb813823bdd20940b903addbd779551569679f` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 17 | `public IActionResult Login(string? returnUrl = null) =>` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 18 | `View(new LoginViewModel { ReturnUrl = returnUrl });` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 23 | `[EnableRateLimiting("login")]` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 24 | `public async Task<IActionResult> Login(LoginViewModel model)` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 36 | `"Login",` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 53 | `"Login",` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 62 | `"Login",` |
| `src/SecureFlow.Web/Data/DbInitializer.cs` | 48 | `logger.LogInformation("Database migration and fictional development identity seeding completed.");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 168 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 170 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 183 | `b.HasKey("LoginProvider", "ProviderKey");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 187 | `b.ToTable("AspNetUserLogins", (string)null);` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 210 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 219 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.Designer.cs` | 242 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 97 | `name: "AspNetUserLogins",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 100 | `LoginProvider = table.Column<string>(type: "text", nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 107 | `table.PrimaryKey("PK_AspNetUserLogins", x => new { x.LoginProvider, x.ProviderKey });` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 109 | `name: "FK_AspNetUserLogins_AspNetUsers_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 145 | `LoginProvider = table.Column<string>(type: "text", nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 151 | `table.PrimaryKey("PK_AspNetUserTokens", x => new { x.UserId, x.LoginProvider, x.Name });` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 177 | `name: "IX_AspNetUserLogins_UserId",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 178 | `table: "AspNetUserLogins",` |
| `src/SecureFlow.Web/Data/Migrations/20260729120950_InitialCreate.cs` | 208 | `name: "AspNetUserLogins");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 168 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 170 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 183 | `b.HasKey("LoginProvider", "ProviderKey");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 187 | `b.ToTable("AspNetUserLogins", (string)null);` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 210 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 219 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121014_AddTickets.Designer.cs` | 279 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 168 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 170 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 183 | `b.HasKey("LoginProvider", "ProviderKey");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 187 | `b.ToTable("AspNetUserLogins", (string)null);` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 210 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 219 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 372 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 165 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 167 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 180 | `b.HasKey("LoginProvider", "ProviderKey");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 184 | `b.ToTable("AspNetUserLogins", (string)null);` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 207 | `b.Property<string>("LoginProvider")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 216 | `b.HasKey("UserId", "LoginProvider", "Name");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 369 | `modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>` |
| `src/SecureFlow.Web/Models/LoginViewModel.cs` | 5 | `public sealed class LoginViewModel` |
| `src/SecureFlow.Web/Program.cs` | 50 | `options.LoginPath = "/Account/Login";` |
| `src/SecureFlow.Web/Program.cs` | 54 | `builder.Services.AddRateLimiter(options =>` |
| `src/SecureFlow.Web/Program.cs` | 57 | `options.AddFixedWindowLimiter("login", limiter =>` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 45 | `logger.LogInformation(` |
| `src/SecureFlow.Web/Views/Account/Login.cshtml` | 1 | `@model SecureFlow.Web.Models.LoginViewModel` |
| `src/SecureFlow.Web/Views/Account/Login.cshtml` | 8 | `<form asp-action="Login" method="post">` |
| `src/SecureFlow.Web/Views/Shared/_Layout.cshtml` | 31 | `<a asp-controller="Account" asp-action="Login">Sign in</a>` |

## Security headers

| File | Line | Matched source |
|---|---:|---|
| `src/SecureFlow.Web/Program.cs` | 83 | `app.UseMiddleware<SecurityHeadersMiddleware>();` |
| `src/SecureFlow.Web/Security/SecurityHeadersMiddleware.cs` | 3 | `public sealed class SecurityHeadersMiddleware(RequestDelegate next)` |
| `src/SecureFlow.Web/Security/SecurityHeadersMiddleware.cs` | 14 | `headers["Content-Security-Policy"] =` |
| `src/SecureFlow.Web/Security/SecurityHeadersMiddleware.cs` | 17 | `"style-src 'self' 'unsafe-inline'";` |

## Container hardening

| File | Line | Matched source |
|---|---:|---|
| `infrastructure/docker/Dockerfile` | 1 | `FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build` |
| `infrastructure/docker/Dockerfile` | 16 | `FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final` |
| `infrastructure/docker/Dockerfile` | 17 | `RUN addgroup -S appgroup && adduser -S appuser -G appgroup` |
| `infrastructure/docker/Dockerfile` | 21 | `USER appuser` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 31 | `var user = await userManager.FindByEmailAsync(model.Email);` |
| `src/SecureFlow.Web/Controllers/AccountController.cs` | 32 | `if (user is null)` |
| `src/SecureFlow.Web/Controllers/TicketsController.cs` | 203 | `?? throw new InvalidOperationException("Authenticated user identifier is unavailable.");` |
| `src/SecureFlow.Web/Data/DbInitializer.cs` | 21 | `foreach (var role in new[] { AppRoles.Admin, AppRoles.User })` |
| `src/SecureFlow.Web/Data/DbInitializer.cs` | 73 | `var user = new IdentityUser` |
| `src/SecureFlow.Web/Security/AppRoles.cs` | 6 | `public const string User = "User";` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js` | 1265 | `// would stop cycling until user tapped out of it;` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.js.map` | 1 | `{"version":3,"file":"bootstrap.bundle.js","sources":["../../js/src/dom/data.js","../../js/src/util/index.js","../../js/src/dom/event-handler.js","../../js/src/dom/manipulator.js...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.bundle.min.js.map` | 1 | `{"version":3,"names":["elementMap","Map","Data","set","element","key","instance","has","instanceMap","get","size","console","error","Array","from","keys","remove","delete","TRAN...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.esm.js` | 1261 | `// would stop cycling until user tapped out of it;` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.esm.js.map` | 1 | `{"version":3,"file":"bootstrap.esm.js","sources":["../../js/src/dom/data.js","../../js/src/util/index.js","../../js/src/dom/event-handler.js","../../js/src/dom/manipulator.js","...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.esm.min.js.map` | 1 | `{"version":3,"names":["elementMap","Map","Data","set","element","key","instance","has","instanceMap","get","size","console","error","Array","from","keys","remove","delete","MAX_...` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.js` | 1284 | `// would stop cycling until user tapped out of it;` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.js.map` | 1 | `{"version":3,"file":"bootstrap.js","sources":["../../js/src/dom/data.js","../../js/src/util/index.js","../../js/src/dom/event-handler.js","../../js/src/dom/manipulator.js","../....` |
| `src/SecureFlow.Web/wwwroot/lib/bootstrap/dist/js/bootstrap.min.js.map` | 1 | `{"version":3,"names":["elementMap","Map","Data","set","element","key","instance","has","instanceMap","get","size","console","error","Array","from","keys","remove","delete","TRAN...` |
| `src/SecureFlow.Web/wwwroot/lib/jquery-validation/dist/jquery.validate.js` | 76 | `//   - A user defined a \`submitHandler\`` |
| `src/SecureFlow.Web/wwwroot/lib/jquery-validation/dist/jquery.validate.js` | 783 | `// if the former exists, otherwise user the global one in case it exists.` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 1823 | `// The user may use createPseudo to indicate that` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 4122 | `var dataUser = new Data();` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 4132 | `//	4. _Never_ expose "private" data to user code (TODO: Drop _data, _removeData)` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 4133 | `//	5. Avoid exposing implementation details on user objects (eg. expando properties)` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 5841 | `// 2. Copy user data` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 9701 | `// Make this explicit, since user can override this through ajaxSetup (trac-11264)` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.js` | 10220 | `// user can override it through ajaxSetup method` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.slim.js` | 1823 | `// The user may use createPseudo to indicate that` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.slim.js` | 4122 | `var dataUser = new Data();` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.slim.js` | 4132 | `//	4. _Never_ expose "private" data to user code (TODO: Drop _data, _removeData)` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.slim.js` | 4133 | `//	5. Avoid exposing implementation details on user objects (eg. expando properties)` |
| `src/SecureFlow.Web/wwwroot/lib/jquery/dist/jquery.slim.js` | 5841 | `// 2. Copy user data` |

## Audit and detection fields

| File | Line | Matched source |
|---|---:|---|
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 12 | `public DbSet<SecurityAuditEvent> SecurityAuditEvents => Set<SecurityAuditEvent>();` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 41 | `builder.Entity<SecurityAuditEvent>(entity =>` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 44 | `entity.HasIndex(auditEvent => auditEvent.OccurredAtUtc);` |
| `src/SecureFlow.Web/Data/ApplicationDbContext.cs` | 45 | `entity.HasIndex(auditEvent => new { auditEvent.EventType, auditEvent.Outcome });` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 224 | `modelBuilder.Entity("SecureFlow.Web.Models.SecurityAuditEvent", b =>` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 232 | `b.Property<string>("CorrelationId")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 237 | `b.Property<string>("EventType")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 250 | `b.Property<DateTimeOffset>("OccurredAtUtc")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 253 | `b.Property<string>("Outcome")` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 268 | `b.HasIndex("OccurredAtUtc");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 270 | `b.HasIndex("EventType", "Outcome");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.Designer.cs` | 272 | `b.ToTable("SecurityAuditEvents");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 16 | `name: "SecurityAuditEvents",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 21 | `EventType = table.Column<string>(type: "character varying(80)", maxLength: 80, nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 22 | `Outcome = table.Column<string>(type: "character varying(30)", maxLength: 30, nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 26 | `CorrelationId = table.Column<string>(type: "character varying(100)", maxLength: 100, nullable: false),` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 28 | `OccurredAtUtc = table.Column<DateTimeOffset>(type: "timestamp with time zone", nullable: false)` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 32 | `table.PrimaryKey("PK_SecurityAuditEvents", x => x.Id);` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 60 | `name: "IX_SecurityAuditEvents_EventType_Outcome",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 61 | `table: "SecurityAuditEvents",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 62 | `columns: new[] { "EventType", "Outcome" });` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 65 | `name: "IX_SecurityAuditEvents_OccurredAtUtc",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 66 | `table: "SecurityAuditEvents",` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 67 | `column: "OccurredAtUtc");` |
| `src/SecureFlow.Web/Data/Migrations/20260729121034_AddAttachmentsAndAudit.cs` | 79 | `name: "SecurityAuditEvents");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 221 | `modelBuilder.Entity("SecureFlow.Web.Models.SecurityAuditEvent", b =>` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 229 | `b.Property<string>("CorrelationId")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 234 | `b.Property<string>("EventType")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 247 | `b.Property<DateTimeOffset>("OccurredAtUtc")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 250 | `b.Property<string>("Outcome")` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 265 | `b.HasIndex("OccurredAtUtc");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 267 | `b.HasIndex("EventType", "Outcome");` |
| `src/SecureFlow.Web/Data/Migrations/ApplicationDbContextModelSnapshot.cs` | 269 | `b.ToTable("SecurityAuditEvents");` |
| `src/SecureFlow.Web/Models/SecurityAuditEvent.cs` | 5 | `public sealed class SecurityAuditEvent` |
| `src/SecureFlow.Web/Models/SecurityAuditEvent.cs` | 10 | `public string EventType { get; set; } = string.Empty;` |
| `src/SecureFlow.Web/Models/SecurityAuditEvent.cs` | 13 | `public string Outcome { get; set; } = string.Empty;` |
| `src/SecureFlow.Web/Models/SecurityAuditEvent.cs` | 25 | `public string CorrelationId { get; set; } = string.Empty;` |
| `src/SecureFlow.Web/Models/SecurityAuditEvent.cs` | 30 | `public DateTimeOffset OccurredAtUtc { get; set; } = DateTimeOffset.UtcNow;` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 10 | `string eventType,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 11 | `string outcome,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 24 | `string eventType,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 25 | `string outcome,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 31 | `var auditEvent = new SecurityAuditEvent` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 33 | `EventType = eventType,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 34 | `Outcome = outcome,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 38 | `CorrelationId = httpContext.TraceIdentifier,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 42 | `dbContext.SecurityAuditEvents.Add(auditEvent);` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 46 | `"SecurityAudit EventType={EventType} Outcome={Outcome} UserId={UserId} ObjectType={ObjectType} ObjectId={ObjectId} CorrelationId={CorrelationId}",` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 47 | `eventType,` |
| `src/SecureFlow.Web/Security/SecurityAuditService.cs` | 48 | `outcome,` |
| `src/SecureFlow.Web/wwwroot/lib/jquery-validation/dist/jquery.validate.js` | 438 | `eventType = "on" + event.type.replace( /^validate/, "" ),` |
| `src/SecureFlow.Web/wwwroot/lib/jquery-validation/dist/jquery.validate.js` | 440 | `if ( settings[ eventType ] && !$( this ).is( settings.ignore ) ) {` |
| `src/SecureFlow.Web/wwwroot/lib/jquery-validation/dist/jquery.validate.js` | 441 | `settings[ eventType ].call( validator, this, event );` |
