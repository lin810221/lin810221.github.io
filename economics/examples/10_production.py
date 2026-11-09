"""Cobb-Douglas production and marginal products; not an estimated technology."""
K,L,A,alpha=100,25,2,.3
Y=A*K**alpha*L**(1-alpha)
MPK=alpha*Y/K; MPL=(1-alpha)*Y/L
print({"Y":Y,"MPK":MPK,"MPL":MPL,"Euler_sum":MPK*K+MPL*L})
