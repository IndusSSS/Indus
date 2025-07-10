# CHANGELOG.md

## v0.1

- Added contracts/openapi-generated Kotlin DTO module (OpenAPI Generator, Moshi, Java8 date).
- Updated root settings.gradle.kts to include :contracts:openapi-generated.
- Patched root-app/build.gradle.kts to depend on :contracts:openapi-generated.
- All DTO imports in root-app now use solutions.smartsecurity.contracts.health.*

### Cross-module changes
- Added contracts/health.yml OpenAPI spec for health beacon endpoint.
- Generated DTOs in contracts/openapi-generated for use by all modules. 