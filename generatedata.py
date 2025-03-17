import pandas as pd
import numpy as np
import os

# Ensure the 'Project' folder exists
os.makedirs('Project', exist_ok=True)

# Set random seed for reproducibility and define number of rows
np.random.seed(42)
n = 1000

# Define possible values for categorical columns
categories = ['A', 'B', 'C', 'D']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# Generate sample data
data = {
    'Category': np.random.choice(categories, n),
    'Month': np.random.choice(months, n),
    'Sales': np.random.uniform(100, 1000, n).round(2),
    'Profit': np.random.uniform(10, 300, n).round(2)
}

# Create DataFrame and save to Excel in the Project folder
df = pd.DataFrame(data)
excel_path = os.path.join('Project', 'sampledata.xlsx')
df.to_excel(excel_path, index=False)
print(f"Sample data generated at {excel_path}")
