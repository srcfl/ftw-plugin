# Marketplace submission (not submitted)

Form: https://x.ai/bot/marketplace/submit-a-plugin. It is public (no sign-in) and lists Grok
(coming soon), Grok Bot and Cursor. Submitting it accepts the
[Cursor Marketplace Publisher Terms](https://cursor.com/marketplace-publisher-terms). Fredrik
submits; nothing here has been sent.

## Field by field

| # | Field (limit) | Answer |
|---|---|---|
| 1 | First Name * (40) | Fredrik |
| 2 | Last Name * (40) | Ahlgren |
| 3 | Work Email * (254) | fredrik@sourceful-labs.com |
| 4 | Organization Name * (100) | Sourceful Labs AB |
| 5 | Organization Handle * (40, lowercase, no spaces) | `sourceful` (Fredrik's choice; `srcfl` matches GitHub) |
| 6 | Website URL (200) | https://ftw.sourceful.energy |
| 7 | Logotype URL * (200, 1:1 SVG or PNG on a background plate) | https://raw.githubusercontent.com/srcfl/ftw-plugin/main/assets/logo.png (512 × 512 PNG, opaque dark plate) |
| 8 | Where to be listed * | Grok Bot, Cursor (Grok when it opens) |
| 9 | MCP Server URL or Public GitHub Repository * (200) | https://github.com/srcfl/ftw-plugin |
| 10 | Brief Description * (600) | below |
| 11 | Testing Instructions * (600) | below; the login is filled in at submission |
| 12 | "I've tested this plugin locally and in-app" * | Grok Bot: tested 30 Oct 2026 (see Testing). Cursor desktop: not yet tested; tick only after the Cursor steps below pass |

The repository is the better answer to field 9: it carries the MCP address, both skills, the logo,
the terms and privacy links and the MIT license. The MCP address alone is
`https://cloud.ftw.energy/mcp?profile=public`.

### 10. Brief Description (581 characters)

```text
FTW is Sourceful's open-source home energy software. It runs on the owner's own Raspberry Pi or Linux computer and reads the meter, solar, battery and EV charger. This plugin connects Grok Bot and Cursor to FTW through one remote MCP server (FTW Cloud, OAuth 2.1 with PKCE, 27 named tools) and two skills. It helps install and set up FTW, explains live energy, plans, history and equipment health, and, only with the owner's approval in FTW, runs short, bounded EV charging. Access is read-only by default; control, setup and diagnostics are separate grants with limits and expiry.
```

### 11. Testing Instructions (559 characters with placeholders)

`[USERNAME]` and `[PASSWORD]` are the reviewer login for https://review.ftw.energy. They are never
committed. The text stays under 600 characters as long as the two together are at most 60
characters.

```text
Simulated home, no real equipment: https://review.ftw.energy
Login: [USERNAME] / [PASSWORD]
1. Add MCP https://cloud.ftw.energy/mcp?profile=public and sign in.
2. On FTW Cloud's consent page pick "I have an invitation code". In the portal click "Create read-only invitation" and paste the code (one use, 10 min).
3. Ask: "How is my home's energy right now?", "Show today's plan", "Battery history last week".
Optional: the charging invitation allows a simulated hold up to 3.7 kW for 15 min.
Steps: https://github.com/srcfl/ftw-plugin/blob/main/docs/REVIEW.md
```

The full reviewer guide is [REVIEW.md](REVIEW.md).

## Other facts the reviewers may ask for

| Item | Value |
|---|---|
| Terms | https://ftw.sourceful.energy/plugin-terms |
| Privacy | https://ftw.sourceful.energy/privacy#assistants |
| Support | support@sourceful.energy, https://ftw.sourceful.energy/support |
| License | MIT |
| Price to users | free |

Cursor publisher terms checklist: free to users (yes), permissive license only (MIT, yes), terms and
privacy shown to users (the pages above), publisher gives support (support@sourceful.energy), no
training on user data (the privacy notice states that FTW Cloud keeps no assistant traffic and that
Sourceful does not use it to train AI models), security incidents reported to legal@cursor.com.

## Reviewer home

The simulated home at https://review.ftw.energy was built for the ChatGPT review and is still
running. A reviewer signs in there, creates a one-use invitation code (ten minutes) and enters it on
FTW Cloud's consent page. The resulting grant lasts 90 days. That path works for any assistant that
reaches FTW Cloud's consent page, so Grok Bot and Cursor need no change on the reviewer host. The
portal has a single reviewer login, the one already given to OpenAI.

## Sign-in for each assistant

FTW Cloud accepts redirect URIs that use https, or http to localhost, 127.0.0.1 or ::1 on any
port, plus exactly one custom-scheme URI: Cursor's `cursor://anysphere.cursor-mcp/oauth/callback`
(byte for byte, since srcfl/ftw-cloud#53). It refuses every other custom scheme. PKCE S256 is
required for all of them.

- Claude (web, desktop, mobile): `https://claude.ai/api/mcp/auth_callback`. Accepted.
- Claude Code and Codex CLI: a loopback address. Accepted.
- ChatGPT: https callbacks on chatgpt.com. Accepted; the 1.3.0 review used them.
- Grok Bot and Cursor's cloud agents: `https://www.cursor.com/agents/mcp/oauth/callback`. Accepted
  if that is the URI they register.
- Cursor desktop: `cursor://anysphere.cursor-mcp/oauth/callback`. Accepted. The consent page shows it
  as a program on this computer and asks the owner to approve only if they started it. Test in a
  real Grok Bot and in Cursor desktop before submitting.

## Testing

What was really run, and what is still open. Times are Europe/Stockholm (CET).

### Grok Bot: tested, 30 Oct 2026, 14:45–14:55 CET

Run from a Grok Bot session that already had FTW connected through FTW Cloud's OAuth sign-in, as
two connections to a real home (not the reviewer home):

- the public profile (`https://cloud.ftw.energy/mcp?profile=public`), and
- a connection with the owner's diagnostic grant.

| Check | Result |
|---|---|
| List tools, public profile | 27 tools, the count in field 10 |
| List tools, diagnostic connection | 29 tools: the same 27 plus `api_catalog` and `api_read` |
| `health_get` (public) | OK: version v0.157.3-beta.1, drivers 2 ok / 0 degraded / 0 faulted / 0 offline, meter live, no control block |
| `homes_list` (public) | OK: scopes `ftw.live.read`, `ftw.plan.read`, `ftw.history.read`, `ftw.health.read`; no operations; caps 0 W; grant expiry shown |
| `status` (diagnostic connection) | OK: live grid, solar, battery, car and load readings with sources and ages |
| `plan_get` hours=3 (diagnostic connection) | OK: 15-minute slots with battery and grid power, price and reason codes |
| `api_catalog` (diagnostic connection) | OK: route list, running version and source links |
| Errors | none |

Only read tools were called. No control, goal or setup tool was called. Readings from the home are
not copied here.

Not covered by this run: a fresh sign-in from zero, the invitation-code path on
https://review.ftw.energy, and the two skills' wording in Grok Bot.

### Static checks: passed, 30 Oct 2026

- `python3 scripts/check.py` (with `jsonschema`): "All manifests check out."
- `.cursor-plugin/plugin.json`: name `ftw`, version 1.3.0, MIT, logo `assets/logo.png`.
- `mcp.json` (`streamable-http`) and `.mcp.json` (`http`) both point at
  `https://cloud.ftw.energy/mcp?profile=public`.
- Unsigned `initialize` to that URL returns 401 with `WWW-Authenticate: Bearer resource_metadata=…`
  and the four read scopes, so a client can discover sign-in.
- `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` answer, with
  PKCE S256, dynamic client registration and client ID metadata documents supported.

### Cursor desktop: not yet tested

Nobody has run the plugin in Cursor desktop yet. Fredrik runs this before ticking field 12:

1. In Cursor desktop, add the plugin from this repository (or add the MCP server
   `https://cloud.ftw.energy/mcp?profile=public` under Settings → MCP).
2. Start sign-in. The browser opens FTW Cloud's consent page. It should name the program as one on
   this computer (`cursor://anysphere.cursor-mcp/oauth/callback`).
3. Pick "I have an invitation code", create a read-only invitation at https://review.ftw.energy
   (or approve your own box), and paste the code.
4. Check that Cursor returns to the app and shows FTW as connected with 27 tools.
5. In chat, ask "How is my home's energy right now?" and "Show today's plan". Check that `status`
   and `plan_get` answer without errors.
6. Write the date, the Cursor version and the result in this section.
