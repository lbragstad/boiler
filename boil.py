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

"""Calculator for estimating ratios and prices of meals."""

import argparse

import yaml


def _get_args():
    """Get arguments from the user."""
    parser = argparse.ArgumentParser(
        prog='seafood-boil',
        description='Calculate seafood boil ratios.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Meal plan to parse. Detailed in a .yaml file')
    args = parser.parse_args()
    return args.input


def _parse_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        plan = yaml.safe_load(f)
    return plan


def _calculate_meal_weight(plan):
    return plan.get('people') * plan.get('ounces_per_person')


def _validate_meal_plan(plan):
    """Check to make sure the values of the meal add up to 100%."""
    # get all the foods
    foods = plan.get('foods')
    total_ratio = 0
    for food in plan.get('foods'):
        total_ratio += foods.get(food).get('ratio')
    if not total_ratio == 1:
        raise ValueError(
            'Meal ratios should equal a total of 1. '
            'Total ratio given was %d' % total_ratio
        )


def boil(plan):
    """Determine the weight and price of a meal plan.

    This method expects a dictionary that contains the number of guests, ounces
    of food per person, and list of menu items. It will return the menu items
    in a list. Each item in the list is a tuple containing the item name, the
    ounces to buy from the store, and the estimated price of the item for the
    meal.

    :param plan: a dictionary containing the meal plan
    :returns: a list of tuples with calculated facts about the meal items

    """
    # calculate the total weight of the meal in ounces
    total_meal_weight = _calculate_meal_weight(plan)

    # get all the foods
    foods = plan.get('foods')

    # process every item in the meal plan
    report = list()
    for food in foods:

        # find the specific percentage of food needed
        food_ounces_needed = total_meal_weight * foods.get(food).get('ratio')

        # determine the raw weight, in ounces, of a specific food since this is
        # what you'll need to get from the store
        non_edible_percentage = 1 - foods.get(food).get('edible_percentage')

        # total weight multiplier of edible and non-edible bits, we
        # use this to determine the total weight in what we need to buy from
        # the store in order to feed everyone the proper ratio
        food_multiplier = non_edible_percentage + 1

        # calculate the total ounces need from the store, i.e. just tell this
        # to the guy behind the counter
        raw_ounces = food_ounces_needed * food_multiplier

        # based on the raw_ounces and the estimated price per pound, determine
        # the total cost of the item, in pounds
        price = (raw_ounces / 16) * foods.get(food).get('price_per_pound')

        # pack the name of the food, the total ounces needed from the store,
        # and the estimated price in a tuple and append it to the report
        summary = food, raw_ounces, price
        report.append(summary)

    return (report, plan.get('people'))


def main():
    """Main entry point for the boil calculator."""
    # get the location of the yaml file that describes the meal plan
    yaml_file = _get_args()

    # parse the meal plan from yaml
    meal_plan = _parse_yaml(yaml_file)

    # make sure the ratios in the meal plan equal 1, or 100% of the meal
    _validate_meal_plan(meal_plan)

    # determine ratios!
    report, number_of_people = boil(meal_plan)

    # print the number of people partaking
    print ("for %r people you'll need:" % number_of_people)

    total_price = float()
    for item in report:
        print ("-  %r pounds of %s: $%r" % (round(item[1] / 16, 2),
                                            item[0],
                                            round(item[2], 2)))
        total_price += item[2]
    print ("%r ounces of food per person" % meal_plan.get('ounces_per_person'))
    print ("total cost: $%r" % round(total_price, 2))


if __name__ == '__main__':
    main()
