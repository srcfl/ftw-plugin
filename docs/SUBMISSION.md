# Marketplace submission notes (draft, not submitted)

Form: https://x.ai/bot/marketplace/submit-a-plugin ("Grok (coming soon), Grok Bot, and Cursor").
Fredrik submits; nothing here has been sent.

| Field | Proposed answer | Status |
|---|---|---|
| Name | FTW | ready |
| Organisation | Sourceful Labs AB | ready |
| Work e-mail | ? | Fredrik picks |
| Website | https://ftw.sourceful.energy | live |
| Logo URL | a public PNG URL is needed, e.g. raw GitHub URL of `assets/logo.png` once merged, or a hosted copy on ftw.sourceful.energy | open |
| MCP server URL | https://cloud.ftw.energy/mcp?profile=public | live (401 + OAuth metadata) |
| GitHub repo | https://github.com/srcfl/ftw-plugin | public after merge |
| Description | from `.cursor-plugin/plugin.json` | ready |
| Testing instructions / reviewer login | needs a reviewer account and a simulated home (the ChatGPT review used two simulated homes) | open |
| Terms URL | draft in `docs/drafts/TERMS-DRAFT.md`; live page today is ChatGPT-specific | open |
| Privacy URL | https://ftw.sourceful.energy/privacy (needs the plugin paragraph widened, see draft) | open |
| Support | support@sourceful.energy | confirm |
| Tested locally and in the app | not yet | open |

Cursor publisher terms checklist: free to users (yes), no GPL-family license (MIT, yes), terms and
privacy shown to users (pending), support from publisher (support@sourceful.energy), no training on
user data (confirm).

Unverified: whether FTW Cloud's OAuth (DCR/CIMD) accepts Cursor's redirect URIs
(`https://www.cursor.com/agents/mcp/oauth/callback`, `cursor://...`). Test by adding the server in a
real Grok Bot before submitting.
