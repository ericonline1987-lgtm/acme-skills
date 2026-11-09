# Sources

- W3C, Understanding SC 1.4.3 Contrast (Minimum) — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C, Understanding SC 1.4.10 Reflow — https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- W3C, Understanding SC 1.4.4 Resize Text — https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
- W3C ACT Rule, Meta viewport allows for zoom — https://www.w3.org/WAI/standards-guidelines/act/rules/b4f0c3/
- W3C, Understanding SC 2.1.1 Keyboard — https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
- W3C, Understanding SC 4.1.2 Name, Role, Value — https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
- W3C, Understanding SC 1.4.1 Use of Color — https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- W3C, Understanding SC 2.4.7 Focus Visible — https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- W3C WAI Tutorials, Labeling Controls — https://www.w3.org/WAI/tutorials/forms/labels/
- W3C WAI Tutorials, Form Instructions (placeholder is not a label) — https://www.w3.org/WAI/tutorials/forms/instructions/

## Grader basis

- contrast-hint-and-button: SC 1.4.3 (4.5:1 normal text; 15px/600 is not "large text"). Ratios computed with the WCAG relative-luminance formula: #999/#fff = 2.85:1, #fff/#4caf50 = 2.78:1.
- zoom-and-reflow: ACT rule b4f0c3 (user-scalable=no fails 1.4.4); SC 1.4.10 Reflow (320 CSS px, no two-dimensional scrolling).
- div-button: SC 2.1.1 Keyboard (F54 pointer-only handlers); SC 4.1.2 (F59 div/span control without role).
- error-not-color-only: SC 1.4.1 (F81 error fields identified by colour only).
- input-overflow: CSS box model (content-box width excludes padding and border: 480 + 24 + 2 = 506px). Layout practitioner knowledge; no single cited page.

## Why a capable general model might miss it

Generic reviews list the familiar items (alt text, labels, outline) and skip quantified contrast on brand-coloured buttons, the viewport meta zoom/reflow failure, and CSS box-model bugs that "look fine on a laptop".

The page is synthetic.
