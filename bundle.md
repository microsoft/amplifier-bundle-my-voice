---
bundle:
  name: my-voice
  version: 0.1.0
  description: Voice preservation and communication tuning - clean up messages while keeping your authentic voice

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main

agents:
  include:
    - my-voice:voice-analyst
    - my-voice:message-tuner

# NOTE: my-voice-profiles tool is scoped to AGENTS ONLY (not root session)
# This structurally enforces delegation - root can't pre-check state
# Tool is declared in each agent's frontmatter

hooks:
  - module: my-voice-sync
    source: git+https://github.com/microsoft/amplifier-bundle-my-voice@main#subdirectory=modules/hook-my-voice-sync
    config:
      my-voice:
        profile_source: unconfigured
        local_path: ~/.amplifier/my-voice/profiles
---

@my-voice:context/delegation-policy.md

---

# My Voice

Voice preservation and communication tuning for Amplifier.

Clean up your messages while keeping them sounding like YOU wrote them.

## Quick Start

**First time? Configure your profile storage:**

```yaml
# Add to ~/.amplifier/settings.yaml
config:
  my-voice:
    # Option A: Private GitHub repo
    profile_source: git+https://github.com/YOUR_USER/my-voice-profiles
    
    # Option B: Local files only
    # profile_source: local
```

Then create your profile:
```
"Analyze my recent sessions and build a voice profile for me"
```

**Clean up a message:**
```
"Help me clean up this message for my team" + [paste your message]
```

## What This Does

- **Voice Profiles** - Captures how you communicate (phrases, patterns, tone)
- **Message Cleanup** - Condenses verbose messages while preserving your voice
- **Decoder Rings** - Helps others' Amplifiers understand your communication style

## Agents

| Agent | Use For |
|-------|---------|
| `my-voice:voice-analyst` | Building voice profiles from your sessions/samples |
| `my-voice:message-tuner` | Cleaning up messages using your profile |

## Profile Storage

Profiles are personal - they're stored separately from this bundle:

| Option | Config | Where Profiles Live |
|--------|--------|---------------------|
| **GitHub** (recommended) | `profile_source: git+https://...` | Your private repo |
| **Local** | `profile_source: local` | `~/.amplifier/my-voice/profiles/` |

GitHub storage syncs across devices. Local storage is device-only but works without a repo.

---

@my-voice:context/agent-overview.md

@foundation:context/shared/common-system-base.md
