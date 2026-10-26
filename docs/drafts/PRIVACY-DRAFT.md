> **DRAFT. Not approved, not published.** Proposed addition to the live privacy notice at
> https://ftw.sourceful.energy/privacy (updated 18 October 2026), which already names Cursor among
> assistants but describes the plugin only for ChatGPT/OpenAI. Fredrik must approve before any change
> to the live page. Only the plugin-specific paragraph changes; the rest of the notice stays as is.

## Assistants and the FTW plugin (proposed replacement for the ChatGPT-only paragraph)

The FTW plugin is available for ChatGPT, Grok Bot, Cursor and other assistants that read Agent
Plugins. It sends the assistant the answers to the tools you use, such as current power, battery and
car state, past power readings, plans, device health, and redacted logs and settings. FTW Cloud
receives the tool name and arguments needed for the request; the plugin does not ask for your full
conversation history.

The company that runs your assistant handles what it receives under its own privacy policy and your
account settings: OpenAI for ChatGPT, xAI and Anysphere (Cursor) for Grok Bot, Anysphere for Cursor.
Their retention and deletion controls are separate from FTW's. Ending access in FTW does not delete
an earlier conversation held by the assistant.

The plugin uses named tools and does not offer arbitrary API reads or backup exports. [TO CONFIRM] Sourceful does
not use what the plugin carries to train models, and the plugin files contain no tracking.

Open questions for Fredrik before publishing:
- Confirm the processor wording for Grok Bot (xAI and/or Anysphere).
- Confirm the "no training on user data" sentence matches FTW Cloud practice (Cursor's publisher
  terms require it).
