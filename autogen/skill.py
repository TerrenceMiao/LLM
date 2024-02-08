"""
Add skills to AutoGen Studio Agents

References

- AutoGen Fully Local ... And Without Coding https://www.ai-for-devs.com/products/autogen-fully-local-and-without-coding
"""

from typing import List, Dict, Optional


def get_inventory():
    """
    Perform a inventory search and returns a list of spare parts including the name and price.

    :return: A list of the available spare parts. Example output: [{'part_id': 1, 'part_name': 'Tesla Windshield', 'quantity': 10, 'price': 1500}, {'part_id': 2, 'part_name': 'Porsche Tire', 'quantity': 50, 'price': 750}, {'part_id': 3, 'part_name': 'Porsche Brake Pad', 'quantity': 100, 'price': 300}, {'part_id': 4, 'part_name': 'Tesla Display', 'quantity': 5, 'price': 2000}, {'part_id': 5, 'part_name': 'Tesla Bumper', 'quantity': 5, 'price': 2000}]
    """

    inventory_list = [
        {"part_id": 1, "part_name": "Tesla Windshield", "quantity": 10, "price": 1500},
        {"part_id": 2, "part_name": "Porsche Tire", "quantity": 50, "price": 750},
        {"part_id": 3, "part_name": "Porsche Brake Pad", "quantity": 100, "price": 300},
        {"part_id": 4, "part_name": "Tesla Display", "quantity": 5, "price": 2000},
        {"part_id": 5, "part_name": "Tesla Bumper", "quantity": 5, "price": 2000},
    ]

    return inventory_list


print(get_inventory())
