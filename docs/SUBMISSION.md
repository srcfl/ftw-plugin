# Marketplace submission notes (not submitted)

Form: https://x.ai/bot/marketplace/submit-a-plugin ("Grok (coming soon), Grok Bot, and Cursor").
Fredrik submits; nothing here has been sent.

| Field | Proposed answer | Status |
|---|---|---|
| Name | FTW | ready |
| Organisation | Sourceful Labs AB | ready |
| Work e-mail | ? | Fredrik picks |
| Website | https://ftw.sourceful.energy | live |
| Logo URL | https://raw.githubusercontent.com/srcfl/ftw-plugin/main/assets/logo.png (512 × 512 PNG) | live after merge |
| MCP server URL | https://cloud.ftw.energy/mcp?profile=public | live (401 + OAuth metadata) |
| GitHub repo | https://github.com/srcfl/ftw-plugin | public |
| Description | from `.cursor-plugin/plugin.json` | ready |
| Testing instructions / reviewer login | needs a reviewer account and a simulated home (the ChatGPT review used two simulated homes) | open |
| Terms URL | https://ftw.sourceful.energy/plugin-terms | live after the ftw-web merge |
| Privacy URL | https://ftw.sourceful.energy/privacy#assistants | live |
| Support | support@sourceful.energy, https://ftw.sourceful.energy/support | ready |
| Tested locally and in the app | not yet | open |

Cursor publisher terms checklist: free to users (yes), no GPL-family license (MIT, yes), terms and
privacy shown to users (the pages above), support from the publisher (support@sourceful.energy), no
training on user data (the privacy notice states that FTW Cloud keeps no assistant traffic and that
Sourceful does not use it to train AI models).

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
