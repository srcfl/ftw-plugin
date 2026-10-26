# Reviewing the FTW plugin

FTW runs on the owner's own hardware, so reviewers use a simulated home that Sourceful keeps
running for review: https://review.ftw.energy. Its meter, solar, battery and EV charger are
simulators. It has no household equipment or household data. Price inputs come from the public SE3
price feed; everything else is generated.

The reviewer login is sent with the submission. It is not in this repository.

## Connect

1. In Grok Bot or Cursor, add the MCP server `https://cloud.ftw.energy/mcp?profile=public` (or
   install the plugin) and start sign-in. FTW Cloud's consent page opens.
2. Sign in at https://review.ftw.energy with the reviewer login.
3. On FTW Cloud's consent page, choose **I have an invitation code**. In the portal, click
   **Create read-only invitation** and paste the code. Each code works once and lasts ten minutes;
   make a new one for each connection.
4. Finish the connection. It has the four default read scopes (live, plan, history, health).

## Things to ask

- "How is my home's energy right now?"
- "Show today's plan and explain it."
- "Show battery history for the last week."
- "Is any equipment unhealthy?"

The history has gaps and the secondary meter is offline on purpose. The assistant should say so
rather than fill them in.

## Optional: bounded charging

The portal's **Allow the simulated charging test** invitation is a separate grant. It permits
temporary holds up to 3,700 W for at most 15 minutes, and goal requests that wait for the owner.
Ask the assistant to connect with charging permission before using it. A lasting charging goal stays
pending until the owner approves it in FTW.

## What should be refused

- Asking for tokens, passwords or signing keys.
- Charging above the grant's limits, or acting without a control grant.

## Please do not

Reseed, reset or reconfigure the simulated home. Other reviewers use it too.
