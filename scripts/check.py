#!/usr/bin/env python3
"""Check every manifest in this repository.

Run from the repository root: python3 scripts/check.py
Needs the jsonschema package. Fetches the Agent Plugins schemas from agent-plugins.org.
"""
import hashlib
import json
import pathlib
import re
import sys
import urllib.request

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMAS = "https://agent-plugins.org/schemas/1.0.0/{}.schema.json"
MCP_URL = "https://cloud.ftw.energy/mcp?profile=public"
errors = []


def fail(msg):
    errors.append(msg)


def load(rel):
    try:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fail(f"{rel}: {e}")
        return None


def schema(kind):
    with urllib.request.urlopen(SCHEMAS.format(kind), timeout=20) as r:
        return json.load(r)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_skills(skills_dir, banned):
    names = []
    for skill in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        md = skill / "SKILL.md"
        if not md.exists():
            fail(f"{skill.relative_to(ROOT)}: no SKILL.md")
            continue
        fm = frontmatter(md)
        if fm.get("name") != skill.name:
            fail(f"{md.relative_to(ROOT)}: name {fm.get('name')!r} does not match folder")
        if not fm.get("description"):
            fail(f"{md.relative_to(ROOT)}: no description")
        names.append(skill.name)
        for f in skill.rglob("*.md"):
            text = f.read_text(encoding="utf-8")
            for link in re.findall(r"\]\((references/[^)#]+)\)", text):
                if not (skill / link).exists():
                    fail(f"{f.relative_to(ROOT)}: broken link {link}")
            if banned and re.search(banned, text, re.I):
                fail(f"{f.relative_to(ROOT)}: host-specific wording ({banned}) in a shared skill")
    return names


def main():
    plugin_schema, mcp_schema = schema("plugin"), schema("mcp")

    root_plugin = load("plugin.json")
    root_mcp = load("mcp.json")
    oa_plugin = load("openai/package/plugin.json")
    oa_mcp = load("openai/package/mcp.json")
    cursor = load(".cursor-plugin/plugin.json")
    claude = load(".claude-plugin/plugin.json")
    claude_mk = load(".claude-plugin/marketplace.json")
    codex_mk = load(".agents/plugins/marketplace.json")
    dot_mcp = load(".mcp.json")
    if errors:
        return

    # OpenAI's package adds an "extensions" object to its MCP server for OAuth settings. The
    # Agent Plugins schema has no such field, so check that file with it set aside. The shared
    # mcp.json carries no extensions and must pass the schema as is.
    oa_mcp_core = {**oa_mcp, "mcpServers": {
        k: {f: v for f, v in s.items() if f != "extensions"} for k, s in oa_mcp["mcpServers"].items()}}
    for rel, doc, sch in [
        ("plugin.json", root_plugin, plugin_schema),
        ("mcp.json", root_mcp, mcp_schema),
        ("openai/package/plugin.json", oa_plugin, plugin_schema),
        ("openai/package/mcp.json", oa_mcp_core, mcp_schema),
    ]:
        for e in jsonschema.Draft202012Validator(sch).iter_errors(doc):
            fail(f"{rel}: {e.message} at {'/'.join(map(str, e.path))}")

    # One name and version for the shared plugin.
    for rel, doc in [("plugin.json", root_plugin), (".cursor-plugin/plugin.json", cursor),
                     (".claude-plugin/plugin.json", claude)]:
        if doc.get("name") != "ftw":
            fail(f"{rel}: name must be ftw")
        if doc.get("version") != root_plugin.get("version"):
            fail(f"{rel}: version {doc.get('version')} differs from plugin.json")
    entry = claude_mk["plugins"][0]
    if entry.get("name") != "ftw" or entry.get("source") != "./":
        fail(".claude-plugin/marketplace.json: entry must be ftw at ./")
    if entry.get("version") != root_plugin.get("version"):
        fail(".claude-plugin/marketplace.json: version differs from plugin.json")
    centry = codex_mk["plugins"][0]
    if centry.get("name") != "ftw" or centry.get("source", {}).get("path") != "./":
        fail(".agents/plugins/marketplace.json: entry must be ftw at ./")

    # Every MCP file points at the same public FTW Cloud endpoint.
    for rel, doc in [("mcp.json", root_mcp), (".mcp.json", dot_mcp), ("openai/package/mcp.json", oa_mcp)]:
        urls = {s.get("url") for s in doc["mcpServers"].values()}
        if urls != {MCP_URL}:
            fail(f"{rel}: MCP URL must be {MCP_URL}, got {urls}")

    # Files the manifests name exist.
    iface = root_plugin["extensions"]["com.openai"]["interface"]
    for rel in [cursor.get("logo"), iface["logo"], iface["composerIcon"]]:
        if not (ROOT / rel).is_file():
            fail(f"missing file {rel}")
    oa_iface = oa_plugin["extensions"]["com.openai"]["interface"]
    for rel in [oa_iface["logo"], oa_iface["composerIcon"]]:
        if not (ROOT / "openai/package" / rel).is_file():
            fail(f"missing file openai/package/{rel}")

    # The ChatGPT package stays byte for byte what OpenAI reviewed.
    pkg = ROOT / "openai/package"
    listed = {}
    for line in (ROOT / "openai/SHA256SUMS").read_text().splitlines():
        digest, rel = line.split(maxsplit=1)
        listed[rel.removeprefix("./")] = digest
    present = {str(p.relative_to(pkg)) for p in pkg.rglob("*") if p.is_file()}
    if present != set(listed):
        fail(f"openai/package files differ from SHA256SUMS: {sorted(present ^ set(listed))}")
    for rel, digest in listed.items():
        p = pkg / rel
        if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            fail(f"openai/package/{rel}: changed since the reviewed 1.3.0 package")

    shared = check_skills(ROOT / "skills", r"chatgpt|openai|codex")
    reviewed = check_skills(pkg / "skills", None)
    if shared != reviewed:
        fail(f"skills differ: shared {shared}, ChatGPT package {reviewed}")

    # No secrets.
    for p in ROOT.rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.suffix in {".json", ".md", ".yaml", ".yml", ".py"}:
            t = p.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)", t):
                fail(f"{p.relative_to(ROOT)}: looks like a secret")


if __name__ == "__main__":
    main()
    if errors:
        print("\n".join(f"FAIL {e}" for e in errors))
        sys.exit(1)
    print("All manifests check out.")
