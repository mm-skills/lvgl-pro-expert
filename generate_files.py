import os

skill_dir = "/Users/mcneillm/Documents/Projects/skills/lvgl-pro-expert"
upstream_dir = os.path.join(skill_dir, "references", "upstream")
os.makedirs(upstream_dir, exist_ok=True)

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# A) official-agents-guide.md
agents_content = read_file("/tmp/agents2.md")
write_file(os.path.join(upstream_dir, "official-agents-guide.md"), agents_content)

# C) cli-and-ai-tools.md
ai_content = read_file("/tmp/ai.md")
cli_content = read_file("/tmp/cli.md")
cli_tools = f"# CLI and AI Tools\n\n## AI Integration\n{ai_content}\n\n## CLI\n{cli_content}"
write_file(os.path.join(upstream_dir, "cli-and-ai-tools.md"), cli_tools)

# F) translations.md
trans_content = read_file("/tmp/translations.md")
write_file(os.path.join(upstream_dir, "translations.md"), trans_content)

# B) official-examples.md
examples = []
for xml_file in ["round_button.xml", "sliderbox.xml", "section.xml", "globals.xml", "project.xml", "hello_world.xml", "data_bindings.xml", "layout.xml", "animations.xml"]:
    content = read_file(f"/tmp/{xml_file}")
    if content:
        examples.append(f"### {xml_file}\n```xml\n{content}\n```\n")

write_file(os.path.join(upstream_dir, "official-examples.md"), "# Official Examples\n\n" + "\n".join(examples))

# For D, E, G, H we will just append the new info
with open(os.path.join(skill_dir, "references", "format", "data-binding.md"), "a") as f:
    f.write("\n\n## Official Update\n" + read_file("/tmp/data-binding.md"))

with open(os.path.join(skill_dir, "references", "format", "animations.md"), "a") as f:
    f.write("\n\n## Official Update\n" + read_file("/tmp/animations.md"))

with open(os.path.join(skill_dir, "references", "targets", "ecosystems-overview.md"), "a") as f:
    f.write("\n\n## Official Update\n" + read_file("/tmp/targets.md"))

print("Files generated successfully.")
