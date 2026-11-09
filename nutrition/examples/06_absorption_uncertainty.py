"""Hypothetical fractions illustrate a range, not personal bioavailability."""
intake=10
fictional_fractions=(.1,.3)
print({"intake_mg":intake,"hypothetical_absorbed_mg":[intake*f for f in fictional_fractions],"not_a_dri_comparison":True})
