# Signal Lab Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the existing Vue + ECharts analytics workspace into a polished Signal Lab interface with a light data canvas, focused dark brand rail, stronger dashboard hierarchy, reference-inspired microinteractions, and reliable local export feedback.

**Architecture:** Keep the current Vue 3, Vite, Element Plus, ECharts, ECharts GL, GSAP, Axios, and Flask stack. Centralize visual tokens and chart semantics in the existing style system, extract only the new cross-page workspace and insight UI into focused Vue components, and keep existing chart components responsible for their own data requests. Reuse the existing `/summary`, `/nps`, and `/export` endpoints; do not add a new backend endpoint unless the current data cannot support the dashboard insight copy.

**Tech Stack:** Vue 3 Composition API, TypeScript, Vite, ECharts/ECharts GL, GSAP, Axios, Flask, existing Element Plus select primitives.

## Global Constraints

- Use a light data canvas with dark brand/navigation zones; chart plotting areas stay light.
- Use `#E56B55` for primary emphasis/risk, `#2E8B78` for positive signals, `#6E8190` for neutral data, and `#C99B4A` for warnings.
- Do not introduce a large UI framework or copy reference-site logos, brand palettes, or full page layouts.
- Appropriate reference-inspired component shapes, hover behavior, local glow/grid detail, and motion are allowed.
- Preserve existing analysis views, filters, endpoints, public deployment configuration, and user changes in `README.md`.
- Respect `prefers-reduced-motion: reduce` and keyboard `focus-visible` states.

---

### Task 1: Establish the Signal Lab visual system

**Files:**
- Modify: `frontend/src/styles/theme.css`
- Modify: `frontend/src/assets/app.css`
- Modify: `frontend/src/assets/main.css`

**Interfaces:**
- Produces CSS variables consumed by `App.vue`, `FilterBar.vue`, and all existing chart wrappers.
- Preserves existing class names so the first visual pass does not change component behavior.

- [ ] **Step 1: Replace the old blue-first tokens** with the Signal Lab canvas, panel, ink, line, accent, positive, neutral, warning, shadow, focus, and reduced-motion variables from the approved spec.
- [ ] **Step 2: Rework the shell rules** so the sidebar is the only persistent dark surface, the main canvas is `#F4F7F6`, cards are white with 8-12px radii, and page headers no longer depend on purple/blue gradients.
- [ ] **Step 3: Add shared interaction rules** for buttons, focus rings, pressed states, `data-hoverable`, selection, and reduced motion.
- [ ] **Step 4: Run `npm run build`** from `frontend`; expected result is a successful Vite build with no TypeScript or CSS errors.

### Task 2: Build the shared workspace header

**Files:**
- Create: `frontend/src/components/WorkspaceBar.vue`
- Modify: `frontend/src/App.vue`

**Interfaces:**
- `WorkspaceBar` props: `{ pageLabel: string; pageDescription: string; datasetLabel: string; filters: Array<{ label: string; value: string }>; updatedAt: string; exporting: boolean }`.
- `WorkspaceBar` emits: `clear-filter(label: string)`, `export`, `refresh`.

- [ ] **Step 1: Add a compact workspace bar** with breadcrumb-like page context, dataset/status pill, filter tokens, update time, refresh icon button, and export icon+text action.
- [ ] **Step 2: Render `WorkspaceBar` above every page body** in `App.vue`, deriving page label and description from the existing `nav` metadata and retaining `sf`/`af` values during navigation.
- [ ] **Step 3: Implement event handlers** in `App.vue`: clear sentiment/category back to `全部`, refresh the summary metrics, and call the export handler created in Task 4.
- [ ] **Step 4: Build again** with `npm run build`; expected result is a successful build and the header visible in all view branches.

### Task 3: Add the dashboard insight layer

**Files:**
- Create: `frontend/src/components/InsightSummary.vue`
- Modify: `frontend/src/App.vue`

**Interfaces:**
- `InsightSummary` props: `{ positiveRate: string; avgRating: string; npsScore: number; total: number; aspectCount: number; avgLength: string; sentiment: string; category: string }`.
- `InsightSummary` emits: `open(view: string)`.

- [ ] **Step 1: Implement the summary panel** with a clear headline, one-sentence conclusion assembled from current metrics, four metric cells, a thin confidence/source footer, and four drill-down action tiles for `sentiment`, `topics`, `rankings`, and `explorer`.
- [ ] **Step 2: Use local computed values** so the panel remains useful when the API is unavailable: show “等待数据” for empty metrics and “暂无足够数据生成结论” when `total === 0`.
- [ ] **Step 3: Place the panel at the top of the dashboard content** and keep the existing `metrics-bar` below it as a compact secondary readout instead of duplicating a large hero statistic block.
- [ ] **Step 4: Connect drill-down actions** to `switchView`, preserve active filters, and verify each tile changes the page without a full reload.

### Task 4: Make filtering and export feel complete

**Files:**
- Modify: `frontend/src/components/FilterBar.vue`
- Modify: `frontend/src/App.vue`
- Modify: `frontend/src/assets/app.css`

**Interfaces:**
- `FilterBar` continues to emit `update:sentimentFilter` and `update:aspectFilter` using existing Chinese display values.
- `App.vue` owns `exporting`, `exportMessage`, and `exportError` state.

- [ ] **Step 1: Convert FilterBar copy to the app’s Chinese product vocabulary** while preserving the current `all`/`positive`/`negative` and category values sent to the API.
- [ ] **Step 2: Add `aria-pressed`, `aria-label`, and `focus-visible` behavior** to segmented buttons and the more menu; keep the menu usable on mobile.
- [ ] **Step 3: Implement `downloadFilteredData()`** with `http.post('/export', { sentiment, category })`, serialize the returned JSON into a Blob, download `appinsight-export-YYYYMMDD.json`, and show success/failure feedback in the workspace bar.
- [ ] **Step 4: Add a compact toast/status surface** that clears after four seconds and remains readable on a small viewport.
- [ ] **Step 5: Build and manually verify** selecting a filter updates the existing charts and the export action downloads a JSON file when the backend is running.

### Task 5: Unify chart surfaces and motion

**Files:**
- Create: `frontend/src/utils/chartTheme.ts`
- Modify: `frontend/src/components/SentimentGauge.vue`
- Modify: `frontend/src/components/RatingSentiment.vue`
- Modify: `frontend/src/components/DomainCompare.vue`
- Modify: `frontend/src/components/EmotionHeatmap.vue`
- Modify: `frontend/src/components/WordCloud.vue`
- Modify: `frontend/src/components/TopAppsChart.vue`
- Modify: `frontend/src/components/QuadrantScatter.vue`
- Modify: `frontend/src/components/LengthAnalysisChart.vue`
- Modify: `frontend/src/components/SentimentTrend.vue`

**Interfaces:**
- `chartTheme.ts` exports `SIGNAL_COLORS`, `SIGNAL_TEXT`, and `applyChartTheme(option)` for consistent ECharts axis, tooltip, grid, and series defaults.

- [ ] **Step 1: Add the shared chart token module** with light-surface colors, semantic positive/negative/neutral colors, muted axis text, and compact tooltip styling.
- [ ] **Step 2: Apply shared colors to the highest-traffic dashboard charts first** (`SentimentGauge`, `RatingSentiment`, `DomainCompare`) without changing their endpoint payloads or series meaning.
- [ ] **Step 3: Apply the same palette and light plotting area** to sentiment, topic, ranking, and trend charts listed above; remove local purple/blue gradient colors where they conflict with semantic data.
- [ ] **Step 4: Add consistent chart transition duration and hover emphasis** while preserving existing resize/dispose lifecycle behavior.
- [ ] **Step 5: Verify charts render with backend data and remain readable at 1280px, 900px, and 390px widths.**

### Task 6: Make the landing entry match the product

**Files:**
- Modify: `frontend/src/components/LandingPage3D.vue`
- Modify: `frontend/src/assets/app.css`

**Interfaces:**
- Keeps the existing `enter` emit and 3D implementation.

- [ ] **Step 1: Reframe the landing screen** around AppInsight / Signal Lab copy, a restrained dark field, one orange/teal signal accent, and a clear entry action.
- [ ] **Step 2: Keep the 3D scene as the signature element** but reduce competing glow/gradient layers so it feels like a product entry, not a separate visual language.
- [ ] **Step 3: Add keyboard focus, reduced-motion fallback, and a loading/ready state** around the enter action.
- [ ] **Step 4: Verify the enter action still switches to the dashboard and the canvas does not remain blank if the 3D scene is unavailable.**

### Task 7: Local verification and cleanup

**Files:**
- Modify only files required by preceding tasks.

- [ ] **Step 1: Run `npm run build`** from `frontend`; expected result is successful production output.
- [ ] **Step 2: Start Flask locally** with `python backend/app.py` and Vite with `npm run dev -- --host 127.0.0.1`; verify `/api/test`, summary load, filters, charts, and export.
- [ ] **Step 3: Inspect desktop and mobile layouts** in the local browser at 1440x900 and 390x844; check no text overflow, fixed-header overlap, chart blank space, or bottom-nav collision.
- [ ] **Step 4: Check `git diff --check` and `git status --short`**; preserve unrelated `README.md` changes and report any remaining runtime limitation.
- [ ] **Step 5: Commit implementation changes** with `feat: refresh AppInsight workspace visual system` after verification succeeds.
