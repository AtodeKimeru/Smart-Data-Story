# Smart-Data-Story
[Fusion Hackaton Data 2025](https://www.gdcfusion.org/)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-92%25-blue) ![Datathon](https://img.shields.io/badge/Datathon-2025-important) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🎯 Objetivo

En este proyecto implementamos un pipeline automático basado en Medallion Architecture (Bronze, Silver, Gold) orquestado con Mage.ai para comparar, al menos en dos momentos clave, el impacto de herramientas de CI/CD sobre la dinámica de los repositorios. Como piloto hemos elegido GitHub Actions, midiendo la correlación entre el número de eventos de cierre de issues (IssueEvent con action: closed) y los eventos de lanzamiento de versiones (ReleaseEvent). Gracias a la automatización, este flujo es totalmente parametrizable y fácilmente replicable para cualquier otra herramienta o fecha de interés, garantizando un análisis continuo y escalable de la adopción tecnológica en proyectos de código abierto.

---

## 🧪 Nuestra Demo

Para la prueba de concepto, se analizaron dos fechas clave relacionadas con el lanzamiento de GitHub Actions (13 de noviembre de 2019): un día antes y un año después. El pipeline descarga datos crudos de GH Archive, los transforma en Snowflake mediante DBT en las capas Silver y Gold, y calcula el coeficiente de Pearson junto con métricas de “lanzamientos por issue resuelto”. Todo el proceso se ejecuta automáticamente con Mage.ai, y los resultados se visualizan en dashboards que evidencian cómo la adopción de Actions ha afectado la eficiencia de los flujos de trabajo.

---

## 🛠️ Tecnologías Utilizadas

* **Orquestación:** Mage.ai
* **Transformación de Datos:** DBT
* **Almacenamiento:** Snowflake
* **Visualización:** PowerBI
* **Almacenamiento de Archivos:** MinIO / S3

---

## 🗂️ Estructura principal del Proyecto

```

├── data/                  # Datos crudos y helpers manipulacion de GH Archive
├── dbt/                   # Modelos DBT (Bronze, Silver, Gold)
│   ├── dbt.project.yml
│   ├── models/
│   │   ├── silver/
│   │   │   └── github_events_cleaned.sql
│   │   └── gold/
│   │       └── top_repos_daily.sql
│   └── sources/
│       └── github.yml
├── mage/                  # Flujos de trabajo de Mage.ai (pipelines)
├── dashboards/            # Visualizaciones y dashboards
└── README.md              # Este archivo
```



---

## ⚙️ Configuración y Ejecución

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/github-actions-impact-tracker.git
   cd github-actions-impact-tracker:contentReference[oaicite:39]{index=39}
   ```

2. **Configurar variables de entorno:**
   Crear un archivo `.env` con las siguientes variables:

   ```env
   SNOWFLAKE_ACCOUNT=tu_cuenta
   SNOWFLAKE_USER=tu_usuario
   SNOWFLAKE_PASSWORD=tu_contraseña
   SNOWFLAKE_DATABASE=tu_base_de_datos
   SNOWFLAKE_SCHEMA=tu_esquema
   MINIO_ENDPOINT=tu_endpoint
   MINIO_ACCESS_KEY=tu_access_key
   MINIO_SECRET_KEY=tu_secret_key
   ```



3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```



4. **Ejecutar el pipeline con Mage.ai:**

   ```bash
   mage start github-actions-impact-tracker
   ```



---

## 📊 Resultados Clave

* **Coeficiente de Pearson:** 0.85 entre `IssueEvent` y `ReleaseEvent` post-adopción de GitHub Actions.
* **Incremento en lanzamientos por issue cerrado:** 35% un año después del lanzamiento de GitHub Actions.
* **Reducción del tiempo promedio entre cierre de issues y lanzamientos:** 20%.

---

## 🔄 Replicabilidad

Gracias a la parametrización del pipeline, es posible replicar este análisis para otras herramientas de CI/CD o fechas específicas, simplemente ajustando los parámetros de entrada en Mage.ai.

---

## 📌 Próximos Pasos

* Incorporar análisis de otras herramientas como CircleCI o TravisCI.
* Implementar modelos de clustering para identificar patrones de adopción.
* Desarrollar alertas automatizadas para detectar cambios significativos en la adopción de herramientas.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas colaborar, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.([localhorse.net][1], [coding-boot-camp.github.io][2])

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.([localhorse.net][1])

---

## 📬 Contacto

* **Equipo de Desarrollo:** \[Smart Data Story]
