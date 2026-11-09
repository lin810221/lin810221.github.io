"""Small-country tariff welfare and the prohibitive-tariff boundary."""
from microeconomics import tariff
for rate in (0,10,20,40): print(rate,tariff(tariff_rate=rate))
