1 · Context
    • Repo root = Indus/
    • root-app/      ← Android sensor publisher (Kotlin)  
    • client-app/    ← Android dashboard (Kotlin)  
    • cloud/         ← FastAPI backend (Python 3.12)  
    • contracts/     ← proto + OpenAPI (source-of-truth)  
    • devops/compose/← docker-compose, Tilt, scripts  
    • .cursor/       ← AI rules & ignore

2 · MESS Principles
    • Modular – code in one module may only call others via generated stubs in contracts/ (gRPC, MQTT 5, GraphQL).
    • Empirical – favour measurable answers: lint configs, benchmark commands, CI matrix snippets.
    • Secure – never print real tokens; instruct to use ENV VARS or Vault.
    • Scalable – design for selective CI builds; reference devops/compose/docker-compose.yml.
3 · Prompt Rules (for Cursor / Gemini)
DO
    • Start every request with the target path (root-app/…) and keep edits inside it.
    • Reference shared APIs by relative path (@contracts/v1/telemetry.proto).
    • Deliver guidance in ≤ 2 steps when the user asks for chunks.
    • Cite commit commands (git add …, git status) after repo-changing steps.
DON’T
    • Suggest direct imports across folders.
    • Include build artefacts (build/, node_modules/, *.apk) in code or examples.
    • Reveal secrets or hard-code passwords.
4 · Answer Style
    • Concise, action-oriented, engineer-friendly.
    • Use fenced code blocks (```bash, ```python). No tables unless critical.
    • Insert absolute dates if clarifying “today / yesterday”.
    • One‐sentence intro, then bullets or code.

5 · Default Tech Stack
    • Python 3.12 + FastAPI · Kotlin + Gradle 8 · Docker-Compose v2 · protobuf / gRPC · MQTT 5.
    • Assume VS Code-based Cursor environment and Git-based CI (GitHub Actions).
    • Always check these rules before responding; they are the contract for AI assistance on the Indus project.
