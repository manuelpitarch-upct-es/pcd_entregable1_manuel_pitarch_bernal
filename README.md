# Sistema de Gestión de Flota Imperial 🌌

Primera práctica entregable de la asignatura **Programación para Ciencia de Datos (2025/2026)**. El objetivo es un software de gestión de mantenimiento mecánico para la flota del Imperio Galáctico, implementado con técnicas de Programación Orientada a Objetos en Python.

---

## 📁 Contenido del Repositorio

| Archivo / Carpeta | Descripción |
|---|---|
| `codigov1.py` | Código principal con la lógica de naves, unidades de combate y almacenes |
| `tests.py` | Pruebas unitarias desarrolladas con `pytest` |
| `Diagramas_UML/` | Diagramas de clases, casos de uso y secuencia diseñados con UMLet |
| `Documentacion_Git.pdf` | Capturas de los comandos Git ejecutados y URL del repositorio |
| `image | Capturas de git añadidas al pdf |

---

## ⚙️ Cómo Funciona el Sistema

El software organiza la flota mediante los siguientes componentes:

- **Jerarquía de Naves** — Existen clases para `EstacionEspacial`, `NaveEstelar` y `CazaEstelar`, todas heredando de la clase abstracta `Nave`.
- **Unidades de Combate** — Las naves de combate aplican herencia múltiple heredando de `Nave` y de `UnidadCombate`, lo que permite el uso de identificadores y claves de transmisión cifrada.
- **Gestión de Almacén** — Los operarios mantienen un catálogo de repuestos. El stock de cada pieza es un atributo privado, protegido de modificaciones externas no autorizadas.
- **Mantenimiento** — Los comandantes solicitan piezas. El sistema valida si el repuesto es compatible con el catálogo específico de la nave antes de actualizar el stock.
- **Control de Errores** — Se gestionan excepciones personalizadas: `StockError`, `RepuestoNoEncontrado` e `IncompatibilidadError`.

---

## 🚀 Instrucciones de Ejecución

Clona el repositorio e instala las dependencias:
```bash
git clone https://github.com/manuelpitarch-upct-es/pcd_entregable1_manuel_pitarch_bernal.git
cd pcd_entregable1_manuel_pitarch_bernal
pip install pytest
```

Ejecuta el flujo principal:
```bash
python codigov1.py
```

Ejecuta las pruebas unitarias:
```bash
pytest tests.py -v
```

---



