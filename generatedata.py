import pandas as pd
import numpy as np
import os

os.makedirs('Project', exist_ok=True)

np.random.seed(42)
n = 1000

categories = ['Electronics', 'Food', 'Clothes', 'Furniture']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


data = {
    'Category': np.random.choice(categories, n),
    'Month': np.random.choice(months, n),
    'Sales': np.random.uniform(100, 1000, n).round(2),
    'Profit': np.random.uniform(10, 300, n).round(2)
}


df = pd.DataFrame(data)
excel_path = os.path.join('Project', 'sampledata.xlsx')
df.to_excel(excel_path, index=False)
print(f"Sample data generated at {excel_path}")
