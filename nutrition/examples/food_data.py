"""Synthetic composition tables with explicit bases, provenance and unknowns."""
from pathlib import Path
import json
import csv
from nutrition_core import nonnegative,positive,volume_mass,portion

DATA=Path(__file__).resolve().parent/'data'
NUTRIENTS={'energy_kcal','protein_g','available_carb_g','fiber_g','fat_g','saturated_g','total_sugars_g','free_sugars_g','sodium_mg','calcium_mg','iron_mg','vitamin_d_ug'}


def foods(path=None):
    rows=json.loads((Path(path) if path else DATA/'foods.json').read_text(encoding='utf-8'))
    indexed={}
    for row in rows:
        if not row.get('id') or row['id'] in indexed:raise ValueError('Food IDs must be nonempty and unique')
        if row['source_type']!='synthetic' or row['basis_unit'] not in {'g','mL'}:raise ValueError('Unknown provenance or basis')
        positive(basis=row['basis_amount'])
        if not row.get('state') or not row.get('group'):raise ValueError('State and food group required')
        values=row['nutrients']
        if set(values)!=NUTRIENTS:raise ValueError('Nutrient schema mismatch')
        for key,value in values.items():
            if value is not None:nonnegative(**{key:value})
        for child,parent in [('saturated_g','fat_g'),('total_sugars_g','available_carb_g'),('free_sugars_g','total_sugars_g')]:
            if values[child] is not None and values[parent] is not None and values[child]>values[parent]+1e-8:raise ValueError('Nutrient subset exceeds parent')
        indexed[row['id']]=row
    return indexed


def food_portion(food,amount,unit=None):
    nonnegative(amount=amount)
    original=unit or food['basis_unit']
    converted=volume_mass(amount,original,food['basis_unit'],food.get('density_g_ml'))
    # Zero consumption contributes zero even when composition is unmeasured.
    values={key:(0 if converted==0 else None if value is None else portion(value,converted,food['basis_amount'])) for key,value in food['nutrients'].items()}
    return {'food_id':food['id'],'amount':amount,'unit':original,'nutrients':values,'group':food['group']}


def meal(items,catalog=None):
    catalog=foods() if catalog is None else catalog
    portions=[]
    for item in items:
        if item['food_id'] not in catalog:raise ValueError('Unknown food ID')
        portions.append(food_portion(catalog[item['food_id']],item['amount'],item.get('unit')))
    result={}
    for nutrient in sorted(NUTRIENTS):
        missing=[row['food_id'] for row in portions if row['nutrients'][nutrient] is None]
        known=sum(row['nutrients'][nutrient] or 0 for row in portions)
        result[nutrient]={'amount':None if missing else known,'known_subtotal':known,'missing_foods':missing}
    return {'nutrients':result,'groups_present':sorted({r['group'] for r in portions if r['amount']>0}),
            'portions':portions,'interpretation':'Synthetic arithmetic; food-group presence does not establish dietary adequacy'}


def diary(path=None):
    with (Path(path) if path else DATA/'diary.csv').open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    days={}
    for row in rows:
        row['amount']=float(row['amount']);nonnegative(amount=row['amount'])
        if not row['day'] or row['unit'] not in {'g','mL'}:raise ValueError('Explicit day and unit required')
        days.setdefault(row['day'],[]).append(row)
    return {day:meal(items) for day,items in sorted(days.items())}


def references():return json.loads((DATA/'references.json').read_text(encoding='utf-8'))


def free_sugar_known(food):
    value=food['nutrients']['free_sugars_g']
    return {'value':value,'reason':'Unknown recipe; total sugar cannot identify free sugar' if value is None else 'Defined synthetic recipe, not inferred from total sugar'}
