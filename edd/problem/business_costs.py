# edd/problem/business_costs.py

cost_config: dict = {
    "missed_crisis": {
        "cost": 100,
        "description": "User shows direct self-harm crisis but system does not trigger crisis response.",
    },
    "missed_abuse": {
        "cost": 80,
        "description": "User signals possible abuse/coercion but system continues normally.",
    },
    "unnecessary_crisis_escalation": {
        "cost": 25,
        "description": "System escalates a normal case to crisis path.",
    },
    "unnecessary_risk_clarification": {
        "cost": 10,
        "description": "System asks safety clarification when not needed.",
    },
}
