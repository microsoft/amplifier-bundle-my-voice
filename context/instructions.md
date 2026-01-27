# My Voice Instructions

You have access to the **my-voice** capability for personalizing AI interactions.

## Configuration Check

**Before using voice features, verify configuration exists:**

Check for `config.my-voice.profile_source` in the user's settings. If not configured, guide them:

```yaml
# Add to ~/.amplifier/settings.yaml
config:
  my-voice:
    profile_source: git+https://github.com/USER/my-voice-profiles
    # OR
    profile_source: local
```

## Profile Storage Locations

| Config Value | Profile Location |
|--------------|------------------|
| `git+https://github.com/user/repo` | Cloned to `~/.amplifier/my-voice/profiles/` from that repo |
| `local` | `~/.amplifier/my-voice/profiles/` (local only, not synced) |
| Not set | Features unavailable - prompt user to configure |

## Profile Structure

```
~/.amplifier/my-voice/profiles/
└── default/                    # Or username for multi-profile
    ├── VOICE_PROFILE.md        # How they communicate
    ├── DECODER_RING.md         # Guide for others (optional)
    └── samples/                # Writing samples (optional)
```

## Workflow: Building a Profile

1. **Check config** - Is `profile_source` set? If not, guide setup first.
2. **Gather samples** - Sessions, messages, writing samples
3. **Analyze** - Use `my-voice:voice-analyst` agent
4. **Create profile** - Start from template, customize
5. **Test** - Clean up a real message, get feedback
6. **Iterate** - Update profile based on what worked/didn't

## Workflow: Cleaning Up Messages

1. **Load profile** - Read from configured location
2. **Understand context** - Who's the audience? What medium?
3. **Apply guidelines** - Follow the profile's preserve/condense/never-do
4. **Present draft** - Show what changed and why
5. **Incorporate feedback** - Iterate until right
6. **Capture learnings** - Update profile if something new was learned

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
