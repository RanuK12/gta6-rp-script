# Elección de Idea para Script Premium FiveM

## Tabla Comparativa de Candidatas

| Candidata | Release Posts | Precio (USD) | Replies/Views | Última Actividad | Demanda (1-5) | Saturación (1-5) | Factibilidad (1-5) | Stack Fit (1-5) | Techo Precio (1-5) | **Total** |
|-----------|---------------|--------------|---------------|------------------|---------------|------------------|-------------------|-----------------|-------------------|-----------|
| **Hitman Contracts** | 0 | 0 (free) | N/A | **2025-09-15** | 3 | **5** (pocos releases) | 4 | 5 | 4 | **21** |
| **Immersive Hospital** | 1 | N/A | N/A | **2025-08-24** | 3 | 4 | 3 | 4 | 3 | 17 |
| **Elite Tuners** | 0 | N/A | N/A | **2025-08-14** | 3 | 4 | 4 | 5 | 3 | 19 |
| **Fishing & Maritime** | 0 | 0 (free) | N/A | **2025-07-30** | 2 | 4 | 3 | 4 | 2 | 15 |
| **Cartel Economy** | 0 | 0 (free) | N/A | 2024-05-17 | 2 | 4 | 3 | 5 | 2 | 16 |
| **Gang Territory** | 0 | 0 (free) | N/A | 2024-05-07 | 2 | 4 | 3 | 5 | 2 | 16 |
| **Housing 2.0 Physics** | 0 | N/A | N/A | 2025-04-13 | 2 | 3 | 2 | 4 | 3 | 14 |
| **Prison Break** | 1 | 0 (free) | N/A | 2023-05-24 | 2 | 3 | 2 | 4 | 2 | 13 |
| **Celebrities/Influencers** | 0 | N/A | N/A | 2025-03-01 | 1 | 4 | 2 | 3 | 2 | 12 |
| **NPC Memory & AI** | 0 | N/A | N/A | N/A (sin resultados) | 1 | **5** (vacío) | **1** (requiere LLM backend, costos API, latencia, fallback offline complejo) | 2 | 2 | **11** |

**Puntuación**: 1 = bajo/malo, 5 = alto/bueno. Para Saturación: 5 = poca competencia (pocos releases), 1 = muy saturado.

---

## **Chosen: Hitman Contracts**

### Justificación

**Hitman Contracts** encabeza el scoring (21/25) por combinar **demanda comprobada** (thread activo sept 2025), **baja saturación** (cero releases de pago visibles), **factibilidad alta** (ESX standalone, sin dependencias externas pesadas), **encaje perfecto** con el stack ESX+QB/ox_lib/oxmysql/escrow, y **techo de precio atractivo** (scripts de contratos/asesinatos en Tebex se venden $25–45). El thread "Hitman Contracts ESX Standalone" (5352887) muestra actividad reciente y es gratuito, lo que valida que la mecánica interesa a dueños de servidores; la versión premium con contratos persistentes, reputación, variedad de targets y anti-cheat escrow cubre el gap de monetización.

### Por qué NO las otras 9

- **NPC Memory & AI**: Sin resultados en forum.cfx.re; requiere backend LLM (costos API recurrentes por servidor, latencia, fallback offline) — inviable para un script vendido como asset standalone.
- **Housing 2.0 Physics**: Thread único sin precio claro, actividad 2025-04; physics en FiveM es frágil y propenso a desync, alto riesgo técnico.
- **Cartel Economy**: Solo sistema de drogas free (2024-05), mercado saturado de "drug scripts" gratuitos; diferenciar requiere economía compleja y balanceo continuo.
- **Gang Territory**: Free release 2024-05, competencia establecida (GL Territories); territorio es feature core de muchos frameworks, difícil cobrar premium.
- **Elite Tuners**: Buen encaje stack y actividad reciente, pero tuning shops son commodity; techo de precio menor ($15–25) y requiere modelado 3D/vehicles custom.
- **Immersive Hospital**: Un release 2025-08 valida nicho, pero RP médico es nicho de nicho; servidor promedio no prioriza hospital sobre jobs/crimen.
- **Celebrities/Influencers**: Referral system para streamers (2025-03), dependiente de meta externa (Twitch/YouTube), audiencia reducida.
- **Fishing & Maritime**: Free advanced fishing 2025-07, actividad decente pero precio techo bajo ($10–20); pesca es side-activity, no core loop.
- **Prison Break**: Free release 2023 (stale >2 años), jailbreak mecánica limitada; servidores usan jail nativo de ESX/QB, poco incentivo a pagar.