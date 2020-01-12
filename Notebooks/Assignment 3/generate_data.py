import numpy as np
import pandas as pd

students = 250
nr_to_label = {0: 'bike', 1: 'car', 2: 'bus 40', 3: 'bus 240'}
label_to_nr = {v: k for k, v in nr_to_label.items()}


def choice(income, distance, lazy):
    """
    Generate a choice based on the params
    """
    if income < 500:
        if distance < 8 and distance * lazy * lazy < 120:
            return label_to_nr['bike']
        elif income > 350:
            return label_to_nr['bus 40']
        else:
            return label_to_nr['bus 240']
    if lazy < 3:
        return label_to_nr['bus 40']
    return label_to_nr['car']

# generate some random numbers
idc = np.array([np.round(np.random.normal(300, 200, size=students).clip(min=0)),
                np.random.poisson(8, size=students),
                np.random.randint(1, 10, size=students)]).T

# get their favourite mode of transport
idct = np.hstack((idc, np.array([[choice(*row) for row in idc]]).T))

# add some randomness by shuffling some labels
replace = np.where(np.random.random(size=students) < 0.15)[0]
idct[replace, 3] = np.random.randint(0, 4, size=replace.size)

# store result
df = pd.DataFrame(idct, columns=['income', 'distance', 'lazy', 'transport'])
df['transport'] = df['transport'].map(nr_to_label)
df.to_csv('transport.csv', sep=';', encoding='utf-8')
