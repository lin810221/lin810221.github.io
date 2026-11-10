"""38: alcohol-units. Fictional offline educational example."""
volume_ml=330;abv_fraction=.05;ethanol_density_g_ml=.789
print({"ethanol_g_approx":volume_ml*abv_fraction*ethanol_density_g_ml})
print("5%以0.05計，密度為近似假設；標準杯各地不同，此式不產生安全飲酒配額。")
