# Sistema de Gestión para Taller Mecánico «LA RUEDA» — Módulo de Inventario de Repuestos

Repositorio del módulo desarrollado en la Unidad 3 de la asignatura Ingeniería de Software,
Carrera de Tecnologías de la Información, Universidad Estatal Amazónica.

## Datos del proyecto

| Dato | Detalle |
|---|---|
| Sistema | Sistema de Gestión para Taller Mecánico «LA RUEDA» |
| Módulo implementado | Gestión de inventario de repuestos |
| Grupo | Grupo 13 |
| Integrantes | Edison Paul Llerena Cuzco |
| Docente | Ing. Hermes Darío Sánchez Bermeo |
| Stack | Python 3.11 + Django · SQLite en desarrollo · pytest · GitHub Actions |

## Qué hace el módulo

El módulo administra las existencias de repuestos del taller. Permite registrar un repuesto con
su código, nombre, precio de compra, precio de venta y cantidad en stock; descuenta las unidades
de forma automática cuando el repuesto se consume en una orden de trabajo; y emite una alerta
cuando la cantidad disponible llega al nivel mínimo definido.

Requerimientos del mini SRS que atiende:

- **RF-09** — Registrar repuestos con código, nombre, precio de compra, precio de venta y cantidad en stock.
- **RF-10** — Restar automáticamente el stock cada vez que se utiliza un repuesto en una orden de trabajo.
- **RF-11** — Mostrar una alerta cuando el stock de un repuesto llegue al nivel mínimo definido.
- Da soporte a **RF-07** (agregar repuestos y servicios a la orden de trabajo).

## Estructura del repositorio

```
taller-la-rueda-inventario/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   └── inventario/
│       ├── __init__.py
│       ├── modelo.py         # Entidad Repuesto (capa de datos del dominio)
│       ├── repositorio.py    # Patrón DAO: único punto de acceso a los datos
│       └── servicio.py       # Capa de lógica de negocio: descuento de stock y alerta
├── tests/
│   └── test_inventario.py    # Pruebas (se completan en los avances 3 y 4)
├── docs/
│   └── matriz_decision_tecnologica_U3.xlsx   # Evidencia del Avance 1
└── .github/
    └── workflows/
        └── ci.yml            # Pipeline de integración continua
```

La separación entre `modelo.py`, `repositorio.py` y `servicio.py` conserva la arquitectura en
tres capas y el patrón DAO definidos en la Unidad 2: la lógica de negocio nunca accede
directamente a los datos, sino a través del repositorio.

## Flujo de ramas

Se trabaja con un flujo simple tipo **GitHub Flow**:

1. La rama `main` se mantiene siempre estable: solo recibe código que ya pasó por el pipeline.
2. Cada cambio se hace en una rama de trabajo propia, nombrada según lo que resuelve:
   - `feature/...` para una funcionalidad nueva (por ejemplo `feature/descuento-stock`).
   - `fix/...` para la corrección de un error.
   - `docs/...` para cambios de documentación.
3. Los commits son pequeños y su mensaje describe el cambio en presente
   (`Agrega validación de stock mínimo`), no de forma genérica.
4. La rama se integra a `main` mediante un **pull request**, nunca con un merge directo.
   El pull request se fusiona solo cuando el pipeline muestra el check verde.
5. Una vez fusionada, la rama de trabajo se elimina.

Comandos habituales:

```bash
git checkout main
git pull origin main
git checkout -b feature/descuento-stock
git add .
git commit -m "Agrega el descuento automático de stock"
git push origin feature/descuento-stock
# En GitHub: abrir el pull request hacia main
```

## Integración continua

El archivo `.github/workflows/ci.yml` define un pipeline que se ejecuta en cada `push` y en cada
`pull request`. En este avance verifica que el proyecto se instale y que el código compile sin
errores de sintaxis. En el Avance 4 (Semana 12) se agregará la ejecución automática de las
pruebas con `pytest`.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```
Módulo en construcción — Avance 2, Unidad 3.
