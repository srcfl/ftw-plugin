# Anthropic directory submission (not submitted)

Portal: https://claude.ai/directory/manage → Submit new. It takes two kinds of submission, and
Anthropic asks for both when a plugin points at a server you run:

- **MCP connector**: FTW Cloud's remote server (`https://cloud.ftw.energy/mcp?profile=public`).
- **Plugin bundle**: this repository, read from `.claude-plugin/plugin.json`.

A listing reaches claude.ai, Cowork and Claude Code. Anthropic's `claude-plugins-official`
marketplace is separate and takes no portal submissions; it goes through an Anthropic partner
contact. Fredrik submits; nothing here has been sent. Facts below were checked on 30 Oct 2026.

Sources:

- [S1] Submit a connector: https://claude.com/docs/connectors/building/submission
- [S2] Connector review criteria: https://claude.com/docs/connectors/building/review-criteria
- [S3] Authentication for connectors: https://claude.com/docs/connectors/building/authentication
- [S4] Software Directory Policy: https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy
- [S5] Submit a plugin: https://claude.com/docs/plugins/submit
- [S6] Plugin pre-submission checklist: https://claude.com/docs/plugins/pre-submission-checklist
- [S7] Publish a plugin (Claude Code): https://code.claude.com/docs/en/plugins/publish
- [S8] Anthropic's marketplaces: https://code.claude.com/docs/en/plugins/anthropic-marketplaces

Status: ✅ met, from repo or server facts · ⚠️ open, needs work or a decision · ❓ not checked yet

## Who submits

| Requirement | Answer | Status |
|---|---|---|
| Paid Claude plan; on Team/Enterprise an Owner submits [S1][S7] | Which Claude account Sourceful uses is not known | ❓ |
| GitHub account connected on claude.ai, with push rights to the repo [S5] | srcfl/ftw-plugin is public | ❓ (connect at submission) |
| Agree to the Directory Terms and Policy, maintain security, respond to security issues [S1][S4] | Support: support@sourceful.energy | ⚠️ Fredrik reads and accepts |

## 1. MCP connector (FTW Cloud)

| Requirement | Our answer | Status |
|---|---|---|
| Remote, reachable over `https://` [S1] | `https://cloud.ftw.energy/mcp?profile=public` | ✅ |
| Streamable HTTP transport [S4 §5F] | `mcp.json` declares `streamable-http` | ✅ |
| OAuth 2.0 for authenticated services, 401 discovery metadata [S1][S3][S4 §5D] | Unsigned call returns 401 with `resource_metadata`; authorization server metadata lists PKCE S256, `/oauth/register` (DCR) and client ID metadata documents | ✅ |
| Claude's callback accepted | `https://claude.ai/api/mcp/auth_callback` is accepted (see SUBMISSION.md, "Sign-in for each assistant") | ✅ |
| Every tool has `title` and `readOnlyHint` / `destructiveHint` [S1][S4 §5E] | srcfl/ftw-cloud `internal/mcp/tools.go` sends `title`, `readOnlyHint` and `destructiveHint` for each tool | ✅ in source; ⚠️ check the portal's Tools step shows no flags |
| Split safe and unsafe actions into separate tools [S2] | Reads, `ev_charge_now`, `goal_request` / `car_goal_request` and `setup_*` are separate tools | ✅ |
| Tool names at most 64 characters [S4 §5C] | Longest is `measurement_diagnostics` (23) | ✅ |
| Clear errors, frugal with tokens [S4 §5A–B] | Tools take `hours`, `points`, `lines`, `limit` bounds | ⚠️ reviewer judgment |
| Tested in Claude as a custom connector, every tool called [S1 step 8] | Tested in Grok Bot (see SUBMISSION.md, Testing); not yet in Claude | ⚠️ |
| Reviewer test account, fully populated [S1][S4 D] | Simulated home at https://review.ftw.energy with invitation codes (see REVIEW.md); login only in the portal, never in git | ✅ (Fredrik enters the login) |
| Three or more working example prompts [S4 E] | "How is my home's energy right now?", "Show today's plan", "Battery history last week" (REVIEW.md) | ✅ |
| Own the endpoint and domain [S4 F] | cloud.ftw.energy and ftw.sourceful.energy are Sourceful's | ✅ |
| Documentation URL [S1 step 3] | https://ftw.sourceful.energy, plus this repository | ✅ |
| Privacy policy URL [S1 step 3] | https://ftw.sourceful.energy/privacy#assistants | ✅ |
| Support contact [S1 step 3] | support@sourceful.energy | ✅ |
| Icon [S1 step 3] | `assets/icon.png`, `assets/logo.png` | ✅ |
| Listing: name ≤100, one-liner ≤200, description ≤2,000, 1–5 categories, slug (permanent) [S1 step 3] | Name "FTW"; one-liner: plugin.json `description`; slug `ftw` proposed | ⚠️ description and categories not written; slug is Fredrik's call |
| Use cases, prerequisites, reads/writes [S1 step 4] | Needs an FTW box at home and the owner's approval; reads by default, writes (short charging, requests) only with a separate grant | ⚠️ write out |
| Company and primary contact [S1 step 5] | Sourceful Labs AB, fredrik@sourceful-labs.com | ✅ |
| Authentication method [S1 step 6] | Required; OAuth with DCR / client ID metadata (no Anthropic-held client) | ✅ |
| Data handling: own API, health data, sponsored content [S1 step 7] | Own API (FTW Cloud and the owner's box); no health data; no sponsored content | ✅ |
| Seven compliance acknowledgments, incl. financial transactions and prompt injection [S1 step 9] | No purchases or payments; tool descriptions mark box data as data, not instructions | ⚠️ Fredrik reads and ticks |
| Allowed link URIs (only if `ui/open-link` is used) [S1] | Not used | ✅ n/a |
| MCP App screenshots [S1] | Not an MCP App | ✅ n/a |

## 2. Plugin bundle (this repository)

| Requirement | Our answer | Status |
|---|---|---|
| Folder with `.claude-plugin/plugin.json` [S6] | Repository root | ✅ |
| Name: lowercase, digits, hyphens, ≤64, not reserved, not taken [S6] | `ftw` | ✅ pattern; ❓ whether the name is free; a short name may be held as look-alike |
| `description`, `author`, `version` set [S6] | Set, version 1.3.0 | ✅ |
| README ≥40 words outside code blocks [S6] | README.md, 664 words in total | ✅ |
| License [S6] | `LICENSE` (MIT) and `license` in plugin.json | ✅ |
| `.mcp.json` valid; remote server has `type` http/sse/ws and an `https://` URL [S6] | `{"type":"http","url":"https://cloud.ftw.energy/mcp?profile=public"}` | ✅ |
| No credentials in any file [S6] | None; the reviewer login lives outside git | ✅ |
| No launchers, lockfiles, hooks or local server commands [S6] | None | ✅ |
| No `.DS_Store` and similar, no symlinks, submodules or LFS [S6] | None found | ✅ |
| Non-image files under 256 KiB, ≤512 files, only text/PNG/JPEG/GIF/WebP/SVG/fonts [S6] | Text and PNG only, well under 512 files | ✅ |
| Skills: valid YAML front matter with a text `description` [S6] | Two skills; `scripts/check.py` checks name and description | ✅ |
| README describes everything the plugin runs, sends or fetches (security scan) [S6] | README names FTW Cloud as the only server | ⚠️ re-read with the scan in mind |
| `claude plugin validate ./ --strict` passes [S5][S7] | Not run: Claude Code is not installed on the box | ❓ |
| Loaded and tried on each surface (claude.ai, Cowork, Claude Code) [S6] | Not done | ⚠️ |
| Extra folders shipped to users | `openai/`, `.cursor-plugin/`, `.agents/` and `docs/` sit in the plugin folder and ship with it | ⚠️ allowed by the checks above; decide if a subfolder is cleaner |

## Gaps to close before submitting

1. Choose the Claude account (paid plan, Owner role on Team/Enterprise) and connect GitHub on claude.ai.
2. Add FTW as a custom connector in Claude, sign in through the reviewer home, call each read tool
   and record it, as was done for Grok Bot.
3. Run `claude plugin validate ./ --strict`, then the portal's Validate, and fix any finding.
4. Write the connector listing description (≤2,000 characters), the categories and the use-case text.
5. Decide whether to submit the connector first, then the plugin paired with it, as [S1] and [S5]
   suggest.
6. Read and accept the Directory Terms and the seven acknowledgments.

Escalation address for a stuck connector submission: mcp-review@anthropic.com [S1].
