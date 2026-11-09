"""Competitive labor demand and supply; monopsony is a different model."""
from microeconomics import market,price_control
print("Competitive wage equilibrium",market(a=100,b=1,c=20,d=1))
print("Binding wage floor; unemployment in this model",price_control(70,"floor"))
