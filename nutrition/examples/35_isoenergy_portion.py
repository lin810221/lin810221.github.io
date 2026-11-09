"""Equal calories need different masses and do not imply equivalent nutrition."""
from nutrition_core import match_energy
for density in (116,590): print(density,match_energy(120,density))
