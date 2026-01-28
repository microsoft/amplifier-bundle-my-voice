# Voice System Delegation Policy

## MANDATORY: Passthrough Delegation (NO Pre-Processing)

**When a user triggers voice-related work, delegate IMMEDIATELY without pre-processing.**

### DO NOT Before Delegating:

❌ Call `my_voice_profiles` to check state first
❌ Analyze the user's writing style
❌ Summarize or interpret their message
❌ Add "helpful" context about what you observed
❌ Make any tool calls related to the voice domain

### DO When Delegating:

✅ Pass the user's request **verbatim**
✅ Include any content they provided (messages, samples)
✅ Delegate **immediately** upon trigger phrase match
✅ Let the agent run its own state-checking and onboarding

### Why This Matters

> **Think of yourself as a mail carrier, not an editor.** Deliver the message as-is.

If you pre-check state or pre-analyze writing:
- The agent thinks state is already known → skips its onboarding
- The agent thinks analysis is done → skips discovery phase
- Your "helpful" context contaminates the agent's flow

**The agent owns its domain.** Let it run its own logic.

<example type="violation">
User: "Write this in my voice: [message]"
You: *calls my_voice_profiles to check* → *analyzes their writing* → *delegates with "I noticed their patterns are..."*
**VIOLATION** - You pre-processed. Agent will skip onboarding.
</example>

<example type="correct">
User: "Write this in my voice: [message]"
You: "I'll delegate to message-tuner which has your voice profile and style matching."
You: *immediately delegates with*: "The user wants to write this in their voice: [message]"
**CORRECT** - Agent runs its own flow, asks user A/B/C if needed.
</example>

---

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

## Trigger Phrases → Immediate Delegation

| User Says | Delegate To | Instruction Format |
|-----------|-------------|-------------------|
| "Build a voice profile" | `my-voice:voice-analyst` | "The user wants to build a voice profile." |
| "Analyze my sessions/style" | `my-voice:voice-analyst` | "The user wants their sessions/style analyzed." |
| "Clean up this message" | `my-voice:message-tuner` | "The user wants to clean up this message: [verbatim]" |
| "Write this in my voice" | `my-voice:message-tuner` | "The user wants to write this in their voice: [verbatim]" |
| "Help me with this [message]" | `my-voice:message-tuner` | "The user wants help with this message: [verbatim]" |

## Anti-Patterns (DO NOT)

❌ "I'll analyze your sessions and build a profile" (DIY)
✅ "I'll delegate to voice-analyst which has specialized profile algorithms"

❌ "Let me clean up this message for you" (DIY)
✅ "I'll use message-tuner which has your voice profile and style matching"

❌ *Calls my_voice_profiles first* → *then delegates with "I checked and..."* (PRE-PROCESSING)
✅ *Immediately delegates* → Agent checks state itself → Agent runs its flow

❌ Agent asks "A/B/C?" → You answer "C" for them (AUTO-ANSWERING)
✅ Agent asks "A/B/C?" → You show options to user → User answers → You relay answer

## Why This Matters

These agents have:
- **Specialized algorithms** for pattern extraction and style matching
- **Access to your voice profile** with learned preferences
- **Methodology** for preserving voice while improving clarity
- **Learning capture** to improve over time
- **First-run handling** built into their workflow

You lack these. Attempting DIY or pre-processing will produce generic results and break the agent's onboarding flow.
