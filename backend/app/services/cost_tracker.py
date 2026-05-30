# Token pricing per million tokens (input + output blended estimate)
PRICING = {
    "sonnet": 8.0,   # $3 input + $15 output, blended ~$8/M
    "opus": 30.0,    # $15 input + $75 output, blended ~$30/M
}

# Default hourly rate for ROI calculation
DEFAULT_HOURLY_RATE = 75.0


def estimate_cost(tokens_used: int, model: str = "sonnet") -> float:
    rate = PRICING.get(model, PRICING["sonnet"])
    return (tokens_used / 1_000_000) * rate


def estimate_pipeline_cost(
    analysis_tokens: int,
    generation_tokens: int,
    review_tokens: int,
) -> dict:
    analysis_cost = estimate_cost(analysis_tokens, "sonnet")
    generation_cost = estimate_cost(generation_tokens, "opus")
    review_cost = estimate_cost(review_tokens, "sonnet")
    total = analysis_cost + generation_cost + review_cost

    return {
        "analysis_cost": round(analysis_cost, 4),
        "generation_cost": round(generation_cost, 4),
        "review_cost": round(review_cost, 4),
        "total_cost": round(total, 4),
    }


def calculate_roi(hours_saved: float, total_cost: float, hourly_rate: float = DEFAULT_HOURLY_RATE) -> float:
    if total_cost <= 0:
        return 0.0
    return round((hours_saved * hourly_rate) / total_cost, 1)
