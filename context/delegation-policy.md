# Voice System Delegation Policy

**CRITICAL**: The voice profile system uses specialized agents with session analysis algorithms and style matching capabilities you do not have. You MUST delegate to the appropriate agent.

## Domain Honoring

When these agents are available, you MUST delegate rather than attempting the task directly:

| Domain | Agent | Why Delegate |
|--------|-------|--------------|
| Profile building/analysis | `my-voice:voice-analyst` | Session parsing algorithms, pattern extraction |
| Message cleanup/tuning | `my-voice:message-tuner` | Style matching, voice preservation algorithms |

## Trigger Phrases → Delegation

| User Says | Delegate To |
|-----------|-------------|
| "Build a voice profile" | `my-voice:voice-analyst` |
| "Analyze my sessions/style" | `my-voice:voice-analyst` |
| "Update my profile" | `my-voice:voice-analyst` |
| "Clean up this message" | `my-voice:message-tuner` |
| "Help me with this [message/email/text]" | `my-voice:message-tuner` |
| "Make this clearer" | `my-voice:message-tuner` |
| "Write this in my voice" | `my-voice:message-tuner` |

## How It Works

**The agents handle first-run onboarding themselves.** When you delegate:

1. The agent checks `configuration_state` via the `my_voice_profiles` tool
2. If unconfigured, the agent asks the user clarifying questions
3. The agent handles setup if needed, then proceeds with the work
4. You don't need to check state before delegating - just delegate

**This means:** You can confidently delegate on trigger phrases. The specialized agent knows how to handle all states including first-run.

## Anti-Patterns (DO NOT)

❌ "I'll analyze your sessions and build a profile" (DIY)
✅ "I'll delegate to voice-analyst which has specialized profile algorithms"

❌ "Let me clean up this message for you" (DIY)
✅ "I'll use message-tuner which has your voice profile and style matching"

❌ "Based on what I can see in your writing..." (DIY analysis)
✅ "I'll have voice-analyst analyze your patterns - it has algorithms I lack"

❌ "Let me check if you have a profile first..." (unnecessary pre-check)
✅ Just delegate - the agent handles state checking internally

## Why This Matters

These agents have:
- **Specialized algorithms** for pattern extraction and style matching
- **Access to your voice profile** with learned preferences
- **Methodology** for preserving voice while improving clarity
- **Learning capture** to improve over time
- **First-run handling** built into their workflow

You lack these. Attempting DIY will produce generic results that don't preserve the user's authentic voice.
