# Design System Document: The Celestial Intelligence Framework

## 1. Overview & Creative North Star
**Creative North Star: "The Deep Space Observatory"**

To design for churn prediction is to design for foresight. We are moving away from the "cluttered spreadsheet" aesthetic of traditional SaaS and toward a high-end, cinematic dashboard experience. The goal is to make the user feel like they are piloting a sophisticated vessel through a sea of data. 

We break the "template" look through **Intentional Asymmetry** and **Atmospheric Depth**. By avoiding rigid, boxy grids and instead utilizing floating glass modules and overlapping translucent layers, we create a sense of vastness and "Apple-level" fluidness. This system isn't just a UI; it’s a digital environment where data doesn't just sit on a screen—it glows within a dark, infinite space.

---

## 2. Colors & Surface Philosophy
The palette is rooted in the "Deep Space" concept, utilizing a high-contrast relationship between obsidian-toned foundations and hyper-saturated neon signals.

### Surface Hierarchy & Nesting
We abandon the flat UI. We use the `surface-container` tiers to create "nested" depth, simulating physical layers of frosted glass.
- **The Foundation:** Use `surface` (#060e20) for the primary application background.
- **The Stacking Rule:** To create a module, place a `surface-container-low` (#091328) panel on top of the foundation. Inside that panel, use `surface-container` (#0f1930) for interactive elements. This creates "soft lift" without the need for heavy-handed shadows.
- **The "No-Line" Rule:** **1px solid borders are prohibited for sectioning.** Boundaries must be defined solely through background color shifts or the transition of `backdrop-blur`. If two areas need separation, use a 40px - 64px vertical gap or a subtle shift from `surface-container-low` to `surface-container-high`.

### The Glass & Gradient Rule
To achieve the "Futuristic" feel, primary panels must use **Glassmorphism**:
- **Recipe:** `surface-container` at 70% opacity + 20px - 40px `backdrop-blur`.
- **Signature Textures:** Use a subtle linear gradient (Top-Left to Bottom-Right) from `primary` (#89acff) to `secondary` (#b884ff) at 15% opacity as an overlay on high-value prediction cards to give them a "soul."

---

## 3. Typography: The Editorial Voice
Our typography needs to feel authoritative yet breathable. We pair **Manrope** (Display/Headlines) for its technical, modern character with **Inter** (Body) for its legendary legibility.

- **Display Scale:** Use `display-lg` (3.5rem) with `-0.04em` tracking for "Hero" churn percentages. This creates a bold, editorial impact.
- **The Hierarchy of Truth:** Headlines should use `headline-sm` in `Medium` or `SemiBold` weight. Body text (`body-md`) should always utilize a slightly increased line-height (1.6) and `on-surface-variant` (#a3aac4) color to reduce eye strain against the dark background.
- **Labeling:** Use `label-md` in `All Caps` with `+0.05em` tracking for category headers to create a "technical instrument" feel.

---

## 4. Elevation & Depth
In "Deep Space," light comes from the data itself.

- **The Layering Principle:** Stack `surface-container-lowest` cards on a `surface-container-low` background to create a "recessed" or "carved" look.
- **Ambient Shadows:** For floating modals or dropdowns, use an "Ambient Glow" rather than a shadow. Use a 60px blur, 0px offset, and 6% opacity of the `primary` (#89acff) color. This mimics the light refraction of a neon screen in a dark room.
- **The "Ghost Border" Fallback:** If accessibility requires a border, use the `outline-variant` (#40485d) at **15% opacity**. It should be a suggestion of an edge, not a hard line.

---

## 5. Components

### Buttons
- **Primary:** Linear gradient from `primary` to `primary-dim`. Large corner radius (`xl`). No border.
- **Secondary (Glass):** `surface-variant` at 40% opacity with a `backdrop-blur` of 12px.
- **States:** On hover, increase the `surface-tint` or add a 1px "Ghost Border" using `tertiary` (#8ff5ff) at 30% opacity to simulate a power-on state.

### Input Fields
- **Styling:** Use `surface-container-highest` for the field background.
- **Focus State:** Instead of a thick border, use a 2px outer glow of `secondary` (#b884ff) with a 10% opacity.
- **Forbid Dividers:** In forms, do not use lines to separate inputs. Use 24px of vertical whitespace.

### Churn Prediction Cards (Specialty Component)
- **Visuals:** Large `xl` (3rem) rounded corners. A subtle internal shadow (inset 0 1px 1px rgba(255,255,255,0.1)) to create a "beveled glass" edge.
- **Data Visualization:** Use `tertiary` (Neon Cyan) for "Safe" metrics and `error` (#ff716c) for "At Risk" metrics.

### Chips & Badges
- **Selection Chips:** No background fill; use a `primary` "Ghost Border" and `label-md` text. When selected, fill with `primary` and change text to `on-primary`.

---

## 6. Do's and Don'ts

### Do:
- **Do** use varying font weights to create hierarchy instead of just increasing size.
- **Do** use large, generous white space. High-end design needs room to breathe.
- **Do** overlap elements (e.g., a chart slightly bleeding over the edge of a container) to break the "grid" feel.

### Don't:
- **Don't** use pure black (#000000) for backgrounds; it kills the depth. Use the `surface` (#060e20) slate-zinc blend.
- **Don't** use 100% opaque borders. They are the quickest way to make a premium design look "cheap" or "bootstrap-like."
- **Don't** use standard "drop shadows." If a panel needs to pop, use atmospheric glow or background tonal shifts.
- **Don't** use more than 3 accent colors in a single view. Stick to the Blue/Violet/Cyan triad to maintain the "Deep Space" sophistication.