#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
project="$repo_root/src/SecureFlow.Web/SecureFlow.Web.csproj"

random_password() {
  printf 'Sf!%sAa9' "$(openssl rand -hex 10)"
}

postgres_password="$(random_password)"
admin_password="$(random_password)"
alice_password="$(random_password)"
bob_password="$(random_password)"

cat > "$repo_root/.env" <<EOF
POSTGRES_PASSWORD=$postgres_password
SEED_ADMIN_EMAIL=admin@example.test
SEED_ADMIN_PASSWORD=$admin_password
SEED_ALICE_EMAIL=alice@example.test
SEED_ALICE_PASSWORD=$alice_password
SEED_BOB_EMAIL=bob@example.test
SEED_BOB_PASSWORD=$bob_password
EOF

dotnet user-secrets init --project "$project" >/dev/null 2>&1 || true
dotnet user-secrets set "ConnectionStrings:DefaultConnection" \
  "Host=localhost;Port=5432;Database=secureflow;Username=secureflow;Password=$postgres_password" \
  --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:AdminEmail" "admin@example.test" --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:AdminPassword" "$admin_password" --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:AliceEmail" "alice@example.test" --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:AlicePassword" "$alice_password" --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:BobEmail" "bob@example.test" --project "$project" >/dev/null
dotnet user-secrets set "SeedUsers:BobPassword" "$bob_password" --project "$project" >/dev/null

cat <<EOF
Local development secrets created.

Admin: admin@example.test
Admin password: $admin_password
Alice: alice@example.test
Alice password: $alice_password
Bob: bob@example.test
Bob password: $bob_password

These values are stored only in .env and .NET user-secrets. They are not committed.
EOF
