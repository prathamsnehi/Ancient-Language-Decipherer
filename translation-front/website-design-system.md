\# Remi Website Design System

This document serves as a comprehensive guide to replicating the look, feel, and structure of the Remi public website. It is intended to help other developers or LLMs build new pages and components that perfectly match the existing brand aesthetics.

\## 1. Core Philosophy & Brand Essence

\- \*\*Vibe:\*\* Friendly, inviting, app-like, modern, and deeply human.

\- \*\*Goal:\*\* To feel less like a corporate software product and more like a personal, thoughtful tool for human connection.

\- \*\*Key Visual Traits:\*\* Extremely rounded corners, soft tinted shadows, playful entrance animations, and bold, rounded typography.

\## 2. Typography

The website uses a dual-font strategy relying on system fonts to ensure fast loading and a native app feel across platforms (especially Apple devices).

\- \*\*Body Text (Sans-serif):\*\*

&#x20; \- \*\*Font family:\*\* \`-apple-system\`, \`BlinkMacSystemFont\`, \`SF Pro Display\`, \`Segoe UI\`, \`Roboto\`, \`Helvetica\`, \`Arial\`, \`sans-serif\`

&#x20; \- \*\*Usage:\*\* Standard text, paragraphs, labels, small UI elements.&#x20;

&#x20; \- \*\*Tailwind Class:\*\* \`font-sans\` (set as default for \`body\`).

&#x20; \- \*\*Color:\*\* Typically \`text-muted-foreground\` for paragraphs to reduce harshness.

\- \*\*Headings (Rounded):\*\*

&#x20; \- \*\*Font family:\*\* \`ui-rounded\`, \`SF Pro Rounded\`, \`-apple-system\`, etc.

&#x20; \- \*\*Usage:\*\* All headings (\`h1\` through \`h6\`) and anything meant to pop or look "app-like" (like prominent module titles or large CTA text).

&#x20; \- \*\*Tailwind Class:\*\* Defaults on \`h1\`-\`h6\` tags or explicitly apply \`font-rounded\`.

&#x20; \- \*\*Color:\*\* Standard primary heading text is \`text-foreground\`. In multi-part headings, emphasize key words natively with \`text-primary\`.

\## 3. Colors

All colors are managed as CSS variables in HSL format for robust theme support (Light and Dark modes).

\- \*\*Primary Color (Green):\*\*

&#x20; \- \*\*HSL:\*\* \`151 55% 42%\` (a friendly, active green).

&#x20; \- \*\*Usage:\*\* Primary buttons, icons, highlights, and accent glows.

\- \*\*Backgrounds:\*\*

&#x20; \- \*\*Light Mode:\*\* Off-white/gray base \`240 14% 95%\`.

&#x20; \- \*\*Dark Mode:\*\* Pure black \`0 0% 0%\`.

\- \*\*Surfaces & Cards:\*\*

&#x20; \- Standard popovers/cards use pure white (\`0 0% 100%\`) in light mode and off-black (\`0 0% 10%\`) in dark mode. Surface utilities occasionally use \`bg-surface\`.

\- \*\*Gradients:\*\*

&#x20; \- Background sections often use subtle overlays: \`bg-gradient-to-br from-primary/5 via-transparent to-primary/10\`.

&#x20; \- Gradient on primary badges/icons: \`from-primary/80 to-primary\`.

\## 4. Shapes & Borders

The design heavily leans on large border radiuses to construct its friendly appeal.

\- \*\*Base Radius:\*\* \`1rem\` (used for standard cards and components).

\- \*\*Extreme Rounding:\*\* Large structural cards (like the CTA panel) and app mockups use \`rounded-\[2rem]\` or \`rounded-\[2.5rem]\`.

\- \*\*Buttons & Pills:\*\* Distinct action CTAs and badges should almost always be \`rounded-full\`.

\- \*\*Borders:\*\* Very subtle, often lightly tinted green in light mode (\`hsl(141, 84%, 85%)\`).

\## 5. Shadows and Effects

Flat design is avoided. Depth is established through soft, tinted shadows and background blurs.

\- \*\*Soft Shadows:\*\* The custom \`--shadow-soft\` applies a slight green-tinted drop shadow (\`0 4px 20px -4px hsl(151 55% 42% / 0.15)\`).

\- \*\*Hover Shadows:\*\* Elevate elements gracefully on hover with \`--shadow-hover\`.

\- \*\*Glow Effects (App Mockups):\*\* Images and showcased app screens sit on top of pulsing background layers:

&#x20; \`\`\`html

&#x20; \<div class="absolute inset-0 rounded-\[2.5rem] blur-3xl bg-primary/20" />

&#x20; \`\`\`

\## 6. Layout & Spacing

\- \*\*Max Widths:\*\* Content sections are constrained mostly to \`max-w-6xl\` or \`max-w-4xl\` for focused CTAs, centered via \`mx-auto\`.

\- \*\*Padding:\*\* Copious amounts of breathing room. Sections often carry \`py-20\` or \`py-24\`.

\- \*\*Grid Systems:\*\* Standard side-by-side text/image layouts use \`grid lg:grid-cols-2 gap-12 items-center\`.

\## 7. Component Patterns

When building new UI pieces, follow these established patterns:

\### Primary Buttons (Download CTAs)

\- \*\*Styling:\*\* \`bg-primary text-primary-foreground\`

\- \*\*Class Composition:\*\* Needs to look massive and inviting: \`rounded-full px-8 py-6 text-lg font-rounded shadow-lg\`.

\- \*\*Interactions:\*\* Combine a shadow lift with a size bump: \`transition-\[box-shadow,transform] duration-300 hover:scale-105 hover:shadow-xl\`.

\### Section Headers / Badges

\- Above the \`h2\` title, place a small contextual pill:

&#x20; \`\`\`tsx

&#x20; \<Badge className="px-4 py-2 text-sm font-medium bg-primary/10 text-primary border-none rounded-full">

&#x20; The Remi Experience

&#x20; \</Badge>

&#x20; \`\`\`

\### Imagery

\- Application mockups apply a soft \`transition-transform duration-500\` and are usually paired with Framer Motion entry animations.

\## 8. Animations

\*\*Framer Motion\*\* (\`framer-motion\`) is the standard for almost every interaction.

\- \*\*Scroll Entrances:\*\* Use \`whileInView={{ opacity: 1, y: 0 }}\` paired with \`initial={{ opacity: 0, y: 30 }}\` and \`viewport={{ once: true }}\`. Standard duration is \`0.8s\`.

\- \*\*Staggered Sequences:\*\* Stagger entry text sections (\`h1\`, followed by \`p\`, followed by \`Button\`) using delays in increments of \`0.1s\` or \`0.2s\`.

\- \*\*Continuous Background motion:\*\* Use \`scale: \[1, 1.05, 1]\` or \`opacity: \[0.4, 0.6, 0.4]\` infinitely looped for backdrops (\`repeat: Infinity, repeatType: "reverse"\`).

\## 9. Icons

\- Standard icons rely on \*\*Lucide React\*\* (e.g. \`\<Heart />\`, \`\<Search />\`).

\- Brand and filled bold platform icons utilize \*\*Ionicons\*\* via web components (e.g., \`\<ion-icon name="logo-apple">\</ion-icon>\`) for immediate visual impact.
