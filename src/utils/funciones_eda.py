import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ── Paleta corporativa Trazos y Hojas ─────────────────────────────────────────
C_PRINCIPAL = '#2E5E1E'   # Verde bosque oscuro
C_NARANJA   = '#D97B3A'   # Naranja cálido
C_HOJA      = '#7CB87A'   # Verde hoja medio
C_TIERRA    = '#8B5E3C'   # Tierra/marrón cálido
C_AMARILLO  = '#C8A84B'   # Dorado/mostaza
C_BEIGE     = '#F2EBDD'   # Beige papel
C_BLANCO    = '#FAF8F2'   # Blanco roto

PALETA_CORPORATIVA = [C_PRINCIPAL, C_NARANJA, C_HOJA, C_TIERRA, C_AMARILLO]


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


# ─────────────────────────────────────────────────────────────────────────────
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
            tipo = "Numerica Continua" if porcentaje >= umbral_continua else "Numerica Discreta"

        resultados.append({
            "columna": col,
            "cardinalidad": valores_unicos,
            "porcentaje_cardinalidad": porcentaje,
            "tipo": tipo
        })

    return pd.DataFrame(resultados)


# ─────────────────────────────────────────────────────────────────────────────
def plot_categorical_relationship_fin(df, cat_col1, cat_col2, relative_freq=False, show_values=False, size_group=5):

    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name='count')
    total_counts = df[cat_col1].value_counts()

    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis=1)

    unique_categories = df[cat_col1].unique()

    def _draw(data_subset, order=None):
        plt.figure(figsize=(10, 6), facecolor=C_BLANCO)
        ax = sns.barplot(
            x=cat_col1, y='count', hue=cat_col2,
            data=data_subset, order=order,
            palette=PALETA_CORPORATIVA
        )
        ax.set_facecolor(C_BEIGE)
        plt.title(f'Relación entre {cat_col1} y {cat_col2}', color=C_PRINCIPAL, fontweight='bold')
        plt.xlabel(cat_col1, color=C_TIERRA)
        plt.ylabel('Frecuencia' if relative_freq else 'Conteo', color=C_TIERRA)
        plt.xticks(rotation=45, color=C_TIERRA)
        plt.yticks(color=C_TIERRA)
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}',
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10,
                            color=C_PRINCIPAL, xytext=(0, size_group),
                            textcoords='offset points')
        plt.tight_layout()
        plt.show()

    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))
        for i in range(num_plots):
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]
            _draw(data_subset, order=categories_subset)
    else:
        _draw(count_data)


# ─────────────────────────────────────────────────────────────────────────────
def plot_combined_graphs(df, columns, whisker_width=1.5, bins=None):
    num_cols = len(columns)
    if not num_cols:
        return

    fig, axes = plt.subplots(num_cols, 2, figsize=(12, 5 * num_cols), facecolor=C_BLANCO)
    if num_cols == 1:
        axes = np.array([axes])

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            # Histograma + KDE
            sns.histplot(
                df[column], kde=True,
                ax=axes[i, 0],
                bins="auto" if not bins else bins,
                color=C_PRINCIPAL,
                edgecolor=C_BLANCO,
                line_kws={"color": C_NARANJA, "linewidth": 2}
            )
            axes[i, 0].set_facecolor(C_BEIGE)
            axes[i, 0].set_title(f'Histograma y KDE de {column}', color=C_PRINCIPAL, fontweight='bold')
            axes[i, 0].tick_params(colors=C_TIERRA)

            # Boxplot
            sns.boxplot(
                x=df[column],
                ax=axes[i, 1],
                whis=whisker_width,
                color=C_HOJA,
                medianprops={"color": C_NARANJA, "linewidth": 2},
                boxprops={"edgecolor": C_TIERRA},
                whiskerprops={"color": C_TIERRA},
                capprops={"color": C_TIERRA},
                flierprops={"markerfacecolor": C_NARANJA, "marker": "o", "markersize": 5}
            )
            axes[i, 1].set_facecolor(C_BEIGE)
            axes[i, 1].set_title(f'Boxplot de {column}', color=C_PRINCIPAL, fontweight='bold')
            axes[i, 1].tick_params(colors=C_TIERRA)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
def pinta_distribucion_categoricas(df, columnas_categoricas, relativa=False, mostrar_valores=False):
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(15, 5 * num_filas), facecolor=C_BLANCO)
    axes = axes.flatten()

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]
        ax.set_facecolor(C_BEIGE)

        if relativa:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)
            ax.set_ylabel('Frecuencia Relativa', color=C_TIERRA)
        else:
            serie = df[col].value_counts()
            ax.set_ylabel('Frecuencia', color=C_TIERRA)

        sns.barplot(
            x=serie.index, y=serie, ax=ax,
            palette=PALETA_CORPORATIVA,
            hue=serie.index, legend=False
        )

        ax.set_title(f'Distribución de {col}', color=C_PRINCIPAL, fontweight='bold')
        ax.set_xlabel('', color=C_TIERRA)
        ax.tick_params(axis='x', rotation=45, colors=C_TIERRA)
        ax.tick_params(axis='y', colors=C_TIERRA)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}',
                            (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='center',
                            xytext=(0, 9), textcoords='offset points',
                            color=C_PRINCIPAL)

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
def grafico_dispersion_con_correlacion(df, columna_x, columna_y, tamano_puntos=60, mostrar_correlacion=False):

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=C_BLANCO)
    ax.set_facecolor(C_BEIGE)

    sns.scatterplot(
        data=df, x=columna_x, y=columna_y,
        s=tamano_puntos,
        color=C_PRINCIPAL,
        edgecolor=C_NARANJA,
        linewidth=0.6,
        ax=ax
    )

    if mostrar_correlacion:
        correlacion = df[[columna_x, columna_y]].corr().iloc[0, 1]
        ax.set_title(f'Diagrama de Dispersión  |  r = {correlacion:.2f}',
                     color=C_PRINCIPAL, fontweight='bold')
    else:
        ax.set_title('Diagrama de Dispersión', color=C_PRINCIPAL, fontweight='bold')

    ax.set_xlabel(columna_x, color=C_TIERRA)
    ax.set_ylabel(columna_y, color=C_TIERRA)
    ax.tick_params(colors=C_TIERRA)
    ax.grid(True, color='#D6CCBB', linewidth=0.6)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values=False, measure='mean'):

    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    grouped_data = grouped_data.sort_values(ascending=False)

    def _draw(data_subset):
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=C_BLANCO)
        ax.set_facecolor(C_BEIGE)
        sns.barplot(
            x=data_subset.index, y=data_subset.values,
            palette=PALETA_CORPORATIVA, ax=ax
        )
        ax.set_title(f'Relación entre {categorical_col} y {numerical_col}',
                     color=C_PRINCIPAL, fontweight='bold')
        ax.set_xlabel(categorical_col, color=C_TIERRA)
        ax.set_ylabel(f'{measure.capitalize()} de {numerical_col}', color=C_TIERRA)
        ax.tick_params(axis='x', rotation=45, colors=C_TIERRA)
        ax.tick_params(axis='y', colors=C_TIERRA)
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}',
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10,
                            color=C_PRINCIPAL, xytext=(0, 5),
                            textcoords='offset points')
        plt.tight_layout()
        plt.show()

    if grouped_data.shape[0] > 5:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / 5))
        for i in range(num_plots):
            categories_subset = unique_categories[i * 5:(i + 1) * 5]
            _draw(grouped_data.loc[categories_subset])
    else:
        _draw(grouped_data)