# CLI and AI Tools

## AI Integration
---
title: AI Integration
description: Connect AI assistants to LVGL Pro through the LVGL MCP server for grounded documentation answers, and close the loop with the CLI for validation and visual feedback.
---

LVGL Pro is built to work hand-in-hand with AI coding assistants. Three pieces make this possible:

- **The LVGL MCP server** gives the AI accurate, up-to-date knowledge of LVGL and LVGL Pro, so it stops guessing APIs.
- **The [`lvgl_pro` repo](#lvgl_pro-repo-real-xml-to-learn-from)** gives it real, valid XML to read: the schema of every built-in widget, plus example and template projects.
- **The [CLI](/cli)** gives the AI objective validation and *eyes*. It can validate XML, generate code, and screenshot the result to verify its own work.

This page covers the MCP server and the repo. For the validation-and-screenshot loop, see the [CLI page](/cli).

## The LVGL MCP server

The LVGL MCP server is a hosted [Model Context Protocol](https://modelcontextprotocol.io) server, powered by [kapa.ai](https://www.kapa.ai), that answers questions from LVGL's official documentation, forum, and source knowledge with links back to the sources.

Connecting it to your AI assistant means answers are grounded in the real, current docs instead of the model's training data, which is often outdated for a fast-moving library like LVGL.

<Callout type="info">
The server endpoint is `https://lvgl.mcp.kapa.ai/`. It is read-only: it returns documentation answers and never edits or runs your code.
</Callout>

## Using it

LVGL Pro projects ship with the MCP configuration already in place (in the project's `.claude` folder), so supported tools detect it as soon as you open the project.

1. **Open the project** in your AI assistant (e.g. Claude Code) from the project root.
2. **Approve & authenticate.** On first use, the assistant asks you to approve the server, then walks you through a one-time login. After that it stays connected.
3. **Ask in plain language.** You don't call the server directly. The assistant invokes it on its own when a question needs LVGL knowledge. A few examples:
   - *"Create a new screen with 3 sliders and labels showing the sliders' current value."* 
   - *"How do I create a chart with two series in LVGL?"*
   - *"dashboard.xml is too complex. Split it into smaller components."*

Phrasing like *"look up"* or *"check the LVGL docs"* nudges the assistant to consult the server rather than answer from memory.

<Callout type="info">
In Claude Code, run `/mcp` to confirm the `lvgl` server is connected and to see the tools it exposes.
</Callout>

## Adding it manually

If your project doesn't already include the configuration, add it yourself. For **Claude Code**, create a `.claude/.mcp.json` file in your project's root:

```json
{
  "mcpServers": {
    "lvgl": {
      "type": "http",
      "url": "https://lvgl.mcp.kapa.ai/"
    }
  }
}
```

Restart the assistant (or reload the project) and approve the server when prompted.

Other tools use the same idea but look for a different file in a slightly different shape. Most reuse the `mcpServers` structure above. The main differences are the file location and, for VS Code/Copilot, the top-level key (`servers` instead of `mcpServers`):

| Tool | Config file |
| --- | --- |
| Claude Code | `.mcp.json` (project root) or `~/.claude.json` (global) |
| Cursor | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global) |
| GitHub Copilot (VS Code) | `.vscode/mcp.json`, uses the `servers` key |
| Gemini CLI | `.gemini/settings.json` (project) or `~/.gemini/settings.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |

## `lvgl_pro` repo: Real XML to learn from

Docs explain the concepts, but agents write better XML when they can read actual, valid XML. The
[lvgl/lvgl_pro](https://github.com/lvgl/lvgl_pro) repository is exactly that, and it's public:

| Path | What's in it |
| --- | --- |
| [`lvgl_widgets_xml/`](https://github.com/lvgl/lvgl_pro/tree/master/lvgl_widgets_xml) | The **XML schema of every built-in LVGL widget**, one folder per LVGL version (e.g. `v9.5.0/`), one `<widget>` file per widget (`lv_slider.xml`, `lv_chart.xml`, ...). Each lists the exact properties, parameters, enums, and elements the tag accepts, with `help` texts. This is the source of truth for "what can I write on this tag?". |
| [`examples/lvgl_open/`](https://github.com/lvgl/lvgl_pro/tree/master/examples/lvgl_open) | 130+ small, focused example screens (widgets, layouts, styles, scrolling) in one runnable project. `examples/lvgl_pro/` next to it holds the one-per-widget examples embedded in these docs. |
| [`tutorials/`](https://github.com/lvgl/lvgl_pro/tree/master/tutorials) | A tutorial project with one screen per concept: styles, layouts, animations, assets, data bindings, translations, custom components and widgets, testing. |
| [`templates/`](https://github.com/lvgl/lvgl_pro/tree/master/templates) | The `basic` project template (a small design system plus reusable components) and the `empty` one. |
| [`docs/`](https://github.com/lvgl/lvgl_pro/tree/master/docs) | The source of this documentation, as plain Markdown. |

Two ways for an agent to use it:

**Clone it once** into a temp folder and grep around freely. This is the cheapest option when the assistant needs
to look up several things:

```bash
git clone --depth 1 https://github.com/lvgl/lvgl_pro /tmp/lvgl_pro
grep -rn "start_angle" /tmp/lvgl_pro/lvgl_widgets_xml/v9.5.0/
```

**Or fetch single files** over raw HTTP when only one answer is needed:

```bash
curl -s https://raw.githubusercontent.com/lvgl/lvgl_pro/master/lvgl_widgets_xml/v9.5.0/lv_slider.xml
```

<Callout type="info">
Pick the `lvgl_widgets_xml` folder that matches the `lvgl_version` in your project's `project.xml`.
The same widget API is also rendered as documentation under [Built-in Widgets](/built_in_widgets), which
the MCP server can search.
</Callout>

## The AI development loop

The MCP server gives the AI *knowledge*; the [CLI](/cli) closes the loop with *validation* and *eyes*. Together they let the assistant write, check, and visually verify a UI on its own:

<Steps>
<Step>
**Ask**: the AI consults the MCP server to check the details of LVGL Open or Pro features, and reads the widget XML and examples from the [`lvgl_pro` repo](#lvgl_pro-repo-real-xml-to-learn-from) for concrete syntax.
</Step>
<Step>
**Write**: it writes or edits XMLs based on the user's request and the information it learned
</Step>
<Step>
**Validate**: run `validate` with the CLI and it returns precise, machine-readable errors to fix, then repeat until clean. `generate` and `compile` with the CLI are also recommended after some iterations to catch all issues.
</Step>
<Step>
**See**: `screenshot` renders the screen to a PNG.
</Step>
<Step>
**Judge**: a vision-capable model compares the image to the intent and iterates from step 1.
</Step>
</Steps>

See the [CLI page](/cli) for the full command reference and a ready-to-use CI/CD example.


## CLI
---
title: CLI
description: The LVGL Pro command-line tool generates and compiles C code, validates and tests XML UIs, and captures screenshots — built for CI/CD pipelines and AI-driven workflows.
---

The CLI, along with the [Editor](./editor/overview), [Figma plugin](./figma), and [online viewer](./online-viewer), is part of **LVGL Pro**, a professional toolkit to develop embedded UIs.

The LVGL Pro CLI is a command line tool bringing the great power of the Editor to the terminal. It's an npm-installed `lvglpro` command that generates and compiles C code from your XML, validates projects, runs headless UI tests, and captures screenshots, all without opening the GUI.

Because it's scriptable and headless, the CLI is the bridge between LVGL Pro and your automation: continuous integration, regression testing, and AI agents that write, validate, and visually verify UI on their own.

<Callout type="warn">
    The CLI is a **Professional feature** and is **not available with the Community and Evaluation licenses**. See
    [pricing and plans](https://pro.lvgl.io/pricing) to unlock it.
</Callout>

## Why use the CLI?

<Cards>
    <Card title="Run in CI/CD">
        Generate C code, compile, and run UI tests on every push. Catch regressions before they merge, no GUI, no manual
        steps.
    </Card>
    <Card title="Close the AI loop">
        Let an AI write XML, then `validate` it for instant, machine-readable feedback and `screenshot` it so a vision
        model can see the result and iterate.
    </Card>
    <Card title="Reproducible builds">
        The same command produces the same C code locally and on your build server. `compare` it against a reference to
        guarantee deterministic output.
    </Card>
</Cards>

## Installation

1. **Install Node.js** 18 or newer (CI is tested on Node 22).
2. **Install the CLI** globally with npm:

```bash
npm install --global @lvgl/lvglpro
```

This puts `lvglpro` on your `PATH`.

```bash
lvglpro --help
```

### Authentication

The CLI requires a Product or Platform license token. Provide it in one of two ways:

- **Environment variable (recommended):** set `LVGLPRO_CLI_TOKEN` and the CLI picks it up automatically. This is the best fit for CI, where you'd store the token as an encrypted secret.
- **Command-line flag:** pass `--token <your-token>` on any command.

```bash
# Picked up automatically from the environment
export LVGLPRO_CLI_TOKEN="your-token"
lvglpro generate path/to/project

# Or pass it explicitly
lvglpro generate path/to/project --token "your-token"
```

<Callout type="warn">
    Treat the token like a password. Prefer `LVGLPRO_CLI_TOKEN` over `--token` so it doesn't leak into shell history or
    CI logs, and never commit it to your repository.
</Callout>

## Quick start

```bash
# Generate C and H files from your XML project
lvglpro generate path/to/project

# Validate XML and report problems
lvglpro validate path/to/project

# Compile and run all UI tests headlessly
lvglpro run-all-tests path/to/project

# Capture a screen as a PNG
lvglpro screenshot path/to/project screens/home.xml --out home.png
```

## Commands

### Reference

| Command         | Purpose                                      |
| --------------- | -------------------------------------------- |
| `generate`      | Generate C/H code from XML                   |
| `compile`       | Compile the project (`--target editor\|cli`) |
| `validate`      | Validate XML and report errors               |
| `run-test`      | Run a single UI test                         |
| `run-all-tests` | Run all UI tests                             |
| `screenshot`    | Capture a screen as a PNG                    |
| `compare`       | Compare generated code against a reference   |

Run `lvglpro <command> --help` for the full, up-to-date options of any command.

### generate

Generate C and H code from the project's XML files.

```bash
lvglpro generate <project-path> [options]
```

| Option            | Description           |
| ----------------- | --------------------- |
| `--ignore-fonts`  | Skip font conversion  |
| `--ignore-images` | Skip image conversion |

### compile

Compile the project into a runnable binary (runtime) for previewing or testing.

The runtime contains the compiled LVGL, the C code of the UI project, and some editor-specific C code. It is required to run the UI in the Editor or in the CLI.

```bash
lvglpro compile <project-path> [options]
```

| Option                   | Description                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| `--target <editor\|cli>` | Build target: `editor` creates a runtime for the Editor application, `cli` one to be used for testing. |

### validate

Check the project's XML for errors and report them. Exits non-zero on failure, so it doubles as a gate in CI and a fast feedback signal for AI agents.

```bash
lvglpro validate <project-path> [options]
```

| Option                 | Description                       |
| ---------------------- | --------------------------------- |
| `-l, --errorlimit <n>` | Maximum number of errors to print |

### run-test / run-all-tests

Run headless UI interaction tests defined in XML. `run-test` runs one file; `run-all-tests` discovers and runs every test in the project.

```bash
lvglpro run-test <project-path> <testing-file> [options]
lvglpro run-all-tests <project-path> [options]
```

| Option           | Description                                                             |
| ---------------- | ----------------------------------------------------------------------- |
| `--slowdown <n>` | Slow execution down N times for debugging (`0` = no delay, the default) |

`<testing-file>` is the path to a test XML, relative to `<project-path>`.

### screenshot

Render a screen and save it as a PNG. Perfect for visual diffs and AI vision feedback.

```bash
lvglpro screenshot <project-path> <screen> [options]
```

| Option         | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| `--out <file>` | Output file name for the screenshot                                 |
| `--delay <ms>` | Wait before capturing, e.g. to let animations settle (default: `0`) |

`<screen>` is the path of the screen to capture, relative to `<project-path>`.

### compare

Compare two project directories by file presence and normalized content. Use it to assert that generated output matches a known-good reference.

```bash
lvglpro compare <generated-path> <reference-path>
```

## Use case: CI/CD pipelines

Run the CLI on every pull request to generate code, compile it, and run your UI tests automatically. Here's a GitHub Actions workflow that does exactly that:

```yaml
name: LVGL Pro Check
on: [push, pull_request]

jobs:
    ui-check:
        runs-on: ubuntu-latest
        env:
            # Store your Pro license token as an encrypted repository secret
            LVGLPRO_CLI_TOKEN: ${{ secrets.LVGLPRO_CLI_TOKEN }}
        steps:
            - uses: actions/checkout@v4

            - uses: actions/setup-node@v4
              with:
                  node-version: '22'

            - name: Install CLI
              run: npm install --global @lvgl/lvglpro

            - name: Generate code
              run: lvglpro generate examples

            - name: Compile to run tests
              run: lvglpro compile examples --target cli

            - name: Run UI tests
              run: lvglpro run-all-tests examples
```

## Use case: AI-driven UI development

The CLI gives an AI agent two things a language model otherwise lacks: **objective validation** and **eyes**. Together they form a closed feedback loop the model can run on its own.

1. **Generate**: the AI writes or edits XML for a component or screen.
2. **Validate**: `validate` returns precise, machine-readable errors. The AI fixes them and repeats until the project is clean. `generate` can also be used to export code.
3. **See**: `screenshot` renders the screen to a PNG.
4. **Judge**: a vision-capable model inspects the image, compares it to the intent, and decides what to change.
5. **Iterate**: back to step 1 until the UI looks right.

```bash
# 1–2: write XML, then check it
lvglpro validate path/to/project --errorlimit 25
lvglpro generate path/to/project

# 3: render what the user will actually see
lvglpro screenshot path/to/project screens/home.xml --out home.png --delay 200
```
