import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def test_chi2(df, var1, var2, alpha=0.05):
   
    tabla = pd.crosstab(df[var1], df[var2])
    print(tabla, "\n")

    chi2, p, dof, expected = chi2_contingency(tabla)
    esp = pd.DataFrame(expected, index=tabla.index, columns=tabla.columns)

    print(f"Chi-cuadrado = {chi2:.4f}")
    print(f"p-valor      = {p:.4f}")
    print(f"gl           = {dof}")
    print("Frecuencias esperadas:")
    print(esp.round(2), "\n")

    # Aviso si hay celdas con esperado < 5
    if (expected < 5).any():
        print("Aviso: hay celdas con frecuencia esperada < 5.")
        if tabla.shape == (2, 2):
            odds, p_fisher = fisher_exact(tabla)
            print(f"Se recomienda Fisher exact: p = {p_fisher:.4f}")

    if p < alpha:
        print(f"-> p < {alpha}: Rechazo H0. Las variables ESTÁN asociadas.")
    else:
        print(f"-> p >= {alpha}: No se rechaza H0. No hay evidencia de asociación.")

    return chi2, p, dof, esp

# Uso:
# test_chi2(df, 'sex', 'smoker')
# test_chi2(df, 'day', 'time')

#-----------------------
def cardinalidad(df_in: pd.DataFrame, umbral_categoria: int, umbral_continua: float) -> pd.DataFrame:
    resultados = []

    n_filas = len(df_in)

    for col in df_in.columns:
        valores_unicos = df_in[col].nunique(dropna=False)
        porcentaje = valores_unicos / n_filas

        if valores_unicos == 2:
            tipo = "Binaria"
        elif valores_unicos < umbral_categoria:
            tipo = "Categórica"
        else:
            if porcentaje >= umbral_continua:
                tipo = "Numerica Continua"
            else:
                tipo = "Numerica Discreta"

        resultados.append({
            "columna": col,
            "cardinalidad": valores_unicos,
            "porcentaje_cardinalidad": porcentaje,
            "tipo": tipo
        })

    return pd.DataFrame(resultados)
#-----------------------

#-----------------------
def plot_categorical_relationship_fin(df, cat_col1, cat_col2, relative_freq=False, show_values=False, size_group = 5):
    # Prepara los datos
    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name='count')
    total_counts = df[cat_col1].value_counts()
    
    # Convierte a frecuencias relativas si se solicita
    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis=1)

    # Si hay más de size_group categorías en cat_col1, las divide en grupos de size_group
    unique_categories = df[cat_col1].unique()
    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=data_subset, order=categories_subset)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {cat_col1} y {cat_col2} - Grupo {i + 1}')
            plt.xlabel(cat_col1)
            plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de size_group categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=count_data)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {cat_col1} y {cat_col2}')
        plt.xlabel(cat_col1)
        plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()
#-----------------------