import pandas as pd
import numpy as np
from datetime import timedelta, date


# Initial Settings
start_date = date(2014, 1, 1)
end_date = date(2023, 12, 31)
employees = ["Peter", "Anna", "Tom", "Richard", "Josh", "Beatrice", "Noah", "Oliver", "Olivia", "Ava"]
categories = {"Peter": "Categoria A", "Anna": "Categoria B", "Tom": "Categoria C", "Richard": "Categoria A",
              "Josh": "Categoria D", "Beatrice": "Categoria B", "Noah": "Categoria C", "Oliver": "Categoria D",
              "Olivia": "Categoria A", "Ava": "Categoria B"}
satisfaction_levels = ["Satisfeito", "Neutro", "Insatisfeito"]
base_values = {"Ram 3500": 534990, "Corvette Z06": 1700000, "Porsh 911": 1700000, "Bentley Batur": 950000, "Audi TT": 500000,
               "Ducati Superleggera V4": 700000, "BMW HP4 Race": 495000, "Harley-Davidson CVO": 200000, "Honda Gold Wing ": 150000, "Kawasaki Ninja H2": 140000}

# Generate business days within the range of days
dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Frequência 'B' considera apenas dias úteis

# Create data lists
data = []
for current_date in dates:
    for employee in employees:

        # Randomly selecting the product sold and the seller's satisfaction on the day of purchase
        product = np.random.choice(list(base_values.keys()))
        satisfaction = np.random.choice(satisfaction_levels)

        # Retrieving the value of the product sold and the employee's category
        # AThe employee's category could have been defined directly as was done for the product, through the dictionary
        # However, the idea is to implement different methods and tools in this project
        base_value = base_values[product]
        category = categories[employee]
        
        # Mapping categories to sales intervals
        category_mapping = {"Categoria A": (1, 4), "Categoria B": (1, 2), "Categoria C": (0, 2), "Categoria D": (0, 2)}

        # Defining the influence of the category on sales
        # The use of the asterisk * unpacks the tuple
        num_products_sold = 0  
        if category in category_mapping:
            num_products_sold = np.random.randint(*category_mapping[category]) 

        # Add to the file only if there is a sale
        if num_products_sold != 0:
            total_sales_value = int(num_products_sold * base_value)
            data.append([current_date, employee, category, satisfaction, product, base_value, num_products_sold, total_sales_value])
       

# Create DataFrame
df = pd.DataFrame(data, columns=["Data", "Nome do Funcionario", "Categoria do Funcionário",
                                 "Satisfação", "Produto Vendido", "Valor do Produto", "Quantidade Vendida", "Valor da Venda"])


# Save DataFrame to a CSV file separated by columns (sep=";") and without the DataFrame index
df.to_csv("dados_vendas.csv", sep=";", index=False)
