<p align="center">
  <img src="src/img/logo.png" alt="Trazos y Hojas" width="300"/>
</p>

<h1 align="center">Gestión Inteligente de Compras — EDA Trazos y Hojas</h1>

<p align="center">
  Análisis Exploratorio de Datos sobre costos, márgenes y valor en el inventario de una papelería madrileña.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-4a7c59?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-2.x-4a7c59?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-3.x-6b9e6e?style=flat-square"/>
  <img src="https://img.shields.io/badge/Seaborn-0.13-6b9e6e?style=flat-square"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-c8a951?style=flat-square&logo=jupyter&logoColor=white"/>
</p>

---

## Descripción del proyecto

**Trazos y Hojas** es una papelería ubicada en la zona centro-norte de Madrid que opera a través de dos canales: una tienda física con TPV y la plataforma de delivery **Glovo**. El negocio gestiona un catálogo de 862 artículos que incluye material de oficina, escritura, copistería, manualidades y productos escolares.

Este proyecto realiza un **análisis exploratorio de datos (EDA)** sobre los registros de ventas del periodo comprendido entre el **1 de enero y el 8 de mayo de 2026** (94 días de actividad), con el objetivo de transformar los datos operativos en decisiones concretas de negocio: identificar qué productos impulsan la rentabilidad, detectar errores de precios y entender el comportamiento de compra por franja horaria y canal.

---

## Hipótesis planteadas

| # | Hipótesis | Resultado |
|---|-----------|-----------|
| H1 | Los 5 productos más vendidos por volumen son también los que mayor margen absoluto aportan al negocio. | ❌ Rechazada |
| H2 | La existencia de productos con margen negativo se debe a que los precios han sido establecidos incorrectamente. | ✅ Confirmada |
| H3 | El comportamiento de ventas varía significativamente entre categorías según la hora del día. | ✅ Confirmada |
| H4 | Las ventas a través de Glovo representan una proporción significativa de las ventas globales. | ❌ Rechazada |

---

## Tecnologías utilizadas

- **Python 3.10+** — lenguaje principal del análisis
- **Pandas** — limpieza, transformación y agrupación de datos
- **Matplotlib / Seaborn** — visualizaciones estáticas
- **Jupyter Notebook** — entorno de desarrollo y presentación del análisis

---

## Estructura del repositorio

```
EDA_Trazos_y_Hojas/
│
├── src/
│   ├── data/
│   │   ├── agrupacion_horas.csv      # Ventas por franja horaria (24 franjas x 94 días)
│   │   ├── cierre_caja.csv           # Ventas diarias totales (94 días)
│   │   ├── compras_articulos.csv     # Catálogo con márgenes por producto (862 artículos)
│   │   ├── compras_tpv.csv           # Líneas de venta individuales TPV (7.615 líneas)
│   │   └── ventas_glovo.csv          # Ventas canal Glovo (59 productos)
│   │
│   ├── img/
│   │   └── logo.png                  # Logo de la papelería
│   │
│   ├── notebooks/                    # Notebooks de desarrollo y exploración
│   │
│   └── utils/                        # Funciones auxiliares y helpers
│
├── main.ipynb                        # Versión final y limpia del EDA completo
├── Memoria.pdf                       # Documento técnico
├── Presentacion.pdf                  # Diapositivas utilizadas en el vídeo
├── .gitignore
└── README.md
```



---

## Instrucciones de reproducción

**1. Clonar el repositorio**

```bash
git clone https://github.com/alimadriz0110/EDA_Trazos_y_Hojas.git
cd EDA_Trazos_y_Hojas
```

**2. Instalar las dependencias**

```bash
pip install pandas matplotlib seaborn jupyter
```

**3. Lanzar el notebook**

```bash
jupyter notebook main.ipynb
```

> Los datasets deben estar ubicados en la carpeta `data/` con los nombres exactos indicados en la estructura del repositorio.

---

## Principales conclusiones

**Estructura de ventas**

La actividad comercial sigue un patrón bimodal con picos en las franjas 10-13h (copistería y oficina) y 17-19h (papelería escolar y manualidades). La franja de 14-16h registra actividad mínima, lo que representa una posible oportunidad de horario extendido. Glovo representa solo el 1,7% de las transacciones totales (129 pedidos frente a 7.486 en tienda), aunque con un ticket medio significativamente superior: 4,67 € frente a 1,89 €.

**Rentabilidad por producto**

Los 5 productos más vendidos en volumen (principalmente fotocopias) no coinciden con los 5 más rentables en margen absoluto: juntos representan el 36,8% del margen total frente al 0,1% de los 5 últimos. En Glovo, Blocs y Navigator son las categorías más eficientes, con márgenes del 82% y 50% respectivamente usando muy pocos productos. El catálogo de Pilot está sobredimensionado: 12 referencias con menos ventas que Navigator con 3.

**Productos con margen negativo**

Solo 8 de 862 artículos (menos del 1%) presentan margen negativo. Todos los casos son corregibles: errores de imputación de descuentos o precios de venta inferiores al coste registrado en el sistema. El mayor impacto individual es de -9,29 € (A4 Doble Cara Color Cartulina).

---

## Autores

| Nombre | GitHub |
|--------|--------|
| Raquel Martine | [@raquelmg1312](https://github.com/raquelmg1312) |
| Ali Manuel Madriz Valero | [@alimadriz0110](https://github.com/alimadriz0110) |

---

*Proyecto desarrollado como ejercicio de análisis exploratorio de datos con datos reales de negocio.*
