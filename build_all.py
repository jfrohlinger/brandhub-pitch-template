"""
build_all.py
════════════════════════════════════════════════════════════════════════════════
brandhub pitch deck builder — generates one index.html per client from the
shared template (brandhub-presentation.html).

HOW TO USE
──────────
1. Edit brandhub-presentation.html to update shared content (platform features,
   case studies, pricing, etc.).
2. Add or update a client config in the CLIENTS list below.
3. Run:  python3 build_all.py
4. Push each client's output file to its GitHub Pages repo.

ADD A NEW CLIENT
──────────────────
Copy one of the existing entries in CLIENTS, change the values, set output_path
to wherever that client's repo lives on your machine.
════════════════════════════════════════════════════════════════════════════════
"""

import re, os, sys

# ── Paths ─────────────────────────────────────────────────────────────────────
TEMPLATE = os.path.join(os.path.dirname(__file__), "brandhub-presentation.html")

# ── Client definitions ────────────────────────────────────────────────────────
# output_path: absolute path where index.html should be written.
# config: the full content of the <script id="client-config"> block (JS only,
#         no surrounding <script> tags — those are added automatically).
# ─────────────────────────────────────────────────────────────────────────────

CLIENTS = [

  # ── Heaven Hill ─────────────────────────────────────────────────────────────
  {
    "id":          "heaven-hill",
    "output_path": os.path.join(os.path.dirname(__file__), "index.html"),

    # Heaven Hill keeps the default config already baked into template.html,
    # so we set config=None to just copy the template as-is.
    "config": None,
  },

  # ── Pernod Ricard ────────────────────────────────────────────────────────────
  {
    "id":          "pernod",
    "output_path": os.path.join(
        os.path.dirname(__file__),
        "../../OneDrive-SelectDesignLtd/Pitch Decks/Pernod/index.html"
    ),
    "config": """
  /* ── Identity ────────────────────────────────────────────────────────── */
  name: "Pernod Ricard",
  sub:  "Global Spirits Leader",

  logoImg: "",

  /* ── Emblem ──────────────────────────────────────────────────────────── */
  emblemInitials:  "PR",
  emblemColor1:    "#00205B",
  emblemColor2:    "#003DA5",
  emblemShadow:    "rgba(0,32,91,.4)",
  emblemTextColor: "#FFFFFF",

  /* ── Atlas ───────────────────────────────────────────────────────────── */
  atlasUrl:  "https://brandhub-demo-atlas.streamlit.app/",
  atlasDesc: "Bluetooth beacons in your displays ping phones and VIP's fleet network in real time. Watch a display travel from production through the VIP hub, to retail floor — every step tracked.",

  /* ── Email CTAs ──────────────────────────────────────────────────────── */
  emailDemo:  "brandhub Demo Request - Pernod",
  emailRoi:   "brandhub ROI Model Request - Pernod",
  emailPilot: "brandhub Pilot Program - Pernod",

  /* ── Competitor label ────────────────────────────────────────────────── */
  competitor: "Proof & Vineyards / IMS",

  /* ── Priorities ──────────────────────────────────────────────────────── */
  priorities: [
    {
      icon: "🌍", title: "Global Brand Consistency",
      links: [
        { href: "#platform",     label: "Multi-market brand governance" },
        { href: "#ai-features",  label: "Atlas display tracking demo" },
        { href: "#case-studies", label: "99.7% on-time delivery result" }
      ]
    },
    {
      icon: "💵", title: "Cost Optimization",
      links: [
        { href: "#calculator",   label: "Build your ROI model" },
        { href: "#comparison",   label: "Compare your options" },
        { href: "#case-studies", label: "48% more product, same spend" }
      ]
    },
    {
      icon: "📦", title: "Distributor Execution",
      links: [
        { href: "#ai-features",  label: "Smart ordering demo" },
        { href: "#platform",     label: "How brandhub manages stock" },
        { href: "#case-studies", label: "33% vendor savings case study" }
      ]
    }
  ]
""",
  },

  # ── Proximo Spirits ──────────────────────────────────────────────────────────
  # Uncomment and fill in when ready.
  # {
  #   "id":          "proximo",
  #   "output_path": "/path/to/brandhub_proximo/index.html",
  #   "config": """
  #   name: "Proximo Spirits",
  #   sub:  "Premium Spirits Portfolio",
  #   logoImg: "",
  #   emblemInitials:  "PX",
  #   emblemColor1:    "#1A1A2E",
  #   emblemColor2:    "#16213E",
  #   emblemShadow:    "rgba(26,26,46,.4)",
  #   emblemTextColor: "#E8C97A",
  #   atlasUrl:  "https://brandhub-demo-atlas.streamlit.app/",
  #   atlasDesc: "Watch a display travel from production through the VIP hub, to retail floor — every step tracked.",
  #   emailDemo:  "brandhub Demo Request - Proximo",
  #   emailRoi:   "brandhub ROI Model Request - Proximo",
  #   emailPilot: "brandhub Pilot Program - Proximo",
  #   competitor: "Proof & Vineyards / IMS",
  #   priorities: [
  #     { icon: "🥃", title: "Portfolio Execution", links: [
  #       { href: "#platform",     label: "Multi-brand management" },
  #       { href: "#ai-features",  label: "Smart ordering demo" },
  #       { href: "#case-studies", label: "48% more product, same spend" }
  #     ]},
  #     { icon: "💵", title: "Cost Optimization", links: [
  #       { href: "#calculator",   label: "Build your ROI model" },
  #       { href: "#comparison",   label: "Compare your options" },
  #       { href: "#case-studies", label: "33% vendor savings case study" }
  #     ]},
  #     { icon: "👁️", title: "Distributor Visibility", links: [
  #       { href: "#ai-features",  label: "Atlas beacon tracking demo" },
  #       { href: "#why-exist",    label: "See the full platform map" },
  #       { href: "#case-studies", label: "99.7% on-time delivery result" }
  #     ]}
  #   ]
  # """,
  # },

  # ── Diageo ───────────────────────────────────────────────────────────────────
  # {
  #   "id":          "diageo",
  #   "output_path": "/path/to/brandhub_diageo/index.html",
  #   "config": """
  #   name: "Diageo",
  #   sub:  "World's Leading Premium Spirits",
  #   logoImg: "",
  #   emblemInitials:  "DG",
  #   ...
  # """,
  # },

]

# ── Config block template wrapper ─────────────────────────────────────────────
def wrap_config(inner_js):
    return (
        '<script id="client-config">\n'
        '/* ═══════════════════════════════════════════════════════════════════════════\n'
        '   CLIENT CONFIG — Edit ONLY this block to personalise for a new client.\n'
        '   Copy this entire file and update the values below.\n'
        '   Everything else (platform features, case studies, pricing) is shared.\n'
        '   ═══════════════════════════════════════════════════════════════════════════ */\n'
        'const CLIENT = {\n'
        + inner_js +
        '\n};\n'
        '/* ═══════════════════════════════════════════════════════════════════════════\n'
        '   END CLIENT CONFIG\n'
        '   ═══════════════════════════════════════════════════════════════════════════ */\n'
        '</script>'
    )

# ── Build ─────────────────────────────────────────────────────────────────────
CONFIG_PATTERN = re.compile(
    r'<script id="client-config">.*?</script>',
    re.DOTALL
)

def build():
    if not os.path.exists(TEMPLATE):
        print(f"✗ Template not found: {TEMPLATE}")
        sys.exit(1)

    with open(TEMPLATE, "r") as f:
        template_html = f.read()

    if not CONFIG_PATTERN.search(template_html):
        print("✗ No <script id=\"client-config\"> block found in template.")
        sys.exit(1)

    print(f"Template: {TEMPLATE}")
    print(f"Building {len(CLIENTS)} client(s)...\n")

    errors = []

    for client in CLIENTS:
        cid   = client["id"]
        out   = os.path.normpath(os.path.join(os.path.dirname(TEMPLATE), client["output_path"])) \
                if not os.path.isabs(client["output_path"]) \
                else client["output_path"]
        cfg   = client.get("config")

        # Heaven Hill uses template as-is; others get their config injected
        if cfg is None:
            html = template_html
        else:
            new_block = wrap_config(cfg)
            html = CONFIG_PATTERN.sub(new_block, template_html, count=1)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(out), exist_ok=True)

        try:
            with open(out, "w") as f:
                f.write(html)
            print(f"  ✓ [{cid}] → {out}")
        except Exception as e:
            print(f"  ✗ [{cid}] Failed: {e}")
            errors.append(cid)

    print()
    if errors:
        print(f"⚠️  {len(errors)} build(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {len(CLIENTS)} client build(s) complete.")
        print()
        print("Next steps:")
        print("  1. Review each output file in a browser")
        print("  2. Push index.html to each client's GitHub Pages repo")

if __name__ == "__main__":
    build()
