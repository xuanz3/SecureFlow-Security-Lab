using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using SecureFlow.Web.Models;

namespace SecureFlow.Web.Controllers;

public sealed class AccountController(
    SignInManager<IdentityUser> signInManager,
    UserManager<IdentityUser> userManager,
    ILogger<AccountController> logger) : Controller
{
    [AllowAnonymous]
    [HttpGet]
    public IActionResult Login(string? returnUrl = null) =>
        View(new LoginViewModel { ReturnUrl = returnUrl });

    [AllowAnonymous]
    [HttpPost]
    [ValidateAntiForgeryToken]
    [EnableRateLimiting("login")]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var user = await userManager.FindByEmailAsync(model.Email);
        if (user is null)
        {
            logger.LogWarning(
                "SecurityAudit LoginFailure EmailHash={EmailHash} CorrelationId={CorrelationId}",
                model.Email.ToUpperInvariant().GetHashCode(),
                HttpContext.TraceIdentifier);
            ModelState.AddModelError(string.Empty, "Invalid sign-in attempt.");
            return View(model);
        }

        var result = await signInManager.PasswordSignInAsync(
            user,
            model.Password,
            model.RememberMe,
            lockoutOnFailure: true);

        if (!result.Succeeded)
        {
            logger.LogWarning(
                "SecurityAudit LoginFailure UserId={UserId} LockedOut={LockedOut} CorrelationId={CorrelationId}",
                user.Id,
                result.IsLockedOut,
                HttpContext.TraceIdentifier);
            ModelState.AddModelError(string.Empty, "Invalid sign-in attempt.");
            return View(model);
        }

        logger.LogInformation(
            "SecurityAudit LoginSuccess UserId={UserId} CorrelationId={CorrelationId}",
            user.Id,
            HttpContext.TraceIdentifier);

        if (!string.IsNullOrWhiteSpace(model.ReturnUrl) && Url.IsLocalUrl(model.ReturnUrl))
        {
            return LocalRedirect(model.ReturnUrl);
        }

        return RedirectToAction("Index", "Tickets");
    }

    [Authorize]
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Logout()
    {
        var userId = userManager.GetUserId(User);
        await signInManager.SignOutAsync();
        logger.LogInformation(
            "SecurityAudit Logout UserId={UserId} CorrelationId={CorrelationId}",
            userId,
            HttpContext.TraceIdentifier);
        return RedirectToAction("Index", "Home");
    }

    [AllowAnonymous]
    public IActionResult AccessDenied() => View();
}
