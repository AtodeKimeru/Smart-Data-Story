# Smart-Data-Story
[Fusion Hackaton Data 2025](https://www.gdcfusion.org/)

## Objetivo del proyecto
En este proyecto implementamos un pipeline automático basado en Medallion Architecture (Bronze, Silver, Gold) orquestado con Mage.ai para comparar, al menos en dos momentos clave, el impacto de herramientas de CI/CD sobre la dinámica de los repositorios. Como piloto hemos elegido GitHub Actions, midiendo la correlación entre el número de eventos de cierre de issues (IssueEvent con action: closed) y los eventos de lanzamiento de versiones (ReleaseEvent). Gracias a la automatización, este flujo es totalmente parametrizable y fácilmente replicable para cualquier otra herramienta o fecha de interés, garantizando un análisis continuo y escalable de la adopción tecnológica en proyectos de código abierto.
## Nuestra demo
Para la prueba de concepto tomamos dos fechas relativas al lanzamiento de GitHub Actions (13 de noviembre de 2019): un día antes y un año después. El pipeline descarga los datos crudos de GH Archive, los transforma en Snowflake mediante DBT en capas Silver y Gold, y calcula el coeficiente de Pearson junto con métricas de “lanzamientos por issue resuelto”. Todo el proceso se dispara automáticamente con Mage.ai, y los resultados se visualizan en dashboards que evidencian cómo la adopción de Actions ha afectado la eficiencia de los flujos de trabajo.
