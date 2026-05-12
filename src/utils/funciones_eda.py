import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact

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