using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SecureFlow.Web.Data;
using SecureFlow.Web.Security;

namespace SecureFlow.Web.Controllers;

[Authorize(Roles = AppRoles.Admin)]
public sealed class AdminController(ApplicationDbContext dbContext) : Controller
{
    public async Task<IActionResult> Index()
    {
        var tickets = await dbContext.Tickets
            .AsNoTracking()
            .OrderByDescending(ticket => ticket.CreatedAtUtc)
            .ToListAsync();

        return View(tickets);
    }
}
