import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/format_size_comparation.csv')

X = df.index
plt.plot(X, df['ISO'], color='r', label='ISO')
plt.plot(X, df['PB'], color='g', label='Protocol Buffer')
plt.plot(X, df['XYT'], color='b', label='XYT')
plt.plot(X, df['JSON'], color='y', label='JSON')


plt.xlabel("Minúcias")
plt.ylabel("Tamanho do Arquivo(bytes)")
plt.title("Comparação entre diferentes formas de armazenar minúcias")
  
# Adding legend, which helps us recognize the curve according to it's color
plt.legend()
  
# To load the display window
plt.savefig('images/plots/formatSizeComparation.png')
