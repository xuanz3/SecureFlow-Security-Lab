using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using SecureFlow.Web.Security;

namespace SecureFlow.Web.Data;

public static class DbInitializer
{
    public static async Task InitializeAsync(IServiceProvider services, IConfiguration configuration)
    {
        await using var scope = services.CreateAsyncScope();
        var scopedServices = scope.ServiceProvider;
        var dbContext = scopedServices.GetRequiredService<ApplicationDbContext>();
        var roleManager = scopedServices.GetRequiredService<RoleManager<IdentityRole>>();
        var userManager = scopedServices.GetRequiredService<UserManager<IdentityUser>>();
        var logger = scopedServices.GetRequiredService<ILoggerFactory>()
            .CreateLogger("SecureFlow.Database");

        await dbContext.Database.MigrateAsync();

        foreach (var role in new[] { AppRoles.Admin, AppRoles.User })
        {
            if (!await roleManager.RoleExistsAsync(role))
            {
                var roleResult = await roleManager.CreateAsync(new IdentityRole(role));
                EnsureSuccess(roleResult, $"create role {role}");
            }
        }

        await SeedUserAsync(
            userManager,
            configuration["SeedUsers:AdminEmail"],
            configuration["SeedUsers:AdminPassword"],
            AppRoles.Admin);

        await SeedUserAsync(
            userManager,
            configuration["SeedUsers:AliceEmail"],
            configuration["SeedUsers:AlicePassword"],
            AppRoles.User);

        await SeedUserAsync(
            userManager,
            configuration["SeedUsers:BobEmail"],
            configuration["SeedUsers:BobPassword"],
            AppRoles.User);

        logger.LogInformation("Database migration and fictional development identity seeding completed.");
    }

    private static async Task SeedUserAsync(
        UserManager<IdentityUser> userManager,
        string? email,
        string? password,
        string role)
    {
        if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
        {
            return;
        }

        var existing = await userManager.FindByEmailAsync(email);
        if (existing is not null)
        {
            if (!await userManager.IsInRoleAsync(existing, role))
            {
                EnsureSuccess(await userManager.AddToRoleAsync(existing, role), $"assign {role}");
            }

            return;
        }

        var user = new IdentityUser
        {
            UserName = email,
            Email = email,
            EmailConfirmed = true
        };

        EnsureSuccess(await userManager.CreateAsync(user, password), $"create {email}");
        EnsureSuccess(await userManager.AddToRoleAsync(user, role), $"assign {role}");
    }

    private static void EnsureSuccess(IdentityResult result, string operation)
    {
        if (result.Succeeded)
        {
            return;
        }

        var errors = string.Join("; ", result.Errors.Select(error => error.Description));
        throw new InvalidOperationException($"Failed to {operation}: {errors}");
    }
}
