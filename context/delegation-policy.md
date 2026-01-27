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

## Anti-Patterns (DO NOT)

❌ "I'll analyze your sessions and build a profile" (DIY)
✅ "I'll delegate to voice-analyst which has specialized profile algorithms"

❌ "Let me clean up this message for you" (DIY)
✅ "I'll use message-tuner which has your voice profile and style matching"

❌ "Based on what I can see in your writing..." (DIY analysis)
✅ "I'll have voice-analyst analyze your patterns - it has algorithms I lack"

## Why This Matters

These agents have:
- **Specialized algorithms** for pattern extraction and style matching
- **Access to your voice profile** with learned preferences
- **Methodology** for preserving voice while improving clarity
- **Learning capture** to improve over time

You lack these. Attempting DIY will produce generic results that don't preserve the user's authentic voice.
