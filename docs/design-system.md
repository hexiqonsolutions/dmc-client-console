# Design system — Studio Command

Locked in Milestone 1. All UI must follow these tokens.

## Brand

| Token | Hex | CSS variable |
|-------|-----|--------------|
| Primary (teal) | `#0F766E` | `--primary` |
| Ink (sidebar) | `#0B1220` | `--sidebar` |
| Background (mist) | `#F5F7FA` | `--background` |
| Surface | `#FFFFFF` | `--card` |
| Text | `#0F172A` | `--foreground` |
| Muted | `#64748B` | `--muted-foreground` |
| Border | `#E2E8F0` | `--border` |
| CTA | `#C2410C` | `--cta` |

## Typography

- Headings: **Space Grotesk** (`--font-space-grotesk`, utility `font-heading`)
- Body / UI: **Manrope** (`--font-manrope`, utility `font-sans`)
- Code: **Geist Mono**

## Brand assets

| File | Use |
|------|-----|
| `/public/dm-logo.png` | Full DMC wordmark (auth header, marketing) |
| `/public/favicon.png` | Circular mark + browser favicon (`src/app/icon.png`) |

Component: `src/components/brand/brand-logo.tsx` (`mark` | `wordmark`).

## Rules

1. Prefer tables/lists for work data; cards only for interactive containers.
2. No purple AI gradients, neon glow, or emoji-as-icons.
3. Use Lucide icons via `lucide-react`.
4. Hover/focus transitions 150–300ms; respect `prefers-reduced-motion`.
5. Light mode is the default product experience.
6. Reuse `EmptyState`, `PageHeader`, `PageLoading`, and `ErrorState` instead of one-off placeholders.

Source of truth: `src/app/globals.css` + `docs/design-system.md`
