"""InfoNCE arithmetic; score at index 0 is the designated positive."""
from embedding_core import contrastive_loss

if __name__ == "__main__":
    for temperature in (1., .2, .05):
        loss, probabilities = contrastive_loss([.8, .6, .1], temperature)
        print("temperature:", temperature, "loss:", round(loss, 5), "probabilities:", [round(p, 5) for p in probabilities])
