"""Artificial logits for learning softmax and nucleus sampling, not a real model."""
import math


def distribution(logits: list[float], temperature: float = 1.0, top_p: float = 1.0) -> list[float]:
    if not logits or not all(math.isfinite(value) for value in logits):
        raise ValueError("Provide a nonempty list of finite logits")
    if not math.isfinite(temperature) or temperature < 0 or not 0 < top_p <= 1:
        raise ValueError("temperature >= 0 and 0 < top_p <= 1 required")
    if temperature == 0:
        winner = max(range(len(logits)), key=logits.__getitem__)
        return [1.0 if index == winner else 0.0 for index in range(len(logits))]
    peak = max(logits)
    weights = [math.exp((value - peak) / temperature) for value in logits]
    total = sum(weights)
    probabilities = [weight / total for weight in weights]
    ordered = sorted(range(len(logits)), key=lambda index: probabilities[index], reverse=True)
    keep, cumulative = [], 0.0
    for index in ordered:
        keep.append(index)
        cumulative += probabilities[index]
        if cumulative >= top_p:
            break
    retained = sum(probabilities[index] for index in keep)
    return [probability / retained if index in keep else 0.0 for index, probability in enumerate(probabilities)]


if __name__ == "__main__":
    names = ["建議", "可以", "或許", "但是"]
    for temperature, top_p in [(1.0, 1.0), (0.3, 1.0), (1.0, 0.6)]:
        print("T=", temperature, "top_p=", top_p)
        print(dict(zip(names, map(lambda p: round(p, 4), distribution([2.8, 1.9, 0.9, 0.3], temperature, top_p)))))
