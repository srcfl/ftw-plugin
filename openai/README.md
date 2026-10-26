# ChatGPT and Codex package

`package/` is FTW 1.3.0 as submitted to OpenAI's plugin directory on 18 October 2026. Its 14 files
match the archive in OpenAI's portal byte for byte; `SHA256SUMS` records them, and
`scripts/check.py` fails if any file changes.

It differs from the shared plugin at the repository root in four ways: the skills address ChatGPT,
each skill has `agents/openai.yaml`, `plugin.json` carries OpenAI's review cases and release notes,
and `mcp.json` names the server `ftw-cloud` with OpenAI's OAuth settings (dynamic client
registration, four read scopes).

Build the upload ZIP with:

    python3 scripts/build-chatgpt-package.py

Change `package/` only for a new OpenAI submission. Then raise the version, update `SHA256SUMS` and
consider pointing `termsOfServiceURL` at https://ftw.sourceful.energy/plugin-terms. The reviewed
1.3.0 package points at /chatgpt-terms, which stays online.
