# Relationship Support AI Assistant

A production-style AI system for relationship guidance — built with safety, structure, and evaluation at its core.

---

## What this is

This is **not a chatbot**.

It is a **decision system around an LLM**:

- understands user intent and emotional state
- enforces safety policies
- selects a response strategy
- generates controlled, grounded responses

---

## System Architecture

```text
UserMessage
   ↓
Safety Layer
(precheck → deep evaluation → policy)
   ↓
Intent + Emotion Classification
   ↓
Context Retrieval
(user state + therapist context + content)
   ↓
Response Planning
(mode selection)
   ↓
LLM Generation (constrained)
   ↓
Interaction Log + Evaluation
```

---

## Safety First

Safety is not handled by generation.

It is enforced by the system:

- high-recall precheck
- context-aware deep safety evaluation
- deterministic policy actions:
  - `continue_normal`
  - `clarify_risk`
  - `crisis_response`

Example:

```text
"I can't do this anymore" → clarification mode
"I want to kill myself" → crisis response, no normal pipeline
```

---

## Structured Intelligence

The system extracts:

- **Intent** — venting, advice, exercise, reflection
- **Emotion + intensity**
- **Target** — self, partner, family, therapist, other
- **Ambiguity score**

This enables state-aware behavior, not generic replies.

---

## Response Planning

Before generating text, the system chooses a response mode:

- emotional validation
- guided reflection
- coping exercise
- communication script
- clarifying question
- crisis response
- content recommendation

The planner narrows the allowed response.  
The LLM writes inside that box.

---

## Evaluation-First Development

Behavior is tested before adding real LLM complexity.

```text
test_cases.json
→ pipeline
→ structured checks
→ pass/fail
```

The evaluation checks:

- safety action
- intent
- emotion
- response mode

Current result:

```text
3/8 passing
```

This is intentional. The failures show exactly where the system needs better intelligence.

---

## Why this matters

Generic LLMs are risky in this domain because they:

- lack persistent, structured user state
- do not enforce safety guarantees
- produce inconsistent guidance
- cannot be reliably evaluated

This project addresses those gaps with:

- deterministic orchestration
- structured outputs
- safety-first routing
- response planning
- evaluation-driven iteration

---

## Current Status

- System architecture defined
- Core Pydantic models created
- Pipeline implemented
- Two-stage safety flow implemented
- Evaluation harness implemented

Next step:

```text
Improve classifier + planner until evals pass
then replace selected modules with structured LLM calls
```

---

## Core Principle

> The LLM is not the system.  
> The system decides. The LLM assists.
