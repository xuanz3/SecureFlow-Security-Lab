using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using SecureFlow.Web.Models;

namespace SecureFlow.Web.Data;

public sealed class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext(options)
{
    public DbSet<Ticket> Tickets => Set<Ticket>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity<Ticket>(entity =>
        {
            entity.HasKey(ticket => ticket.Id);
            entity.HasIndex(ticket => new { ticket.OwnerId, ticket.CreatedAtUtc });
            entity.Property(ticket => ticket.Title).HasMaxLength(120);
            entity.Property(ticket => ticket.Description).HasMaxLength(4000);
            entity.Property(ticket => ticket.OwnerId).HasMaxLength(450);
        });
    }
}
