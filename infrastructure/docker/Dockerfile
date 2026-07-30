FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
WORKDIR /src

COPY SecureFlow.sln ./
COPY Directory.Build.props ./
COPY src/SecureFlow.Web/SecureFlow.Web.csproj src/SecureFlow.Web/
COPY src/SecureFlow.Web/packages.lock.json src/SecureFlow.Web/
RUN dotnet restore src/SecureFlow.Web/SecureFlow.Web.csproj --locked-mode

COPY src/SecureFlow.Web/ src/SecureFlow.Web/
RUN dotnet publish src/SecureFlow.Web/SecureFlow.Web.csproj \
    --configuration Release \
    --no-restore \
    --output /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=build --chown=appuser:appgroup /app/publish .
RUN mkdir -p /app/App_Data/uploads && chown -R appuser:appgroup /app/App_Data
USER appuser
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "SecureFlow.Web.dll"]
