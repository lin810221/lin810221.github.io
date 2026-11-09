"""Numerical identities, domain boundaries and artifact/data acceptance. No network."""
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree
import importlib
import json
import math
import unittest
from microeconomics import (ppf,market,price_control,midpoint_elasticity,consumer,hicks_decomposition,
    leisure,intertemporal,firm,monopoly,cournot,game,externality,abatement,insurance,distribution,trade,tariff)
from macroeconomics import (expenditure_gdp,price_indexes,percent_change,labor,growth,solow,growth_accounting,
    fisher,present_value,bond,bank_loan,multiplier,ad_as,is_mp_pc,debt_path,exchange,balance_of_payments)
from evidence import ols,difference_in_differences,read_basket,read_vintages,as_of
from policy_report import deliver,market_svg


class MarketTests(unittest.TestCase):
    def test_ppf_endpoints(self):
        self.assertEqual(ppf(0)['y'],80);self.assertEqual(ppf(100)['y'],0)
        self.assertIsNone(ppf(100)['marginal_y_per_x'])
    def test_ppf_opportunity_cost_rises(self):
        self.assertGreater(ppf(80)['marginal_y_per_x'],ppf(20)['marginal_y_per_x'])
    def test_ppf_domain(self):
        for x in (-1,101,float('nan'),True):
            with self.subTest(x=x),self.assertRaises(ValueError): ppf(x)
    def test_market_clearing(self):
        r=market();self.assertEqual(r['q'],40);self.assertEqual(r['buyer_price'],60)
    def test_tax_wedge(self):
        r=market(tax=20);self.assertEqual(r['q'],30);self.assertEqual(r['buyer_price']-r['seller_price'],20)
    def test_tax_incidence(self):
        for b,d in ((1,1),(2,1),(.5,3)):
            base=market(b=b,d=d);r=market(b=b,d=d,tax=10)
            self.assertAlmostEqual((r['buyer_price']-base['buyer_price'])/10,r['buyer_tax_share'])
            self.assertAlmostEqual((base['seller_price']-r['seller_price'])/10,r['seller_tax_share'])
    def test_welfare_identity(self):
        for tax in (0,1,20,79,80,100):
            r=market(tax=tax);self.assertAlmostEqual(r['total_surplus']+r['dwl'],1600)
    def test_tax_revenue_not_all_lost(self):
        r=market(tax=20);self.assertEqual(r['revenue'],600);self.assertEqual(r['dwl'],100)
    def test_no_trade_has_no_unique_price(self):
        for tax in (80,100):
            r=market(tax=tax);self.assertEqual(r['q'],0);self.assertIsNone(r['buyer_price']);self.assertEqual(r['revenue'],0)
    def test_market_invalid(self):
        for kwargs in ({'b':0},{'d':0},{'tax':-1},{'a':10},{'c':float('inf')}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError): market(**kwargs)
    def test_price_ceiling(self):
        r=price_control(40);self.assertTrue(r['binding']);self.assertEqual(r['q'],20);self.assertEqual(r['shortage'],40)
    def test_nonbinding_control(self):
        self.assertFalse(price_control(70)['binding']);self.assertFalse(price_control(40,'floor')['binding'])
    def test_price_floor(self):
        r=price_control(70,'floor');self.assertEqual(r['q'],30);self.assertEqual(r['excess_supply'],20)
    def test_elasticity_reversal(self):
        self.assertAlmostEqual(midpoint_elasticity(40,30,60,70),midpoint_elasticity(30,40,70,60))
    def test_elasticity_invalid(self):
        with self.assertRaises(ValueError): midpoint_elasticity(1,2,3,3)


class ConsumerFirmTests(unittest.TestCase):
    def test_consumer_budget(self):
        r=consumer();self.assertEqual(r['x'],30);self.assertEqual(r['y'],20);self.assertEqual(r['expenditure'],120)
    def test_consumer_zero_wealth(self):
        self.assertEqual(consumer(0)['utility'],0)
    def test_cobb_douglas_foc(self):
        r=consumer(alpha=.3);self.assertAlmostEqual(.3/.7*r['y']/r['x'],2/3)
    def test_consumer_invalid(self):
        for kwargs in ({'income':-1},{'px':0},{'alpha':1}):
            with self.assertRaises(ValueError): consumer(**kwargs)
    def test_hicks_adding_up(self):
        r=hicks_decomposition();self.assertAlmostEqual(r['substitution']+r['income_effect'],r['total'])
        self.assertLess(r['substitution'],0);self.assertLess(r['income_effect'],0)
    def test_hicks_utility_held(self):
        r=hicks_decomposition();self.assertAlmostEqual(consumer()['utility'],consumer(r['compensated_income'],px=3)['utility'])
    def test_leisure_budget_and_corner(self):
        r=leisure();self.assertAlmostEqual(r['consumption'],10*r['hours']);self.assertEqual(leisure(nonlabor=1000)['hours'],0)
    def test_intertemporal_budget(self):
        r=intertemporal();self.assertAlmostEqual(r['c1']+r['c2']/1.05,r['present_value'])
    def test_firm_marginal_condition(self):
        r=firm(price=20);self.assertEqual(r['mc'],20);self.assertEqual(r['q'],5)
    def test_shutdown_loses_fixed_cost(self):
        r=firm(price=5);self.assertEqual(r['q'],0);self.assertEqual(r['profit'],-100)
    def test_fixed_cost_does_not_change_positive_short_run_q(self):
        self.assertEqual(firm(fixed=100)['q'],firm(fixed=1000)['q'])
    def test_producer_surplus_not_profit(self):
        r=firm();self.assertAlmostEqual(r['producer_surplus']-r['fixed_cost'],r['profit'])
    def test_monopoly_mr_mc(self):
        r=monopoly();self.assertEqual(r['mr'],r['mc']);self.assertGreater(r['price'],r['mc'])
    def test_monopoly_deadweight(self):
        self.assertEqual(monopoly()['dwl'],800)
    def test_cournot_n_one_matches_monopoly(self):
        self.assertAlmostEqual(cournot(1)['total_q'],monopoly()['q'])
    def test_cournot_limit(self):
        self.assertLess(cournot(100)['price'],cournot(2)['price']);self.assertGreater(cournot(100)['price'],20)
    def test_prisoner_dilemma(self):
        self.assertEqual(game()['pure'],[(1,1)]);self.assertIsNone(game()['interior_mixed'])
    def test_matching_pennies(self):
        r=game(((1,-1),(-1,1)),((-1,1),(1,-1)))
        self.assertEqual(r['pure'],[]);self.assertEqual(r['interior_mixed'],{'row0_probability':.5,'column0_probability':.5})
    def test_tied_game_preserves_equilibria(self):
        self.assertEqual(len(game(((1,1),(1,1)),((1,1),(1,1)))['pure']),4)


class PolicyMicroTests(unittest.TestCase):
    def test_pigou_implements_optimum(self):
        r=externality();self.assertAlmostEqual(market(tax=r['pigou_tax'])['q'],r['optimal_q'])
    def test_zero_damage_no_distortion(self):
        r=externality(damage=0);self.assertEqual(r['market_q'],r['optimal_q']);self.assertEqual(r['externality_loss'],0)
    def test_abatement_equal_mac(self):
        r=abatement();self.assertAlmostEqual(sum(r['amounts']),12);self.assertAlmostEqual(r['amounts'][0],3*r['amounts'][1])
    def test_abatement_capacity(self):
        r=abatement(25);self.assertAlmostEqual(r['amounts'][0],10);self.assertAlmostEqual(r['amounts'][1],15)
    def test_abatement_invalid(self):
        with self.assertRaises(ValueError): abatement(26)
    def test_fair_insurance_log_utility(self):
        self.assertTrue(insurance()['prefer_insurance']);self.assertFalse(insurance(premium=20)['prefer_insurance'])
    def test_gini_equality(self):
        self.assertEqual(distribution((10,10,10))['gini'],0);self.assertEqual(distribution((0,0))['gini'],0)
    def test_gini_bounds_and_poverty(self):
        r=distribution();self.assertAlmostEqual(r['gini'],.25);self.assertEqual(r['headcount'],.5)
    def test_trade_mutual_gains(self):
        r=trade(export_x=30);self.assertGreater(r['a_utility_gain'],0);self.assertGreater(r['b_utility_gain'],0)
    def test_not_every_trade_volume_benefits_both(self):
        self.assertLess(trade(export_x=10)['a_utility_gain'],0)
    def test_trade_price_must_fit_opportunity_costs(self):
        with self.assertRaises(ValueError): trade(price=.1)
    def test_tariff_small_country_loss(self):
        self.assertEqual(tariff(tariff_rate=0)['dwl'],0);self.assertGreater(tariff()['dwl'],0)
    def test_prohibitive_tariff_stops_imports(self):
        r=tariff(tariff_rate=100);self.assertEqual(r['imports'],0);self.assertEqual(r['revenue'],0);self.assertEqual(r['price'],60)


class MacroTests(unittest.TestCase):
    def test_nominal_gdp_identity(self):
        self.assertEqual(expenditure_gdp(600,200,150,120,100),970)
    def test_inventory_can_be_negative(self):
        self.assertEqual(expenditure_gdp(100,-10,20,5,5),110)
    def test_price_indexes_base(self):
        r=price_indexes([10,20],[2,3],[10,20],[2,3]);self.assertEqual(r['cpi_laspeyres'],100);self.assertEqual(r['gdp_deflator_fixed_base'],100)
    def test_cpi_and_deflator_differ(self):
        r=price_indexes([1,1],[1,1],[2,1],[1,3]);self.assertEqual(r['cpi_laspeyres'],150);self.assertEqual(r['gdp_deflator_fixed_base'],125)
    def test_price_index_invalid(self):
        with self.assertRaises(ValueError): price_indexes([0],[1],[1],[1])
    def test_percent_vs_points(self):
        self.assertEqual(percent_change(4,5),25)
    def test_labor_denominators(self):
        r=labor(90,10,150);self.assertEqual(r['unemployment_rate'],.1);self.assertEqual(r['employment_population'],.6)
    def test_labor_force_exit(self):
        before,after=labor(90,10,150),labor(90,5,150)
        self.assertLess(after['unemployment_rate'],before['unemployment_rate']);self.assertEqual(after['employment_population'],before['employment_population'])
    def test_growth_compounds(self):
        r=growth(100,200,10);self.assertAlmostEqual((1+r['cagr'])**10,2);self.assertAlmostEqual(r['doubling_years'],10)
    def test_negative_growth_has_no_doubling_time(self):
        self.assertIsNone(growth(final=90)['doubling_years'])
    def test_solow_steady_state_transition(self):
        steady=solow()['steady_k'];r=solow(k0=steady,periods=1);self.assertAlmostEqual(r['path'][1]['k'],steady)
    def test_solow_exact_discrete_dilution(self):
        self.assertAlmostEqual(solow()['replacement_rate'],.0802)
    def test_solow_convergence(self):
        r=solow(periods=500);self.assertAlmostEqual(r['path'][-1]['k'],r['steady_k'],places=6)
    def test_solow_golden_rule(self):
        for s in (.1,.2,.3,.4,.5):
            self.assertLessEqual(solow(s=s)['steady_consumption'],solow(s=.3)['steady_consumption']+1e-9)
    def test_growth_accounting_adds(self):
        r=growth_accounting(100,110,100,120,100,102)
        self.assertAlmostEqual(r['capital_contribution']+r['labor_contribution']+r['residual_tfp'],r['log_output_growth'])
    def test_fisher_exact(self):
        self.assertAlmostEqual(fisher(.05,.02)['real_exact'],1.05/1.02-1)
    def test_bond_price_yield_direction(self):
        self.assertGreater(bond(yield_rate=.02)['price'],bond(yield_rate=.08)['price'])
    def test_zero_coupon_duration(self):
        self.assertAlmostEqual(bond(coupon_rate=0)['macaulay_duration'],5)
    def test_npv_zero_discount(self):
        self.assertEqual(present_value((-100,40,40,40),0),20)
    def test_loan_creates_matching_deposit(self):
        r=bank_loan();self.assertEqual(r['assets']['loans'],70);self.assertEqual(r['liabilities']['deposits'],90)
        self.assertEqual(sum(r['assets'].values()),sum(r['liabilities'].values())+r['equity'])
    def test_invalid_opening_bank_balance(self):
        with self.assertRaises(ValueError): bank_loan(deposits=70)
    def test_multiplier_goods_market_identity(self):
        r=multiplier();self.assertAlmostEqual(r['output'],r['consumption']+30+40+20-r['imports'])
    def test_multiplier_spending_change(self):
        a,b=multiplier(G=40),multiplier(G=50);self.assertAlmostEqual(b['output']-a['output'],10*a['spending_multiplier'])
    def test_multiplier_import_leakage(self):
        self.assertLess(multiplier(m=.3)['spending_multiplier'],multiplier(m=0)['spending_multiplier'])
    def test_adas_shocks(self):
        base=ad_as();self.assertGreater(ad_as(A=220)['output'],base['output']);self.assertGreater(ad_as(C=0)['price_level'],base['price_level'])
    def test_is_mp_pc_three_equations(self):
        r=is_mp_pc(a=2,cost_shock=1)
        self.assertAlmostEqual(r['output_gap_pp'],2-(r['real_rate_percent']-1))
        self.assertAlmostEqual(r['inflation_percent'],2+.5*r['output_gap_pp']+1)
        self.assertAlmostEqual(r['real_rate_percent'],1+(r['inflation_percent']-2))
        self.assertAlmostEqual(r['nominal_rate_percent'],r['real_rate_percent']+2)
    def test_supply_shock_tradeoff(self):
        r=is_mp_pc(cost_shock=2);self.assertLess(r['output_gap_pp'],0);self.assertGreater(r['inflation_percent'],2)
    def test_debt_stabilizing_primary_balance(self):
        needed=debt_path()['stabilizing_primary_surplus'];r=debt_path(primary_surplus=needed)
        self.assertAlmostEqual(r['rows'][-1]['net_debt_ratio'],.6)
    def test_debt_uses_gross_rate_ratio(self):
        r=debt_path(initial=.6,periods=1);self.assertAlmostEqual(r['rows'][1]['net_debt_ratio'],1.04/1.03*.6-.01)
    def test_covered_parity(self):
        r=exchange();self.assertAlmostEqual(r['covered_parity_forward']/32*1.02,1.03)
    def test_bop_financial_account_sign(self):
        r=balance_of_payments();self.assertEqual(r['statistical_discrepancy'],2);self.assertEqual(r['identity_residual'],0)


class EvidenceDeliveryTests(unittest.TestCase):
    def test_ols_known_line_and_residual_sum(self):
        r=ols([1,2,3,4],[3,5,7,9]);self.assertEqual(r['slope'],2);self.assertEqual(r['intercept'],1);self.assertAlmostEqual(sum(r['residuals']),0)
    def test_ols_no_variation(self):
        with self.assertRaises(ValueError): ols([1,1,1],[1,2,3])
    def test_did_four_means(self):
        self.assertEqual(difference_in_differences(100,115,80,90)['estimate'],5)
    def test_vintage_cannot_see_future_revision(self):
        rows=read_vintages();earlier=as_of(rows,'2025-05-01');later=as_of(rows,'2026-02-01')
        self.assertEqual(earlier[0]['value'],100);self.assertEqual(later[0]['value'],101)
        self.assertEqual(as_of(rows,'2025-01-01'),[])
    def test_vintage_observation_not_release_date(self):
        self.assertEqual(len(as_of(read_vintages(),'2025-06-30')),1)
    def test_basket_has_stable_items(self):
        rows=read_basket();self.assertEqual(set(rows),{'2024','2025','2026'})
        self.assertEqual(set(rows['2024']),set(rows['2026']))
    def test_plot_is_valid_standalone_svg(self):
        tree=ElementTree.fromstring(market_svg());self.assertEqual(tree.tag,'{http://www.w3.org/2000/svg}svg')
        self.assertIn('No empirical calibration',market_svg())
    def test_report_and_csv_delivery(self):
        with TemporaryDirectory() as folder:
            out=Path(folder)/'delivery';r=deliver(out)
            self.assertTrue(r['synthetic']);self.assertTrue(all(r['checks'].values()));self.assertEqual(r['scenarios'],15)
            self.assertEqual(r['baseline_tax20']['dwl'],100);self.assertTrue((out/'market.svg').is_file())
            self.assertEqual(json.loads((out/'report.json').read_text())['data_sha256'],r['data_sha256'])
            with self.assertRaises(FileExistsError): deliver(out)


if __name__=='__main__': unittest.main(verbosity=2)
