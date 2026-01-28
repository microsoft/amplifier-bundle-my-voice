# Voice System Delegation Policy

## MANDATORY: Question Surfacing Protocol

**When ANY spawned voice agent returns a response containing options or a question for the user:**

### STOP. Do not continue.

1. **Display the question/options VERBATIM** to the user
2. **WAIT** for user's explicit answer
3. **Only THEN** resume with the user's actual response

### Detection Patterns

Look for these in agent responses:
- "Which applies?" / "Which option?" / "Which works for you?"
- "A) ... B) ... C) ..."
- Any response ending in "?"
- "[USER INPUT REQUIRED]" markers

### This is NOT Optional

Auto-answering on behalf of the user **violates user agency**. The user may have important context (like an existing profile stored elsewhere) that you don't know about.

<example type="violation">
Agent returns: "A/B/C - which applies?"
You respond: *resume session with "C - Skip"*
**VIOLATION** - You answered FOR the user without asking them
</example>

<example type="correct">
Agent returns: "A/B/C - which applies?"
You respond: "Before I continue, I need your input:

**A) I have one stored already** (GitHub repo or another device)
**B) I'm new to this** - let me try it first
**C) Skip setup for now** - just help with this message

Which applies to you?"
User answers: "A - I have mine in GitHub"
You: *resume session with user's actual answer*
</example>

---

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
3. **YOU surface those questions to the user** (see protocol above)
4. The agent handles setup based on user's answer, then proceeds

## Anti-Patterns (DO NOT)

❌ "I'll analyze your sessions and build a profile" (DIY)
✅ "I'll delegate to voice-analyst which has specialized profile algorithms"

❌ "Let me clean up this message for you" (DIY)
✅ "I'll use message-tuner which has your voice profile and style matching"

❌ Agent asks "A/B/C?" → You answer "C" for them (AUTO-ANSWERING)
✅ Agent asks "A/B/C?" → You show options to user → User answers → You relay answer

## Why This Matters

These agents have:
- **Specialized algorithms** for pattern extraction and style matching
- **Access to your voice profile** with learned preferences
- **Methodology** for preserving voice while improving clarity
- **Learning capture** to improve over time
- **First-run handling** built into their workflow

You lack these. Attempting DIY will produce generic results that don't preserve the user's authentic voice.
