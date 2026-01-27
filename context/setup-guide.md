# My Voice Setup Guide

## Step 1: Choose Your Storage

**Option A: Private GitHub Repo (Recommended)**
- Syncs across all your devices
- Version controlled
- Can share decoder ring with others

**Option B: Local Files**
- No GitHub account needed
- Stays on this device only
- Simpler setup

## Step 2: Configure Storage

Add to `~/.amplifier/settings.yaml`:

```yaml
config:
  my-voice:
    # For GitHub storage:
    profile_source: git+https://github.com/YOUR_USERNAME/my-voice-profiles
    
    # For local storage:
    # profile_source: local
```

### GitHub Setup (Option A)

1. Create a **private** repo (e.g., `my-voice-profiles`)
2. Add the git URL to your settings (as shown above)
3. The bundle will clone/pull automatically

### Local Setup (Option B)

1. Set `profile_source: local` in settings
2. Profiles stored at `~/.amplifier/my-voice/profiles/`
3. That's it - no repo needed

## Step 3: Build Your Profile

Once configured, ask Amplifier:

```
"Analyze my recent sessions and build a voice profile for me"
```

The `voice-analyst` agent will:
1. Mine your sessions for patterns
2. Identify your signature phrases, style, tone
3. Create a profile from the template
4. Save to your configured storage

## Step 4: Start Using It

Clean up a message:
```
"Help me clean up this Teams message" + [paste your message]
```

The `message-tuner` agent uses your profile to condense while preserving your voice.

## Optional: Create a Decoder Ring

Help others' Amplifiers understand your style:

```
"Create a decoder ring from my voice profile"
```

Share the decoder ring with colleagues - their Amplifier can use it to better parse your communications.

## Troubleshooting

**"Profile not configured"**
→ Check `~/.amplifier/settings.yaml` has `config.my-voice.profile_source` set

**"Profile not found"**
→ Run voice-analyst to create your initial profile

**GitHub auth issues**
→ Ensure `gh auth status` works, or use HTTPS with token
