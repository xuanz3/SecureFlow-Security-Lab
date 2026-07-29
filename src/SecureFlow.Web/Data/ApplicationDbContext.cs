using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using SecureFlow.Web.Models;

namespace SecureFlow.Web.Data;

public sealed class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext(options)
{
    public DbSet<Ticket> Tickets => Set<Ticket>();
    public DbSet<TicketAttachment> TicketAttachments => Set<TicketAttachment>();

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

        builder.Entity<TicketAttachment>(entity =>
        {
            entity.HasKey(attachment => attachment.Id);
            entity.HasIndex(attachment => attachment.TicketId);
            entity.Property(attachment => attachment.OriginalName).HasMaxLength(255);
            entity.Property(attachment => attachment.StoredName).HasMaxLength(80);
            entity.Property(attachment => attachment.ContentType).HasMaxLength(100);
            entity.Property(attachment => attachment.UploadedByUserId).HasMaxLength(450);
            entity.HasOne(attachment => attachment.Ticket)
                .WithMany()
                .HasForeignKey(attachment => attachment.TicketId)
                .OnDelete(DeleteBehavior.Cascade);
        });
    }
}
