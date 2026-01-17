---
description: Taikang style design system for frontend development - professional, trustworthy, and minimalist design language
globs: ["**/frontend/**/*.{tsx,ts,jsx,js,css,scss}", "**/src/**/*.{tsx,ts,jsx,js,css,scss}", "**/*.css", "**/*.scss"]
alwaysApply: false
---

# Taikang Style Design System

## Design Philosophy

The Taikang design system emphasizes:
- **简约大气 (Simple & Elegant)**: Generous whitespace, clear modules, clean and intuitive content presentation
- **专业稳重 (Professional & Stable)**: Deep blue primary color + sans-serif fonts convey financial trust
- **响应式兼容 (Responsive)**: Single layout system adapts to PC/tablet/mobile
- **信息优先 (Information First)**: Use dividers and whitespace to organize content areas, highlighting key data and core business

## 1. Color System (色彩系统)

### Color Palette

```css
:root {
  /* Primary Colors - 主色系 */
  --color-primary: #0A3B73;           /* Deep blue - 深蓝/海军蓝 (企业识别、头部、重要按钮) */
  --color-primary-hover: #0B4A8A;    /* Primary hover state */
  --color-primary-active: #082D5A;    /* Primary active state */
  
  /* Secondary Colors - 辅助色 */
  --color-secondary: #5B7DB1;        /* Light blue / Gray-blue (次级按钮、信息提示) */
  --color-secondary-hover: #6B8DC1;  /* Secondary hover state */
  
  /* Accent Colors - 强调色 */
  --color-accent: #D4AF37;           /* Gold / Orange (链接、交互提示) */
  --color-accent-hover: #E5C047;    /* Accent hover state */
  
  /* Neutral Colors - 中性色 */
  --color-neutral-bg: #F7F8FA;       /* Light gray background */
  --color-neutral-surface: #FFFFFF;  /* White surface */
  --color-neutral-border: #F0F0F0;   /* Light border */
  --color-neutral-text: #333333;     /* Dark gray text */
  --color-neutral-text-secondary: #666666; /* Secondary text */
  --color-neutral-text-tertiary: #999999;  /* Tertiary text */
  
  /* Semantic Colors */
  --color-success: #52C41A;
  --color-warning: #FAAD14;
  --color-error: #FF4D4F;
  --color-info: #1890FF;
  
  /* Border Colors */
  --color-border-default: #D9D9D9;
  --color-border-focus: var(--color-primary);
  
  /* Disabled States */
  --color-disabled-bg: #E0E0E0;
  --color-disabled-text: #9E9E9E;
}
```

### Color Usage Guidelines

| Color Category | Usage | Examples |
|---------------|-------|----------|
| **Primary** | Enterprise branding, headers, important buttons | Navigation bar, primary CTA buttons, page titles |
| **Secondary** | Secondary buttons, information prompts | Secondary actions, info cards |
| **Accent** | Links, interactive hints | Hyperlinks, hover states, highlights |
| **Neutral** | Backgrounds, dividers, body text | Page backgrounds, card backgrounds, text content |

**Key Principle**: Primary colors emphasize "enterprise professionalism and trustworthiness", suitable for financial/insurance industry websites.

## 2. Typography (字体与排版)

### Font Family

```css
:root {
  --font-family-base: "PingFang SC", "Noto Sans", "Microsoft YaHei", Arial, sans-serif;
  --font-family-mono: "SF Mono", "Monaco", "Consolas", monospace;
}
```

**Principle**: Use sans-serif fonts for modern, clean readability that conveys professionalism.

### Font Weights

```css
:root {
  --font-weight-light: 300;
  --font-weight-regular: 400;    /* Body text, descriptive text */
  --font-weight-medium: 500;    /* Form hints, auxiliary information */
  --font-weight-semibold: 600;  /* Module subtitles */
  --font-weight-bold: 700;       /* H1-H3 headings */
}
```

### Font Sizes

```css
:root {
  --font-size-h1: 36px;
  --font-size-h2: 30px;
  --font-size-h3: 24px;
  --font-size-h4: 20px;
  --font-size-body: 18px;       /* Body text */
  --font-size-small: 14px;       /* Small text, captions */
  --font-size-xs: 12px;          /* Extra small text */
  
  /* Line Heights */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

### Typography Classes

```css
/* Headings */
h1, .h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--color-primary);
  margin-bottom: 24px;
}

h2, .h2 {
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--color-primary);
  margin-bottom: 20px;
}

h3, .h3 {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  color: var(--color-primary);
  margin-bottom: 16px;
}

/* Body Text */
body, .body {
  font-family: var(--font-family-base);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-normal);
  color: var(--color-neutral-text);
}

/* Small Text */
small, .small {
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--color-neutral-text-secondary);
}
```

## 3. Spacing & Grid (布局与空间)

### Spacing Scale

Based on 8px base unit:

```css
:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;      /* Base unit */
  --spacing-md: 16px;    /* 2x base */
  --spacing-lg: 24px;    /* 3x base */
  --spacing-xl: 32px;    /* 4x base */
  --spacing-2xl: 48px;   /* 6x base */
  --spacing-3xl: 64px;   /* 8x base */
}
```

### Layout System

```css
:root {
  /* Container Max Widths */
  --container-max-width: 1200px;
  --container-padding: var(--spacing-lg);
  
  /* Grid System */
  --grid-columns: 12;
  --grid-gap: var(--spacing-lg);
}
```

### Container Classes

```css
.container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

.container-fluid {
  width: 100%;
  padding: 0 var(--container-padding);
}

/* Grid System (12 columns) */
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gap);
}

.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-8 { grid-column: span 8; }
.col-9 { grid-column: span 9; }
.col-12 { grid-column: span 12; }
```

**Principle**: Typical layout is "center-axis symmetry + generous whitespace", making content easier to browse and highlighting information hierarchy.

## 4. Borders & Dividers (边框与分隔线)

### Border Styles

```css
:root {
  --border-width: 1px;
  --border-style: solid;
  --border-radius-sm: 2px;
  --border-radius-md: 4px;
  --border-radius-lg: 8px;
  --border-radius-full: 9999px;
  
  /* Border Colors */
  --border-color-default: var(--color-border-default);
  --border-color-focus: var(--color-border-focus);
  --border-color-divider: var(--color-neutral-border);
}

/* Buttons */
.btn {
  border: var(--border-width) var(--border-style) transparent;
  border-radius: var(--border-radius-md);
}

.btn-primary {
  border: none;
}

.btn-secondary {
  border-color: var(--color-primary);
}

/* Input Fields */
.input {
  border: var(--border-width) var(--border-style) var(--border-color-default);
  border-radius: var(--border-radius-md);
}

.input:focus {
  border-color: var(--border-color-focus);
  outline: none;
}

/* Cards */
.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: var(--border-radius-md);
}

/* Dividers */
.divider {
  border-top: var(--border-width) var(--border-style) var(--border-color-divider);
  margin: var(--spacing-lg) 0;
}

.divider-vertical {
  border-left: var(--border-width) var(--border-style) var(--border-color-divider);
  height: 100%;
  margin: 0 var(--spacing-md);
}
```

**Principle**: Avoid heavy borders visually, use light colors and shadows to enhance hierarchy.

## 5. Buttons (按钮)

### Button Styles

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  font-family: var(--font-family-base);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  border: var(--border-width) var(--border-style) transparent;
}

/* Primary Button */
.btn-primary {
  background-color: var(--color-primary);
  color: #FFFFFF;
  border: none;
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
}

.btn-primary:active {
  background-color: var(--color-primary-active);
}

.btn-primary:disabled {
  background-color: var(--color-disabled-bg);
  color: var(--color-disabled-text);
  cursor: not-allowed;
}

/* Secondary Button */
.btn-secondary {
  background-color: var(--color-neutral-surface);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn-secondary:hover {
  background-color: var(--color-neutral-bg);
  border-color: var(--color-primary-hover);
}

.btn-secondary:active {
  background-color: var(--color-neutral-border);
}

.btn-secondary:disabled {
  background-color: var(--color-disabled-bg);
  color: var(--color-disabled-text);
  border-color: var(--color-disabled-bg);
  cursor: not-allowed;
}

/* Accent Button (for links) */
.btn-accent {
  background-color: transparent;
  color: var(--color-accent);
  border: none;
  text-decoration: underline;
}

.btn-accent:hover {
  color: var(--color-accent-hover);
}

/* Button Sizes */
.btn-sm {
  padding: 6px 16px;
  font-size: var(--font-size-small);
}

.btn-lg {
  padding: 14px 32px;
  font-size: 20px;
}
```

### Button Usage Table

| Type | Background | Border | Text Color | Usage |
|------|-----------|--------|------------|-------|
| Primary | Primary color | None | White | Main actions, CTAs |
| Secondary | White | Primary color | Primary color | Secondary actions |
| Accent | Transparent | None | Accent color | Links, highlights |
| Disabled | #E0E0E0 | None | #9E9E9E | Disabled state |

## 6. Components (组件规范)

### Navigation Bar (Header)

```css
.header {
  background-color: var(--color-primary);
  color: #FFFFFF;
  padding: var(--spacing-md) 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-logo {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-bold);
  color: #FFFFFF;
}

.header-nav {
  display: flex;
  gap: var(--spacing-xl);
}

.header-nav-item {
  color: #FFFFFF;
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: opacity 0.3s ease;
}

.header-nav-item:hover {
  opacity: 0.8;
}
```

**Layout**: Logo on left, navigation items center/right. Can be fixed on scroll with simplified style.

### Content Card

```css
.card {
  background-color: var(--color-neutral-surface);
  border-radius: var(--border-radius-md);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-xl);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  margin-bottom: var(--spacing-lg);
}

.card-title {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.card-body {
  color: var(--color-neutral-text);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--spacing-lg);
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}
```

**Structure**: Card can include image/icon at top, title, brief description, and CTA button.

### Icons

```css
.icon {
  width: 20px;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
}

.icon-lg {
  width: 24px;
  height: 24px;
}

.icon-sm {
  width: 16px;
  height: 16px;
}
```

**Principle**: Use simple linear icons (SVG), unified size 20px–24px when aligned with text.

### Form Inputs

```css
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: block;
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-medium);
  color: var(--color-neutral-text);
  margin-bottom: var(--spacing-sm);
}

.form-input {
  width: 100%;
  padding: 10px 16px;
  font-size: var(--font-size-body);
  font-family: var(--font-family-base);
  color: var(--color-neutral-text);
  background-color: var(--color-neutral-surface);
  border: var(--border-width) var(--border-style) var(--border-color-default);
  border-radius: var(--border-radius-md);
  transition: border-color 0.3s ease;
}

.form-input:focus {
  border-color: var(--border-color-focus);
  outline: none;
}

.form-input:disabled {
  background-color: var(--color-disabled-bg);
  color: var(--color-disabled-text);
  cursor: not-allowed;
}

.form-error {
  color: var(--color-error);
  font-size: var(--font-size-small);
  margin-top: var(--spacing-xs);
}

.form-success {
  color: var(--color-success);
  font-size: var(--font-size-small);
  margin-top: var(--spacing-xs);
}
```

## 7. Images & Media (图像与媒体)

### Image Guidelines

```css
.img-responsive {
  max-width: 100%;
  height: auto;
  display: block;
}

.img-rounded {
  border-radius: var(--border-radius-md);
}

.img-cover {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

/* Aspect Ratios */
.aspect-ratio-16-9 {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.aspect-ratio-4-3 {
  aspect-ratio: 4 / 3;
  overflow: hidden;
}
```

**Principles**:
- Use high-quality, high-contrast images to enhance visual appeal
- Images in content blocks align with text (left image right text or vertical arrangement)
- Maintain consistent crop ratios, such as 16:9
- Images should align with group business themes (insurance, pension, asset management), showing professionalism and trust

## 8. Accessibility & Interaction (可访问性与交互)

### Accessibility Requirements

```css
/* Focus States */
*:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Skip Links */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: #FFFFFF;
  padding: var(--spacing-sm);
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}

/* ARIA Support */
[aria-hidden="true"] {
  display: none;
}

[aria-disabled="true"] {
  cursor: not-allowed;
  opacity: 0.6;
}
```

### Interaction States

```css
/* Hover States */
.interactive:hover {
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

/* Active States */
.interactive:active {
  opacity: 0.6;
  transform: scale(0.98);
}

/* Loading States */
.loading {
  position: relative;
  pointer-events: none;
}

.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid var(--color-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**Requirements**:
- Primary color contrast must be sufficient
- Button/link state changes must be obvious (hover/active)
- Form input feedback must be clear (success/error prompts)
- Use ARIA labels throughout the page to enhance accessibility

## 9. Responsive Design (响应式设计)

### Breakpoints

```css
:root {
  --breakpoint-sm: 576px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 992px;
  --breakpoint-xl: 1200px;
}

/* Mobile First Approach */
@media (min-width: 768px) {
  .container {
    padding: 0 var(--spacing-xl);
  }
  
  h1 { font-size: 40px; }
  h2 { font-size: 32px; }
}

@media (min-width: 992px) {
  h1 { font-size: 48px; }
  h2 { font-size: 36px; }
}

/* Mobile Navigation */
@media (max-width: 767px) {
  .header-nav {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
}
```

## 10. Complete Style Example (完整样式示例)

### Base Styles

```css
:root {
  /* Colors */
  --color-primary: #0A3B73;
  --color-secondary: #5B7DB1;
  --color-accent: #D4AF37;
  --color-neutral-bg: #F7F8FA;
  --color-neutral-surface: #FFFFFF;
  --color-neutral-border: #F0F0F0;
  --color-neutral-text: #333333;
  
  /* Typography */
  --font-family-base: "PingFang SC", "Noto Sans", "Microsoft YaHei", Arial, sans-serif;
  --font-size-body: 18px;
  
  /* Spacing */
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* Layout */
  --container-max-width: 1200px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family-base);
  font-size: var(--font-size-body);
  color: var(--color-neutral-text);
  background-color: var(--color-neutral-bg);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3 {
  color: var(--color-primary);
  font-weight: 700;
}

a {
  color: var(--color-accent);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--color-accent-hover);
}
```

## Best Practices

1. **Color Usage**: Always use CSS variables for colors, never hardcode color values
2. **Typography**: Use semantic HTML tags (h1-h6) and apply styles via classes
3. **Spacing**: Use spacing scale variables, maintain consistent rhythm
4. **Components**: Build reusable components following the design system
5. **Responsive**: Mobile-first approach, test on multiple devices
6. **Accessibility**: Include ARIA labels, ensure keyboard navigation, maintain color contrast ratios
7. **Performance**: Optimize images, use CSS transforms for animations
8. **Consistency**: Follow the spacing scale, use consistent border radius values

## Prohibited Patterns

- ❌ Do NOT use colors outside the defined palette
- ❌ Do NOT use arbitrary spacing values (always use spacing scale)
- ❌ Do NOT use heavy borders (prefer shadows and light borders)
- ❌ Do NOT ignore hover/active/focus states
- ❌ Do NOT use serif fonts for body text
- ❌ Do NOT create components that don't follow the design system
- ❌ Do NOT use inline styles (use CSS classes and variables)
- ❌ Do NOT ignore accessibility requirements

## Summary: Core Style Keywords

✅ **简约大气 (Simple & Elegant)**: Generous whitespace, clear modules, clean and intuitive content presentation

✅ **专业稳重 (Professional & Stable)**: Deep blue primary color + sans-serif fonts convey financial trust

✅ **响应式兼容 (Responsive)**: Single layout system adapts to PC/tablet/mobile

✅ **信息优先 (Information First)**: Use dividers and whitespace to organize content areas, highlighting key data and core business
