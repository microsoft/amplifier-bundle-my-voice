# amplifier-bundle-my-voice

Voice preservation and communication tuning for [Amplifier](https://github.com/microsoft/amplifier).

Clean up your messages while keeping them sounding like YOU wrote them.

## What This Does

- **Voice Profiles** - Captures how you communicate (phrases, patterns, tone)
- **Message Cleanup** - Condenses verbose messages while preserving your voice
- **Decoder Rings** - Helps others' Amplifiers understand your communication style

## Installation

Include in your bundle:

```yaml
includes:
  - bundle: git+https://github.com/microsoft/amplifier-bundle-my-voice@main
```

## Configuration

Add to `~/.amplifier/settings.yaml`:

```yaml
config:
  my-voice:
    # Option A: Private GitHub repo (syncs across devices)
    profile_source: git+https://github.com/YOUR_USER/my-voice-profiles
    
    # Option B: Local files only (this device)
    # profile_source: local
```

## Usage

**Build your voice profile:**
```
"Analyze my recent sessions and build a voice profile for me"
```

**Clean up a message:**
```
"Help me clean up this Teams message" + [paste your message]
```

**Create a decoder ring for others:**
```
"Create a decoder ring from my voice profile"
```

## Agents

| Agent | Description |
|-------|-------------|
| `my-voice:voice-analyst` | Analyzes sessions/samples to build voice profiles |
| `my-voice:message-tuner` | Cleans up messages using your profile |

## Profile Storage

Profiles are personal and stored separately:

| Option | Location |
|--------|----------|
| GitHub | Your private repo, synced to `~/.amplifier/my-voice/profiles/` |
| Local | `~/.amplifier/my-voice/profiles/` (device-only) |

## License

MIT
