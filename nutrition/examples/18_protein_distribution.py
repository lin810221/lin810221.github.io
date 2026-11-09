"""Same recorded total can be distributed differently; no clinical outcome is predicted."""
for meals in ([20,20,20],[5,10,45]): print({"per_meal_g":meals,"sum_g":sum(meals),"not_an_optimized_plan":True})
