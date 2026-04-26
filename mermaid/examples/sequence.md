# Mermaid Example — Sequence Diagram

OAuth 2.0 authorization-code flow with PKCE. Shows participants, activations, alt/opt blocks, notes, and async returns.

## Source

````markdown
```mermaid
sequenceDiagram
  autonumber
  actor U as User
  participant B as Browser
  participant C as Client App
  participant A as Auth Server
  participant R as Resource API

  U->>B: click "Sign in"
  B->>C: GET /login
  C->>C: generate code_verifier + code_challenge
  C->>B: 302 to /authorize?code_challenge=...
  B->>A: GET /authorize
  A->>U: prompt credentials + consent
  U->>A: submit
  alt success
    A->>B: 302 to /callback?code=XYZ
    B->>C: GET /callback?code=XYZ
    C->>A: POST /token (code, code_verifier)
    A-->>C: { access_token, refresh_token }
    Note right of C: token in memory only
    C->>R: GET /me  (Authorization: Bearer)
    R-->>C: user profile JSON
    C-->>B: render profile
  else denied
    A->>B: 302 to /callback?error=access_denied
    B->>C: render error page
  end

  loop refresh every 50min
    C->>A: POST /token (refresh_token)
    A-->>C: new access_token
  end
```
````

## Rendered

```mermaid
sequenceDiagram
  autonumber
  actor U as User
  participant B as Browser
  participant C as Client App
  participant A as Auth Server
  participant R as Resource API

  U->>B: click "Sign in"
  B->>C: GET /login
  C->>C: generate code_verifier + code_challenge
  C->>B: 302 to /authorize?code_challenge=...
  B->>A: GET /authorize
  A->>U: prompt credentials + consent
  U->>A: submit
  alt success
    A->>B: 302 to /callback?code=XYZ
    B->>C: GET /callback?code=XYZ
    C->>A: POST /token (code, code_verifier)
    A-->>C: { access_token, refresh_token }
    Note right of C: token in memory only
    C->>R: GET /me  (Authorization: Bearer)
    R-->>C: user profile JSON
    C-->>B: render profile
  else denied
    A->>B: 302 to /callback?error=access_denied
    B->>C: render error page
  end

  loop refresh every 50min
    C->>A: POST /token (refresh_token)
    A-->>C: new access_token
  end
```

## Syntax cheat sheet

| Symbol | Meaning |
|---|---|
| `->>` | Solid arrow — synchronous request |
| `-->>` | Dashed arrow — return / response |
| `-x` | Lost / failed message |
| `actor X as Name` | Stick-figure participant |
| `participant X as Name` | Box participant |
| `Note right of X: text` | Annotation; also `left of`, `over X,Y` |
| `alt / else / end` | Conditional branches |
| `opt / end` | Optional branch (single, no else) |
| `loop label / end` | Repeated section |
| `par / and / end` | Parallel sections |
| `autonumber` | Auto-number every message |
| `activate X` / `deactivate X` | Manual lifeline activation (auto on by default) |
