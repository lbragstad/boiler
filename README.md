# boiler
Calculate meal ratios according to scale.

## Usage

```
> python boil.py -h
usage: seafood-boil [-h] [-i INPUT]

Calculate seafood boil ratios.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Meal plan to parse. Detailed in a .yaml file
```

Let's say you want to plan a crawfish boil, but you're too lazy to figure out
how much raw food to get. You can describe your meal plan in YAML, where
`(required)` is what's expected in order for `boil.py` to work properly.

```
---
# (required) number of people
people: 8

# (required) ounces of edible protein per person
ounces_per_person: 12

# (required) list of food you want to incorporate into your boil
foods:
    "crawfish":
        # (required) this would mean crawfish would make up 60% of the meal
        ratio: 0.6
        # (required) this is an estimation of how edible the raw thing is,
        # crawfish have a lot of shell so consider only 20% of it's total
        # weight to be edible
        edible_percentage: 0.20
        # (required) estimated price per pound in USD
        price_per_pound: 3
    "shrimp":
        ratio: 0.2
        edible_percentage: 0.25
        price_per_pound: 7
    "sausage":
        ratio: 0.2
        edible_percentage: 1
        price_per_pound: 5
```

Calculate your shopping list and get an estimate.

```
boiler >>> python boil.py -i crawfish.yaml
for 8 people you'll need:
-  6.48 pounds of crawfish: $19.44
-  1.2 pounds of sausage: $6.0
-  2.1 pounds of shrimp: $14.7
12 ounces of food per person
total cost: $40.14
```

So, in order to feed 8 people we'll need around 6.48 pounds of raw crawfish,
1.2 pounds of sausage, and 2.1 pounds of raw shrimp from the store. That will
feed everyone a 60, 20, 20 ratio respectively out of a 12 ounce meal
allocation.
