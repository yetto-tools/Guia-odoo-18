# Día 29 — Portafolio y preparación de certificación

**Semana:** 4 — Calidad, performance y profesionalización
**Duración estimada:** 2–3 h

## Objetivo del día
Dejar el proyecto presentable como portafolio público, y mapear qué de todo lo aprendido corresponde a una certificación técnica.

---

## Conceptos de Odoo

### Qué hace que un README de módulo Odoo sea útil, específicamente
Un README genérico de "instalar y listo" no comunica lo importante para alguien evaluando tu trabajo (un reclutador, otro desarrollador, un potencial cliente): qué **decisiones de diseño** tomaste y por qué. Para un módulo de portafolio, importa mostrar no solo que "funciona", sino que entendiste los trade-offs — por ejemplo, mencionar por qué elegiste `store=True` en un campo específico, o por qué la seguridad tiene dos grupos en vez de uno, comunica competencia real, más allá de una lista de funcionalidades.

### Qué evalúa realmente una certificación técnica de Odoo
Las certificaciones técnicas de Odoo están diseñadas para validar exactamente las competencias centrales de un desarrollador Odoo funcional en el día a día: modelado de datos con el ORM, vistas, seguridad, herencia, lógica de negocio con `@api.constrains`/`@api.onchange`/campos computados. No es casualidad que las semanas 1 a 3 de esta guía cubran ese mismo territorio — es, deliberadamente, el núcleo transferible de conocimiento de Odoo, independiente de qué módulo específico termines desarrollando en tu carrera.

### Por qué un video/GIF corto comunica más que texto
Alguien evaluando 20 portafolios distintos no va a instalar tu módulo para probarlo. Un GIF de 60-90 segundos mostrando el flujo principal funcionando reduce la fricción de evaluación a cero — es la diferencia entre "puede que esto funcione" y "vi que funciona, con mis propios ojos, en 60 segundos".

### El código es el 50% del portafolio; la presentación es el otro 50%
Dos módulos técnicamente equivalentes, uno con README pobre y sin capturas, otro bien documentado y con demo visual, comunican niveles de profesionalismo completamente distintos a quien los evalúa — aunque el código sea idéntico en calidad. Invertir tiempo en la presentación no es "trabajo extra innecesario": es parte de completar el trabajo.

---

## Ejercicios prácticos

### Ejercicio 1 — README completo (guiado)

Estructura sugerida:
1. **Descripción** — qué problema resuelve el módulo.
2. **Funcionalidades** — lista de lo implementado (propiedades, ofertas, wizard de venta, reportes, portal público, etc.).
3. **Instalación** — pasos para levantarlo (docker-compose, comando de instalación).
4. **Capturas** — 2-3 screenshots de las pantallas principales.
5. **Stack técnico** — Odoo 18, PostgreSQL 15, OWL, etc.

Escribí el README de `gestion_inmobiliaria` siguiendo esta estructura, creá un repositorio público en GitHub, y subí el módulo completo.

### Ejercicio 2 — Agregar una sección de "decisiones de diseño"
1. Sumá al README una sección corta (5-8 bullets) explicando decisiones no obvias que tomaste durante las 4 semanas: por qué ciertos campos son `store=True` y otros no, por qué la seguridad tiene 2 grupos con esa jerarquía específica, por qué elegiste wizard en vez de un botón directo para confirmar la venta.
2. Esta sección es la que más comunica competencia real — priorizala sobre agregar más capturas.

### Ejercicio 3 — Mapear tu progreso contra el temario de certificación técnica
1. Repasá el índice completo de los 30 días de esta guía (`GUIA-ODOO18-30-DIAS.md`).
2. Marcá qué temas corresponden, a tu criterio, al núcleo de una certificación técnica (modelos, vistas, seguridad, herencia, lógica de negocio) versus qué temas son extensiones más allá de lo "básico certificable" (website, OWL, deployment, OCA).
3. Esto te da un mapa realista de qué repasar con más profundidad si pensás rendir una certificación pronto.

### Ejercicio 4 — Pedir revisión de otra persona
1. Si es posible, pedile a otra persona (con o sin experiencia en Odoo) que lea tu README sin ver el código, y te diga en sus propias palabras qué hace el módulo.
2. Si su descripción no coincide con lo que vos querías comunicar, el README necesita ajustes — es una señal más confiable que releerlo vos mismo.

### Ejercicio 5 — Reto: grabar la demo
Grabá un GIF o video corto (1-2 minutos) mostrando el flujo completo: crear propiedad → recibir oferta → aceptar oferta → confirmar venta → imprimir reporte. Subilo al repositorio (o a un servicio de hosting de video/GIF) y enlazalo desde el README.

---

## Preguntas de repaso conceptual

1. ¿Qué comunica una sección de "decisiones de diseño" en un README que una simple lista de funcionalidades no comunica?
2. ¿Por qué el núcleo de una certificación técnica de Odoo coincide, en gran parte, con el contenido de las semanas 1-3 de esta guía y no tanto con temas como website u OWL?
3. ¿Qué problema práctico resuelve incluir un GIF o video corto en el README, frente a solo texto y capturas estáticas?
4. ¿Por qué "el código funciona" no es suficiente para un portafolio competitivo?
5. ¿Qué señal más confiable que "releer tu propio README" podés usar para validar que comunica bien lo que el módulo hace?

<details>
<summary>Ver respuestas</summary>

1. Comunica que entendiste los trade-offs de tus decisiones técnicas (por qué elegiste X en vez de Y), lo cual demuestra criterio y comprensión profunda, no solo capacidad de seguir un tutorial paso a paso.
2. Porque son las competencias centrales y transferibles de cualquier desarrollador Odoo, sin importar en qué módulo específico termine trabajando — modelado de datos, vistas, seguridad y lógica de negocio son la base que se reutiliza en absolutamente todo desarrollo Odoo, mientras que website/OWL son especializaciones más puntuales.
3. Reduce a cero la fricción de evaluación: quien revisa tu portafolio no necesita instalar nada para confirmar que el flujo funciona, lo ve directamente en unos segundos.
4. Porque la presentación (documentación clara, demo visible, decisiones explicadas) es lo que le permite a un tercero evaluar tu trabajo sin tener que invertir tiempo propio en descubrirlo por su cuenta — dos módulos técnicamente equivalentes comunican niveles de profesionalismo muy distintos según cómo estén presentados.
5. Pedirle a otra persona que lea el README (sin ver el código) y describa en sus propias palabras qué hace el módulo — si su descripción no coincide con la intención, es una señal objetiva de que el texto necesita ajustes.

</details>

## Checklist de cierre
- [ ] El README explica el "qué" y el "por qué", no solo lista archivos.
- [ ] Agregué la sección de decisiones de diseño.
- [ ] El repositorio es accesible públicamente (lo probé en una ventana de incógnito).
- [ ] Grabé y enlacé un GIF o video corto mostrando el módulo funcionando.
