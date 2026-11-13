---
name: architectural-floor-plan-generator
description: This prompt instructs the AI to act as a professional architect and produce a clean, CAD/blueprint-style, top-down floor plan for a house using the provided style, size/layout, room list, special features, and optional site context. The expected outcome is a computer-drawn schematic with clearly separated and labeled rooms, accurately indicated walls, doors, windows, stairs, and any requested elements (e.g., terrace, pool, rooftop garden) integrated logically into the layout, presented with precise lines and clear proportions.
compatibility: Requires betterprompt >= 0.1.3
metadata:
  openclaw:
    homepage: https://github.com/BetterPromptme/skills
    emoji: 🧩
    requires:
      anyBins:
        - betterprompt
        - bp
    os:
      - linux
      - darwin
    install:
      - id: node
        kind: node
        package: betterprompt
        bins: [betterprompt, bp]
        label: Install BetterPrompt CLI (node)
---

## What it does

This prompt instructs the AI to act as a professional architect and produce a clean, CAD/blueprint-style, top-down floor plan for a house using the provided style, size/layout, room list, special features, and optional site context. The expected outcome is a computer-drawn schematic with clearly separated and labeled rooms, accurately indicated walls, doors, windows, stairs, and any requested elements (e.g., terrace, pool, rooftop garden) integrated logically into the layout, presented with precise lines and clear proportions.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Rooms` | Required |  | (none) |
| `Layout` | Required |  | (none) |
| `Features` | Required |  | (none) |
| `Environment` | Required |  | (none) |
| `House_Style` | Required |  | (none) |



### Models and options

This skill's modality is: **`image`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"image"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "image"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:


- Required text inputs:
    - `Rooms`
  - `Layout`
  - `Features`
  - `Environment`
  - `House_Style`
- Optional: model and options.
  - Present the human with the default model **`gpt-image-1`** and its available options. Look up `gpt-image-1` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"quality":"medium"}`.
  - If the human does not specify, defaults are used: model `gpt-image-1`, options `{"quality":"medium"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `architectural-floor-plan-generator`).

Command form:

```bash
betterprompt generate architectural-floor-plan-generator \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-image-1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"quality":"medium"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate architectural-floor-plan-generator \
  --input Rooms=<value> \
  --input Layout=<value> \
  --input Features=<value> \
  --input Environment=<value> \
  --input House_Style=<value> \
  --model gpt-image-1 \
  --options '{"quality":"medium"}'
```
## Adaptación Local (Oleiros, A Coruña - España)
- Todas las medidas, cotas, escalas y superficies deben expresarse exclusivamente en **metros (m) y metros cuadrados (m²)** (prohibido usar pies o pulgadas).
- La normativa de habitabilidad y dimensiones mínimas debe regirse por las **Normas do Hábitat Galego (NHG)** y el **Código Técnico de la Edificación (CTE - Zona Climática C1)**.
- Los parámetros urbanísticos (edificabilidad, ocupación, retranqueos y alturas) deben ajustarse al **PXOM del Concello de Oleiros** (zona Liáns / Santa Cruz).
