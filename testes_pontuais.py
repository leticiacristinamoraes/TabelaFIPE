import pandas as pd
import sys
import os
from datetime import date , timedelta
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath("app"))
from app.database.prices import count_inputs_researcher


# tabela = count_inputs_researcher(3, '2024-12-01', '2024-12-31')
# #print(tabela[0][0])
# df = pd.DataFrame(tabela, columns=['Data', 'Quantidade'])
# df.plot(x='Data', y='Quantidade', kind='bar')

today = date.today()  # 2024-03-28
month, year = [today.month-1, today.year] if today.month > 1 else [12, today.year-1]
