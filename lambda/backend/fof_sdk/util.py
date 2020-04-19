import random
import datetime


iso_formatted_date_today = datetime.date.today().isoformat()
"""
YYYY-mm-dd
"""

follower_table = {'SS': 10,
                  'S': 9,
                  'A': 8,
                  'B': 7,
                  'C': 6,
                  'D': 5
                  }


def gacha():
    return random.choices(['SS', 'S', 'A', 'B', 'C', 'D'],
                          weights=[0.1, 0.5, 5, 20, 30, 44.4])[0]
