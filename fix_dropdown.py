#!/usr/bin/env python3
"""Fix all pages: make nav-center a hidden dropdown on mobile, visible with .open class."""
import os, re

BASE = '/tmp/bisia-mockup'
pages = [
    'landing-4-warm', 'landing-b1-forum', 'landing-b2-mercato', 'landing-b3-news',
    'landing-b4-groups', 'landing-b5-directory', 'landing-b6-drawer',
    'landing-c1-community', 'landing-c3-events', 'landing-profile-matteo',
    'settings', 'signup',
]

for name in pages:
    path = os.path.join(BASE, f'{name}.html')
    with open(path, 'r') as f:
        content = f.read()

    # 1. Add default .nav-center dropdown CSS (hidden by default)
    # Insert BEFORE the first @media or before </style>
    dropdown_css = """
        .nav-center {
            position: fixed; top: 60px; left: 0; right: 0; bottom: 0;
            background: rgba(10,10,12,0.98); backdrop-filter: blur(20px);
            display: flex; flex-direction: column; gap: 0.5rem;
            padding: 1.25rem 1.5rem; overflow-y: auto;
            transform: translateY(-110%); transition: transform 0.3s ease;
            pointer-events: none; opacity: 0;
        }
        .nav-center.open { transform: translateY(0); pointer-events: auto; opacity: 1; }
        .nav-center a { color: var(--gray-300); text-decoration: none; font-size: 1rem; font-weight: 500; padding: 0.6rem 0; border-bottom: 1px solid var(--gray-800); transition: color 0.2s; }
        .nav-center a:hover { color: var(--white); }
        .nav-center a.active { color: var(--accent); }"""

    # Check if dropdown CSS already exists
    if 'position: fixed; top: 60px; left: 0; right: 0; bottom: 0;' in content:
        print(f'SKIP {name}.html — dropdown CSS already present')
        continue

    # Find where to insert: before first @media, or before </style>
    media_match = re.search(r'(\s*)@media\s*\(', content)
    if media_match:
        content = content[:media_match.start()] + dropdown_css + content[media_match.start():]
    else:
        content = content.replace('</style>', dropdown_css + '\n    </style>')

    # 2. Update mobile @media: add .nav-center display:none
    # The mobile rule should hide nav-center (it's already hidden by the default dropdown CSS)
    # But add it explicitly for safety
    mobile_insert = '.nav-center { display: none; }'
    
    # Check if mobile @media already has this
    if 'max-width: 768px' in content:
        # Replace the opening of the mobile rule to include nav-center hide
        content = content.replace(
            '@media (max-width: 768px) {',
            '@media (max-width: 768px) { .nav-center { display: none; }',
            1  # only first occurrence
        )
    
    # 3. Desktop @media already has the nav-center inline rule — that's correct

    with open(path, 'w') as f:
        f.write(content)

    print(f'✓ {name}.html')
