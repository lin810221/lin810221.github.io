"""Quasi-hyperbolic weights illustrate present bias, not estimated behavior."""
beta,delta=.6,.95
for t in range(5):
    exponential=delta**t
    present_biased=1 if t==0 else beta*delta**t
    print({"delay":t,"exponential_weight":exponential,"present_bias_weight":present_biased})
