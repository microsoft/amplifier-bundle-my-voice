# My Voice Instructions

You have access to the **my-voice** capability for personalizing AI interactions.

## First-Run Experience: ASK FIRST

**CRITICAL:** When a user asks for voice-related help and no profile is configured, **ASK before assuming** their situation. They may be:

1. **Returning user on a new device** - Has a profile stored in GitHub
2. **New user** - Wants to try it out first
3. **Just wants help now** - Skip setup for this session

### The Question to Ask

When `configuration_state` is "unconfigured", ask:

> "I don't see a voice profile set up on this device. Quick question:
>
> **A) I have one stored already** (GitHub repo or another device)  
> **B) I'm new to this** - let me try it first  
> **C) Skip setup for now** - just help with this message
>
> Which applies to you?"

### Handling Each Response

| Response | Action |
|----------|--------|
| **A) Has existing** | Ask for repo URL, use `my_voice_profiles` tool with `operation="configure"` to connect, then sync |
| **B) New user** | Work in "ephemeral mode" - infer style from their message. After success, offer to save learnings. |
| **C) Skip** | Work from context only. Don't mention setup again this session. |

## Configuration States

The hook will inject guidance based on state:

| State | Meaning | What to Do |
|-------|---------|------------|
| `unconfigured` | No settings configured | ASK the clarifying question above |
| `configured_needs_clone` | Git URL set, needs sync | Auto-handled by hook - just proceed |
| `configured_no_profile` | Storage ready, no profile | Offer to build profile or work from message |
| `ready` | Profile exists | Normal operation |

## Ephemeral Mode (Unconfigured Users)

When working without a persistent profile:

1. **Infer style** from the user's message itself
2. **Deliver value** - clean up their message
3. **Note patterns** you observed
4. **Offer to save**: "I noticed some patterns in your writing. Want me to save these for next time?"
5. **If yes**: Guide through configure operation

## Profile Storage Options

| Option | Config Value | Best For |
|--------|--------------|----------|
| **GitHub** | `git+https://github.com/user/repo` | Syncs across devices |
| **Local** | `local` | Single device, no sync needed |

## Configuring Storage (Agent-Assisted)

Use the `my_voice_profiles` tool with `operation="configure"`:

```json
// For GitHub storage
{"operation": "configure", "storage_type": "github", "git_url": "https://github.com/user/my-voice-profiles"}

// For local storage  
{"operation": "configure", "storage_type": "local"}
```

The tool will:
1. Update `~/.amplifier/settings.yaml`
2. For GitHub: Attempt to sync immediately
3. Report if existing profiles were found

## Profile Structure

```
~/.amplifier/my-voice/profiles/
└── default/                    # Or username for multi-profile
    ├── VOICE_PROFILE.md        # How they communicate
    ├── DECODER_RING.md         # Guide for others (optional)
    └── samples/                # Writing samples (optional)
```

## Workflow: Building a Profile

1. **Check state** - Use `my_voice_profiles` with `operation="status"` to see `configuration_state`
2. **If unconfigured** - ASK the clarifying question, don't assume
3. **Gather samples** - Sessions, messages, writing samples
4. **Analyze** - Use `my-voice:voice-analyst` agent
5. **Create profile** - Start from template, customize
6. **Test** - Clean up a real message, get feedback
7. **Iterate** - Update profile based on what worked/didn't

## Workflow: Cleaning Up Messages

1. **Check state** - Is profile ready? If not, handle appropriately
2. **Load profile** - Read from configured location (or infer from message if ephemeral)
3. **Understand context** - Who's the audience? What medium?
4. **Apply guidelines** - Follow the profile's preserve/condense/never-do
5. **Present draft** - Show what changed and why
6. **Incorporate feedback** - Iterate until right
7. **Capture learnings** - Update profile if something new was learned

## Agents

### my-voice:voice-analyst

Analyzes communication samples to build voice profiles.

**Delegate when:**
- Creating a new profile from scratch
- Analyzing sessions to extract patterns
- Updating a profile with new learnings

### my-voice:message-tuner

Cleans up messages using an existing voice profile.

**Delegate when:**
- User has a message to clean up
- Need to adapt a message for a different audience
- Transforming verbose content while preserving voice

## Learning Discipline

Voice profiles improve through use. After each cleanup iteration:

1. Note what worked / what didn't
2. Identify the principle (not just the instance)
3. Add to the Learnings Log in the profile
4. Commit changes if using git storage

## Templates

Templates for new profiles are at:
- `my-voice:templates/VOICE_PROFILE_TEMPLATE.md`
- `my-voice:templates/DECODER_RING_TEMPLATE.md`

Use these as starting points, then customize based on analysis.
