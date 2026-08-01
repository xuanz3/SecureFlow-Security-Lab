# Phase 5 Authorisation Retest Method

## Why Phase 4 showed HTTP 200

SecureFlow is a browser-oriented MVC application using ASP.NET Core Identity
cookies. When an authenticated user lacks permission, the cookie handler can
redirect the browser to `/Account/AccessDenied`. The final denial page returns
HTTP 200 because the page itself rendered successfully.

A client that follows redirects and records only the final status can therefore
misclassify a correctly denied request as HTTP 200 access.

## Correct validation method

The Phase 5 retest performs two checks for each denied request:

1. Inspect the raw response without following redirects.
2. Follow the browser flow and verify that the final page is the access-denied
   page and does not contain protected resource content.

Accepted raw denial forms are:

- HTTP 403, or
- HTTP 301/302/303/307/308 with a Location pointing to
  `/Account/AccessDenied`.

## Code controls retained

- `TicketsController` requires authentication.
- Ticket read and modification actions call `ITicketAccessService`.
- The service compares the authenticated user identifier with `Ticket.OwnerId`
  using ordinal comparison.
- Administrators are explicitly allowed by the same service.
- `AdminController` requires the `Admin` role.

The secure application logic is retained. Phase 5 adds regression tests and a
correct retest method rather than altering a control that was already working.
