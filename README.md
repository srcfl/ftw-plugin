# FTW plugin

[FTW](https://ftw.sourceful.energy) is Sourceful's open-source home energy software. You run it
yourself, on a Raspberry Pi or another Linux computer at home, and it reads your meter, solar,
battery and EV charger, keeps the history and plans when to charge and discharge. The source is at
[srcfl/ftw](https://github.com/srcfl/ftw).

This plugin connects an AI assistant (Grok Bot, Cursor, and other apps that read Agent Plugins) to
FTW. It helps you install and set up FTW, explains your home's energy flow, plans, history and
equipment health, and, only with your approval in FTW, runs short, bounded EV charging.

## What it holds

- One remote MCP server, `https://cloud.ftw.energy/mcp?profile=public` (FTW Cloud), with 27 named
  tools. Sign-in is OAuth 2.1 with PKCE; the app registers itself (client ID metadata document or
  dynamic client registration). No keys or secrets live in this plugin.
- Two skills:
  - `ftw-setup-guide`: install, migrate, commission and connect FTW, even before any home is
    connected.
  - `ftw-energy-assistant`: read live energy, plans, history and health; diagnose problems;
    bounded charging and owner-approved goal requests; and the safety limits that apply.
- FTW's logo.

## How access works

Nothing reaches the assistant until the home's owner approves it in FTW, on the box's own page or in
the FTW app. Default access is four read scopes (live, plan, history, health). Control, setup and
diagnostics are separate grants with their own limits and expiry. Lasting changes, such as a new
charging goal, wait for the owner to confirm in FTW. The owner can end access in FTW at any time.
The public connection has no arbitrary API reader, backup export or SSH access, and cannot return
tokens or signing keys. Core on the box keeps final control and its safety checks.

## Install

- **Grok Bot and Cursor:** from the Cursor Marketplace, once listed. Until then, add a custom MCP
  server named `ftw` at `https://cloud.ftw.energy/mcp?profile=public`.
- **Locally in Cursor:** copy this repository to `~/.cursor/plugins/local/ftw` and reload the window.

## Network and data

The plugin talks only to `https://cloud.ftw.energy`. What FTW Cloud handles and keeps is in the
[privacy notice](https://ftw.sourceful.energy/privacy). What you let the assistant read goes to the
company that runs the assistant, under its own privacy policy.

Support: support@sourceful.energy.

## Files

| File | Read by |
|---|---|
| `plugin.json`, `mcp.json` | Agent Plugins format (Cursor, Grok Bot, VS Code and others) |
| `.cursor-plugin/plugin.json` | Cursor Plugins format (Cursor Marketplace, Grok Bot) |
| `.claude-plugin/plugin.json`, `.mcp.json` | Claude Code, Grok Build |
| `skills/` | all of them |
| `assets/` | logo (512 px) and icon (96 px) |

## License

MIT, see [LICENSE](LICENSE). FTW itself and FTW Cloud keep their own licenses; this repository holds
only the plugin files, no FTW code.
