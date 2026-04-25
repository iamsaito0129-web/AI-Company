---
name: Industrial Tech-Noir
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#38393a'
  surface-container-lowest: '#0c0f0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#282a2b'
  surface-container-highest: '#333535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#cfc4c5'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#988e90'
  outline-variant: '#4c4546'
  surface-tint: '#c6c6c6'
  primary: '#c6c6c6'
  on-primary: '#303030'
  primary-container: '#000000'
  on-primary-container: '#757575'
  inverse-primary: '#5e5e5e'
  secondary: '#c6c6c7'
  on-secondary: '#2f3131'
  secondary-container: '#454747'
  on-secondary-container: '#b4b5b5'
  tertiary: '#ffb4a8'
  on-tertiary: '#690100'
  tertiary-container: '#000000'
  on-tertiary-container: '#ec0000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1b1b1b'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a8'
  on-tertiary-fixed: '#410000'
  on-tertiary-fixed-variant: '#930100'
  background: '#121414'
  on-background: '#e2e2e2'
  surface-variant: '#333535'
typography:
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 16px
  margin: 32px
  container-max: 1280px
---

## Brand & Style

The design system is a manifestation of "raw technology." It bridges the gap between retro-analog aesthetics and futuristic digital interfaces. The brand personality is transparent, intentional, and slightly subversive, stripping away the "veneer" of typical consumer tech to reveal a functional, industrial core.

The visual style is a hybrid of **Minimalism** and **Glassmorphism**, reinforced by **Brutalism**. It prioritizes a high-contrast environment where information is organized with clinical precision. The goal is to evoke a sense of curiosity and technical sophistication, making the user feel like they are interacting with the "inner workings" of a premium machine.

## Colors

The palette is strictly monochromatic to maintain a tech-noir atmosphere. 
- **Black (#000000)**: Serves as the infinite void for the background, providing the high-contrast foundation.
- **White (#FFFFFF)**: Used for primary text and high-priority UI elements to ensure maximum legibility.
- **Red (#FF0000)**: A singular, aggressive accent color used sparingly for critical alerts, recording states, or primary calls to action.
- **Light Grey (#F5F5F5)**: Utilized for subtle dividers, secondary text, or low-opacity glass backgrounds.

Designers should rely on opacity variants of white (e.g., White at 5%, 10%, 20%) to create depth rather than introducing new grey hex codes.

## Typography

This design system uses a dual-font approach. **Space Grotesk** provides the technical, geometric edge required for headlines, mimicking the precision of engineering schematics. **Inter** is used for body copy and labels to ensure maximum utility and readability.

**The NDOT Effect:** While the tokens use standard fonts, all primary headings (H1-H3) should ideally be rendered in a Dot Matrix style (NDOT). If the custom font is unavailable, use Space Grotesk with increased letter spacing and a weight that feels light yet structural. Labels should always be uppercase to reinforce the industrial/label-maker aesthetic.

## Layout & Spacing

The layout is governed by a **strict 8px grid**. Everything is aligned to this modular rhythm to maintain an "engineered" appearance. 

The system employs a **Fixed Grid** model for desktop interfaces, utilizing a 12-column structure with 16px gutters. For mobile, a 4-column fluid grid is used. White space is not just "empty"; it is a functional gap that separates distinct functional modules. Layouts should feel modular, as if different components were "snapped" together on a circuit board.

## Elevation & Depth

Hierarchy in the design system is achieved through **Glassmorphism** and **Tonal Layering** rather than traditional drop shadows.

1.  **Backdrop Blurs:** High-elevation elements (like modals or floating menus) use a semi-transparent white or black fill with a heavy background blur (20px-40px). This creates a "frosted glass" effect that hints at the layers beneath.
2.  **Inner Borders:** Instead of shadows, use 1px solid borders with low opacity (10-15% White) to define the edges of containers.
3.  **Physical Stacking:** Elements "higher" in the stack should be slightly lighter in color or more opaque than elements below them. Shadows, if used, must be sharp and minimal—mimicking a direct light source in a dark room.

## Shapes

The shape language is a contrast between **Sharp Geometries** and **Perfect Circles**.

- **Containers:** Large cards and section containers use a "Soft" (0.25rem) radius to feel modern but structured.
- **Interactive Elements:** Buttons, chips, and toggles should lean towards circular or pill-shaped designs (rounded-full).
- **Dot Patterns:** Small circular elements (1px to 4px dots) should be used as decorative grid markers or as part of the NDOT typography style to reinforce the "tech-noir" hardware feel.

## Components

- **Buttons:** Primary buttons are either solid white with black text (high contrast) or transparent with a 1px white border. The hover state should invert the colors. For destructive or critical actions, use the signature Red (#FF0000).
- **Chips & Tags:** Small, pill-shaped containers with mono-spaced uppercase text. Use a 10% white background for a subtle "glass" look.
- **Input Fields:** Minimalist underlines or 1px bordered boxes. Use a dot-matrix style for the label or placeholder to maintain the tech aesthetic.
- **Cards:** Use a background blur effect with a subtle 1px border. Do not use shadows; let the blur and border define the card's boundary against the dark background.
- **Progress Indicators:** Use thin lines or sequences of dots. Circular progress bars should be perfectly geometric without rounded caps for an industrial feel.
- **Checkboxes/Radios:** Should appear as high-precision toggles or "switches" reminiscent of physical hardware buttons.---
name: Industrial Tech-Noir
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#38393a'
  surface-container-lowest: '#0c0f0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#282a2b'
  surface-container-highest: '#333535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#cfc4c5'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#988e90'
  outline-variant: '#4c4546'
  surface-tint: '#c6c6c6'
  primary: '#c6c6c6'
  on-primary: '#303030'
  primary-container: '#000000'
  on-primary-container: '#757575'
  inverse-primary: '#5e5e5e'
  secondary: '#c6c6c7'
  on-secondary: '#2f3131'
  secondary-container: '#454747'
  on-secondary-container: '#b4b5b5'
  tertiary: '#ffb4a8'
  on-tertiary: '#690100'
  tertiary-container: '#000000'
  on-tertiary-container: '#ec0000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1b1b1b'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a8'
  on-tertiary-fixed: '#410000'
  on-tertiary-fixed-variant: '#930100'
  background: '#121414'
  on-background: '#e2e2e2'
  surface-variant: '#333535'
typography:
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 16px
  margin: 32px
  container-max: 1280px
---

## Brand & Style

The design system is a manifestation of "raw technology." It bridges the gap between retro-analog aesthetics and futuristic digital interfaces. The brand personality is transparent, intentional, and slightly subversive, stripping away the "veneer" of typical consumer tech to reveal a functional, industrial core.

The visual style is a hybrid of **Minimalism** and **Glassmorphism**, reinforced by **Brutalism**. It prioritizes a high-contrast environment where information is organized with clinical precision. The goal is to evoke a sense of curiosity and technical sophistication, making the user feel like they are interacting with the "inner workings" of a premium machine.

## Colors

The palette is strictly monochromatic to maintain a tech-noir atmosphere. 
- **Black (#000000)**: Serves as the infinite void for the background, providing the high-contrast foundation.
- **White (#FFFFFF)**: Used for primary text and high-priority UI elements to ensure maximum legibility.
- **Red (#FF0000)**: A singular, aggressive accent color used sparingly for critical alerts, recording states, or primary calls to action.
- **Light Grey (#F5F5F5)**: Utilized for subtle dividers, secondary text, or low-opacity glass backgrounds.

Designers should rely on opacity variants of white (e.g., White at 5%, 10%, 20%) to create depth rather than introducing new grey hex codes.

## Typography

This design system uses a dual-font approach. **Space Grotesk** provides the technical, geometric edge required for headlines, mimicking the precision of engineering schematics. **Inter** is used for body copy and labels to ensure maximum utility and readability.

**The NDOT Effect:** While the tokens use standard fonts, all primary headings (H1-H3) should ideally be rendered in a Dot Matrix style (NDOT). If the custom font is unavailable, use Space Grotesk with increased letter spacing and a weight that feels light yet structural. Labels should always be uppercase to reinforce the industrial/label-maker aesthetic.

## Layout & Spacing

The layout is governed by a **strict 8px grid**. Everything is aligned to this modular rhythm to maintain an "engineered" appearance. 

The system employs a **Fixed Grid** model for desktop interfaces, utilizing a 12-column structure with 16px gutters. For mobile, a 4-column fluid grid is used. White space is not just "empty"; it is a functional gap that separates distinct functional modules. Layouts should feel modular, as if different components were "snapped" together on a circuit board.

## Elevation & Depth

Hierarchy in the design system is achieved through **Glassmorphism** and **Tonal Layering** rather than traditional drop shadows.

1.  **Backdrop Blurs:** High-elevation elements (like modals or floating menus) use a semi-transparent white or black fill with a heavy background blur (20px-40px). This creates a "frosted glass" effect that hints at the layers beneath.
2.  **Inner Borders:** Instead of shadows, use 1px solid borders with low opacity (10-15% White) to define the edges of containers.
3.  **Physical Stacking:** Elements "higher" in the stack should be slightly lighter in color or more opaque than elements below them. Shadows, if used, must be sharp and minimal—mimicking a direct light source in a dark room.

## Shapes

The shape language is a contrast between **Sharp Geometries** and **Perfect Circles**.

- **Containers:** Large cards and section containers use a "Soft" (0.25rem) radius to feel modern but structured.
- **Interactive Elements:** Buttons, chips, and toggles should lean towards circular or pill-shaped designs (rounded-full).
- **Dot Patterns:** Small circular elements (1px to 4px dots) should be used as decorative grid markers or as part of the NDOT typography style to reinforce the "tech-noir" hardware feel.

## Components

- **Buttons:** Primary buttons are either solid white with black text (high contrast) or transparent with a 1px white border. The hover state should invert the colors. For destructive or critical actions, use the signature Red (#FF0000).
- **Chips & Tags:** Small, pill-shaped containers with mono-spaced uppercase text. Use a 10% white background for a subtle "glass" look.
- **Input Fields:** Minimalist underlines or 1px bordered boxes. Use a dot-matrix style for the label or placeholder to maintain the tech aesthetic.
- **Cards:** Use a background blur effect with a subtle 1px border. Do not use shadows; let the blur and border define the card's boundary against the dark background.
- **Progress Indicators:** Use thin lines or sequences of dots. Circular progress bars should be perfectly geometric without rounded caps for an industrial feel.
- **Checkboxes/Radios:** Should appear as high-precision toggles or "switches" reminiscent of physical hardware buttons.