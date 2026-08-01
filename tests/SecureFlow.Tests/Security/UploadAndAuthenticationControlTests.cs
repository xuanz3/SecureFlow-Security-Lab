using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using SecureFlow.Web.Controllers;
using SecureFlow.Web.Security;

namespace SecureFlow.Tests.Security;

public sealed class UploadAndAuthenticationControlTests
{
    [Fact]
    public void LoginLimiterPartitionsBySourceAddress()
    {
        var first = new DefaultHttpContext();
        first.Connection.RemoteIpAddress = IPAddress.Parse("192.0.2.10");

        var second = new DefaultHttpContext();
        second.Connection.RemoteIpAddress = IPAddress.Parse("192.0.2.11");

        Assert.NotEqual(
            LoginRateLimitPartitioner.GetPartitionKey(first),
            LoginRateLimitPartitioner.GetPartitionKey(second));
    }

    [Fact]
    public void LoginLimiterNormalisesIpv4MappedAddress()
    {
        var context = new DefaultHttpContext();
        context.Connection.RemoteIpAddress =
            IPAddress.Parse("::ffff:192.0.2.10");

        Assert.Equal(
            "192.0.2.10",
            LoginRateLimitPartitioner.GetPartitionKey(context));
    }

    [Fact]
    public void UploadEndpointLimitsRequestBeforeModelBinding()
    {
        var method = typeof(TicketsController)
            .GetMethod(nameof(TicketsController.UploadAttachment));

        Assert.NotNull(method);

        var requestLimit = Assert.Single(
            method!.GetCustomAttributes(
                typeof(RequestSizeLimitAttribute),
                inherit: true)
            .Cast<RequestSizeLimitAttribute>());

        var formLimit = Assert.Single(
            method.GetCustomAttributes(
                typeof(RequestFormLimitsAttribute),
                inherit: true)
            .Cast<RequestFormLimitsAttribute>());

        Assert.Equal(
            FileUploadValidator.MaximumRequestBytes,
            requestLimit.Bytes);
        Assert.Equal(
            FileUploadValidator.MaximumRequestBytes,
            formLimit.MultipartBodyLengthLimit);
    }

    [Fact]
    public void ContentSecurityPolicyDisallowsInlineStyles()
    {
        Assert.DoesNotContain(
            "'unsafe-inline'",
            SecurityHeadersMiddleware.ContentSecurityPolicy,
            StringComparison.Ordinal);
        Assert.Contains(
            "style-src 'self'",
            SecurityHeadersMiddleware.ContentSecurityPolicy,
            StringComparison.Ordinal);
    }
}
