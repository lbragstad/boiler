# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os

import yaml


def _get_args():
    """Get arguments from the user."""
    parser = argparse.ArgumentParser(
        prog='seafood-boil',
        description='Calculate seafood boil ratios.')
    parser.add_argument('-i', '--input', type=str,
                        help='Meal plan to parse. Detailed in a .yaml file')
    args = parser.parse_args()
    return args.input


def _parse_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        plan = yaml.safe_load(f)
    return plan


def _calculate_meal_weight(plan):
    return plan.get('people') * plan.get('ounces_per_person')


def boil(plan):
    total_protein_weight = _calculate_meal_weight(plan)

    report = list()
    foods = plan.get('foods')
    for food in foods:
        food_ounces = total_protein_weight * foods.get(food).get('ratio')
        store_ounces = food_ounces * (
            (1 - foods.get(food).get('edible_percentage') + 1)
        )
        price = (store_ounces / 16) * foods.get(food).get('price_per_pound')
        summary = food, round(store_ounces, 2), round(price, 2)
        report.append(summary)

    return report


def main():
    # get the location of the yaml file that describes the meal plan
    yaml_file = _get_args()

    # parse the meal plan from yaml
    meal_plan = _parse_yaml(yaml_file)

    # determine ratios!
    report = boil(meal_plan)

    total_price = float()
    for item in report:
        print "%r pounds of %s: $%r" % (round(item[1] / 16, 2),
                                        item[0],
                                        item[2])
        total_price += item[2]
    print "%r ounces of food per person" % meal_plan.get('ounces_per_person')
    print "total cost: $%r" % round(total_price, 2)


if __name__ == '__main__':
    main()
