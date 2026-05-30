---
version: alpha
name: TicketForge
description: Design system for TicketForge — a developer infrastructure tool that turns GitHub Issues into tested, reviewed pull requests using a multi-agent AI pipeline.
colors:
  surface: "#0F1117"
  surface-raised: "#161B22"
  surface-overlay: "#1C2128"
  on-surface: "#E6EDF3"
  on-surface-muted: "#8B949E"
  border: "#30363D"
  border-emphasis: "#484F58"
  primary: "#2F81F7"
  primary-hover: "#388BFD"
  on-primary: "#FFFFFF"
  accent: "#56D364"
  accent-hover: "#6EE77A"
  on-accent: "#0F1117"
  error: "#F85149"
  error-subtle: "#3D1D20"
  warning: "#D29922"
  warning-subtle: "#2E2111"
  success: "#3FB950"
  success-subtle: "#122117"
  info: "#58A6FF"
  info-subtle: "#121D2F"
  focus-ring: "rgba(47, 129, 247, 0.4)"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "2rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h1:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  h2:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.4
  h3:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.5
  body:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.6
  caption:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "JetBrains Mono, Fira Code, Consolas, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  none: "0px"
  sm: "4px"
  md: "6px"
  lg: "8px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    height: "36px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    height: "36px"
  button-primary-disabled:
    backgroundColor: "{colors.border}"
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    height: "36px"
  button-secondary:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    height: "36px"
  button-secondary-hover:
    backgroundColor: "{colors.surface-overlay}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 16px"
    height: "36px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
    height: "36px"
  input-focus:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
    height: "36px"
  card:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: "16px"
  card-metric:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.h3}"
    rounded: "{rounded.lg}"
    padding: "16px 20px"
  badge-success:
    backgroundColor: "{colors.success-subtle}"
    textColor: "{colors.success}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
    height: "22px"
  badge-error:
    backgroundColor: "{colors.error-subtle}"
    textColor: "{colors.error}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
    height: "22px"
  badge-warning:
    backgroundColor: "{colors.warning-subtle}"
    textColor: "{colors.warning}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
    height: "22px"
  badge-info:
    backgroundColor: "{colors.info-subtle}"
    textColor: "{colors.info}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
    height: "22px"
  nav-sidebar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface-muted}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "12px 16px"
    width: "240px"
  nav-item-active:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
  nav-item-hover:
    backgroundColor: "{colors.surface-overlay}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "8px 12px"
  event-stream-entry:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.mono}"
    rounded: "{rounded.none}"
    padding: "8px 16px"
  pr-preview-card:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: "16px 20px"
  toast-success:
    backgroundColor: "{colors.success-subtle}"
    textColor: "{colors.success}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  toast-error:
    backgroundColor: "{colors.error-subtle}"
    textColor: "{colors.error}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
---

# TicketForge Design System

## Overview

TicketForge is a developer infrastructure tool that automates the pipeline from GitHub Issue to merged pull request. Its users are senior engineers, tech leads, and engineering managers — people who live in terminals, IDEs, and dashboards. They value transparency, precision, and trust above all else.

The design language is industrial and precise. It borrows from the visual vocabulary developers already trust: GitHub's dark surfaces, Linear's clean information hierarchy, and terminal-native monospace typography for agent output. The emotional response should be competence and calm — the feeling of a well-configured CI/CD pipeline that shows its work and never surprises you.

TicketForge must never feel like a marketing site, a gamified productivity app, or a consumer social product. It is infrastructure. It should look like infrastructure.

## Colors

The palette is anchored in deep slate surfaces (`#0F1117` base, `#161B22` raised, `#1C2128` overlay) that reduce eye strain during extended dashboard monitoring sessions. Three surface tiers create visual hierarchy through contrast alone — no shadows required for basic layering.

Primary blue (`#2F81F7`) drives all interactive elements: buttons, links, focus rings, and selected states. It is the only color that signals "you can act on this." Accent green (`#56D364`) is reserved for success states and positive pipeline outcomes — a fix that passed review, a PR that merged, a metric trending up.

Semantic colors follow developer conventions without deviation: red for errors, amber for warnings, green for success, blue for informational. Each semantic color has a subtle background variant (e.g., `#3D1D20` for error backgrounds) that provides context without overwhelming the surface hierarchy. All text-on-background pairings meet WCAG AA contrast minimums. The muted text color (`#8B949E`) is used only for secondary information — timestamps, helper text, metadata — never for content the user needs to act on.

## Typography

Inter is the primary typeface. It is a geometric sans-serif designed for screen readability at small sizes, with a tall x-height and open apertures that keep text legible at the 14px body size developers expect. Its weight range (400 regular, 600 semibold, 700 bold) provides enough hierarchy without visual noise.

JetBrains Mono is the monospace typeface for all code, agent event streams, file paths, and terminal-like output. It was chosen over Fira Code for its slightly wider character width, which improves scanability in event log streams where developers are pattern-matching across hundreds of entries. Ligatures are intentionally disabled — they obscure the actual characters in agent output, which defeats the transparency principle.

The type scale is compressed: display (2rem) is used sparingly for page titles, body (0.875rem / 14px) is the workhorse, and caption (0.75rem / 12px) handles metadata and timestamps. There is no large hero text — this is a dashboard, not a landing page. Tight letter-spacing on display and h1 levels (`-0.02em`, `-0.01em`) keeps headings compact and authoritative.

## Layout

Spacing follows a 4px base unit: `4 / 8 / 12 / 16 / 24 / 32`. The scale is intentionally compact — this is an information-dense tool where screen real estate is valuable. The 12px step (`md`) exists because the jump from 8 to 16 is too large for component internal padding.

The primary layout is a fixed sidebar (240px) with a scrollable content area. The sidebar provides persistent navigation across pipeline views, team settings, and analytics. The content area uses a single-column layout for event streams and ticket detail views, and a responsive grid (auto-fill, min 280px) for metric cards and PR overview lists.

Container max-width is 1200px for content-heavy views (documentation, settings) and full-width for dashboard grids and event streams. Gutters are 16px at all breakpoints — consistency over responsiveness, since this tool is used primarily on desktop monitors.

## Elevation & Depth

TicketForge uses a border-and-contrast strategy rather than shadows. Cards, inputs, and containers are defined by the `border` color (`#30363D`) — a 1px solid line that separates surfaces without lifting them. The `border-emphasis` color (`#484F58`) is used for active or focused elements that need stronger visual separation.

Shadows are avoided for two reasons: they imply floating elements and visual playfulness that conflicts with the industrial aesthetic, and they perform poorly on the dark surfaces that dominate the interface. The only exception is the focus ring (`rgba(47, 129, 247, 0.4)`) — a 2px blue glow that provides clear keyboard navigation feedback without relying on border changes.

Depth is communicated through surface color tiers: base (`surface`) → raised (`surface-raised`) → overlay (`surface-overlay`). Modals and dropdowns use `surface-overlay` with a `border-emphasis` outline. This three-tier system is sufficient for all UI states — more tiers would add complexity without clarity.

## Shapes

Corner radius is conservative: 6px default (`md`) for interactive elements (buttons, inputs, cards), 4px (`sm`) for inline elements (code blocks, small containers), 8px (`lg`) for larger cards and modals, and fully rounded (`9999px`) exclusively for badges and status pills.

The 6px default signals professionalism without severity. Sharper corners (0–2px) would push the design toward brutalist terminal aesthetics that alienate engineering managers. Rounder corners (12px+) would push it toward consumer app territory that undermines developer credibility. The 6px sweet spot says "modern tool, serious purpose."

Radius does not vary by state — a button's corners stay at 6px whether it is default, hovered, or disabled. Consistency in shape language reduces visual noise in dense dashboard layouts.

## Components

**Buttons** come in two variants: primary (blue background, white text) and secondary (raised surface background, light text). Both are 36px tall with 8px vertical / 16px horizontal padding. The primary button is used for the single most important action on a page — never more than one primary button per view. Disabled state uses `border` background with `on-surface-muted` text, making it visually recede without disappearing.

**Inputs** are 36px tall with a `surface` background and `border` outline. On focus, the border is replaced by the `focus-ring` glow. Placeholder text uses `on-surface-muted`. Inputs do not change background color on focus — the ring alone signals the active state.

**Cards** are the primary container for grouped information: metric summaries, PR previews, ticket details. They use `surface-raised` background with `border` outline and `lg` rounding. Internal padding is 16px (standard) or 16px × 20px (metric cards, for extra horizontal breathing room around numbers).

**Badges** communicate pipeline status at a glance. They are fully rounded pills with semantic background-text pairings: green for success/merged, red for error/failed, amber for warning/review-needed, blue for info/in-progress. At 22px tall with caption typography, they are designed to sit inline with body text or in card headers without disrupting line height.

**Nav sidebar** is 240px wide with `surface` background — visually receding behind the content area. Active nav items get `surface-raised` background with full `on-surface` text color. Inactive items use `on-surface-muted` to create a clear active/inactive distinction. Hover state uses `surface-overlay`.

**Event stream entries** are the signature component — a chronological log of every agent action. They use monospace typography on `surface` background with no rounding (stacked entries should feel like a continuous stream, not discrete cards). Each entry includes a timestamp (caption, muted), agent name (caption, primary color), and action description (mono, default text).

**PR preview cards** combine ticket metadata, fix summary, review status badge, and action buttons in a single `surface-raised` card. The title links to the GitHub PR. The review status badge sits in the card header. The event count and time-to-fix are displayed in caption/muted typography below the main content.

**Toasts** provide transient feedback for pipeline events: "Fix generated for ISSUE-342," "Review failed — escalating to human." They use semantic subtle backgrounds with matching text colors, 6px rounding, and auto-dismiss after 5 seconds. Error toasts persist until manually dismissed.

## Do's and Don'ts

**Do:**
- Use the three-tier surface hierarchy (`surface` → `surface-raised` → `surface-overlay`) to create depth without shadows.
- Reserve primary blue exclusively for interactive elements — buttons, links, focus rings, selected states. If it is blue, the user should be able to click it.
- Show agent work transparently: event streams, decision logs, and code diffs are first-class UI elements, not hidden behind "show details" toggles.
- Use monospace typography for all agent-generated content, file paths, code references, and terminal-like output. It signals "this came from the pipeline" versus "this is UI chrome."
- Keep information density high — developers expect data-rich interfaces. Use caption typography and muted colors for metadata rather than hiding it.
- Use badges consistently for pipeline status — the color-to-meaning mapping (green/red/amber/blue) must be absolute and never violated.

**Don'ts:**
- Never use shadows for elevation. The border-and-contrast system is the only depth mechanism.
- Never use more than one primary button per view. If everything is emphasized, nothing is.
- Never hide agent actions behind collapsible sections by default. Transparency is the core trust mechanism — the event stream must be visible, scannable, and complete.
- Never use rounded corners above 8px on functional components. Fully rounded (`9999px`) is reserved for badges and status pills only.
- Never use decorative illustrations, gradients, or animated transitions. This is infrastructure UI — every pixel should convey information or afford interaction.
- Never use marketing language in the UI. Status messages are precise and technical: "Fix generated, 2 tests updated, review passed" — not "Great news! Your bug is fixed!"
