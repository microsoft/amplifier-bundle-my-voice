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

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
