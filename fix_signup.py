#!/usr/bin/env python3
"""Fix signup.html specifically: add mobile hide + dropdown CSS + ensure no stray JS."""
import os, re

path = '/tmp/bisia-mockup/signup.html'
with open(path, 'r') as f:
    content = f.read()

# 1. Replace the mobile @media rule to include .nav-center { display: none; }
old_mobile = '@media (max-width: 768px) { .hamburger { display: flex; } .nav-overlay { display: block; } .page { padding-left: 1rem; padding-right: 1rem; } .form-row { grid-template-columns: 1fr; } }'
new_mobile = '@media (max-width: 768px) { .nav-center { display: none; } .hamburger { display: flex; } .nav-overlay { display: block; } .page { padding-top: 5.5rem; padding-left: 1rem; padding-right: 1rem; } .form-row { grid-template-columns: 1fr; } }'

content = content.replace(old_mobile, new_mobile)

# 2. Add dropdown CSS (hidden by default, shown with .open)
# The existing rules have .nav-center as position: static (inline visible)
# We need to override: default state should be hidden (dropdown)
dropdown_rules = """
        @media (max-width: 1024px) {
            .nav-center { position: fixed; top: 60px; left: 0; right: 0; bottom: 0; background: rgba(10,10,12,0.98); backdrop-filter: blur(20px); display: flex; flex-direction: column; gap: 0.5rem; padding: 1.25rem 1.5rem; overflow-y: auto; transform: translateY(-110%); transition: transform 0.3s ease; pointer-events: none; opacity: 0; }
            .nav-center.open { transform: translateY(0); pointer-events: auto; opacity: 1; }
            .nav-center a { color: var(--gray-300); text-decoration: none; font-size: 1rem; font-weight: 500; padding: 0.6rem 0; border-bottom: 1px solid var(--gray-800); transition: color 0.2s; }
            .nav-center a:hover { color: var(--white); }
            .nav-center a.active { color: var(--accent); }
        }"""

# Check if dropdown rules already exist
if '@media (max-width: 1024px)' not in content:
    # Insert before the last </style>
    content = content.replace('</style>', dropdown_rules + '\n    </style>')

# 3. Check for stray JS and wrap if needed
# The JS toggle should be inside <script> tag
js_pattern = r"</script>\s*\s*document\.getElementById\('hamburger'\)"
if re.search(js_pattern, content):
    # There's stray JS — find it and remove
    stray_match = re.search(js_pattern, content)
    if stray_match:
        stray_start = stray_match.start()
        # Find </body> to remove stray content up to it
        body_end = content.find('</body>', stray_start)
        if body_end != -1:
            content = content[:stray_start] + content[body_end:]
            # Re-add JS in proper script tag
            js_block = """document.getElementById('hamburger').addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('open');
            document.getElementById('nav-center').classList.toggle('open');
            document.getElementById('nav-overlay').classList.toggle('open');
        });
        document.getElementById('nav-overlay').addEventListener('click', function() {
            document.getElementById('hamburger').classList.remove('open');
            document.getElementById('nav-center').classList.remove('open');
            document.getElementById('nav-overlay').classList.remove('open');
        });"""
            content = content.replace('</body>', f'<script>\n        {js_block}\n    </script>\n</body>')

with open(path, 'w') as f:
    f.write(content)

print('Fixed signup.html')
