# AppInsight Brand Icon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Vue template favicon and duplicated inline AppInsight marks with one MIT-licensed, theme-matched `chart-dots` brand SVG.

**Architecture:** Store one transparent two-tone SVG in `frontend/public` so Vite serves it from `/appinsight-mark.svg`. Reference that same URL from the HTML favicon link and both visible brand locations; keep the existing ICO link as a fallback.

**Tech Stack:** Vue 3, Vite, HTML favicon links, inline Vue templates, SVG.

## Global Constraints

- Use Tabler Icons `chart-dots` as the path basis and retain a source/license notice.
- Use project colors `#2E8B78` and `#E56B55` without adding a background to the shared mark.
- Do not change navigation, GitHub, or content-card functional icons.
- Keep the current working-tree changes unrelated to this task untouched.

### Task 1: Add the shared brand asset and notice

**Files:**
- Create: `frontend/public/appinsight-mark.svg`
- Create: `frontend/public/THIRD-PARTY-NOTICES.txt`

**Interfaces:**
- Produces: browser-loadable asset at `/appinsight-mark.svg` for HTML and Vue templates.

- [ ] **Step 1: Create the SVG from the approved icon basis**

Create a 24x24 transparent SVG using the official Tabler `chart-dots` geometry. Render axes and connecting lines in `#2E8B78`, and the three data nodes in `#E56B55`; use `stroke-linecap="round"` and `stroke-linejoin="round"` so the mark remains legible at favicon size.

- [ ] **Step 2: Record the source and license**

Add the Tabler Icons repository URL, `chart-dots` source URL, and MIT license statement to `frontend/public/THIRD-PARTY-NOTICES.txt`.

- [ ] **Step 3: Verify asset syntax**

Run `rg -n "svg|chart-dots|2E8B78|E56B55" frontend/public/appinsight-mark.svg frontend/public/THIRD-PARTY-NOTICES.txt` and confirm the SVG has one root `<svg>` and no Vue-specific paths.

### Task 2: Wire the shared asset into the application

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/src/App.vue:9-13`
- Modify: `frontend/src/components/LandingPage3D.vue:6-8,407-408`

**Interfaces:**
- Consumes: `/appinsight-mark.svg` from Task 1.
- Produces: one favicon source and one visible brand asset path used by both page shells.

- [ ] **Step 1: Update favicon precedence**

Add `<link rel="icon" type="image/svg+xml" href="/appinsight-mark.svg">` before the existing ICO link in `frontend/index.html`; leave `<link rel="icon" href="/favicon.ico">` as the compatibility fallback.

- [ ] **Step 2: Replace the analysis-shell inline mark**

Replace the sidebar inline SVG with `<img class="brand-icon" src="/appinsight-mark.svg" alt="" aria-hidden="true">` in `frontend/src/App.vue`.

- [ ] **Step 3: Replace the landing-shell inline mark**

Replace the landing page inline SVG with `<img class="logo-mark-image" src="/appinsight-mark.svg" alt="" aria-hidden="true">`; update the `.logo-mark svg` selector to `.logo-mark-image` while retaining the existing 32x26 layout box.

- [ ] **Step 4: Verify references and scope**

Run `rg -n "appinsight-mark|favicon|brand-icon|logo-mark" frontend/index.html frontend/src/App.vue frontend/src/components/LandingPage3D.vue` and confirm no inline SVG remains in either brand-mark location while unrelated SVGs remain untouched.

### Task 3: Build and inspect the delivered UI

**Files:**
- Test: `frontend` production build and source reference checks.

- [ ] **Step 1: Run the production build**

Run `npm run build` from `frontend`. Expected result: Vite completes successfully and copies `appinsight-mark.svg` to the build output.

- [ ] **Step 2: Validate the built HTML and asset**

Run `rg -n "appinsight-mark|favicon" frontend/dist/index.html frontend/dist -g "*.html" -g "*.svg"`. Expected result: the SVG favicon is the first icon link, and the built brand asset exists.

- [ ] **Step 3: Review the final diff**

Run `git diff --check` and `git diff -- frontend/index.html frontend/src/App.vue frontend/src/components/LandingPage3D.vue frontend/public/appinsight-mark.svg frontend/public/THIRD-PARTY-NOTICES.txt`. Confirm only the approved icon replacement is included.

- [ ] **Step 4: Commit and push**

Stage only the icon-related files and create commit `feat: replace AppInsight brand icons`, then run `git push origin Design-Upgrade`.
