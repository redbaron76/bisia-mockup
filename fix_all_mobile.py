#!/usr/bin/env python3
"""Fix ALL 12 pages: mobile nav-center uses transform hiding (not display:none) so .open class works."""
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

    # Problem: mobile @media has .nav-center { display: none; }
    # which prevents the .open class from working.
    # We need to REPLACE the mobile hide with transform hiding.
    
    # Strategy:
    # 1. In the mobile @media, replace '.nav-center { display: none; }'
    #    with nothing (the default CSS already handles hiding via transform)
    # 2. Make sure default .nav-center has transform hiding and .nav-center.open shows it
    
    # Check for mobile display:none
    if '.nav-center { display: none; }' in content:
        # Remove the mobile display:none — the default CSS will handle hiding
        content = content.replace(
            '.nav-center { display: none; }',
            ''
        )
        print(f'removed mobile display:none in {name}.html')

    # Now ensure default nav-center has proper dropdown hiding
    # Find the default .nav-center rule and update it
    # There should be a .nav-center { ... display: flex ... } default rule
    
    # Check if dropdown hiding CSS exists
    has_dropdown = 'transform: translateY(-110%)' in content
    
    if not has_dropdown:
        # Add dropdown hiding to default .nav-center
        # The default rule should be: .nav-center { position: static; ... }
        # We need to change it to use transform hiding on mobile
        # Actually, we should make the default rule work on mobile (hidden) and desktop override makes it visible
        
        # Add a media query for mobile that sets the dropdown behavior
        mobile_dropdown = """        @media (max-width: 1024px) {
            .nav-center { position: fixed; top: 60px; left: 0; right: 0; bottom: 0; background: rgba(10,10,12,0.98); backdrop-filter: blur(20px); display: flex; flex-direction: column; gap: 0.5rem; padding: 1.25rem 1.5rem; overflow-y: auto; transform: translateY(-110%); transition: transform 0.3s ease; pointer-events: none; opacity: 0; }
            .nav-center.open { transform: translateY(0); pointer-events: auto; opacity: 1; }
            .nav-center a { color: var(--gray-300); text-decoration: none; font-size: 1rem; font-weight: 500; padding: 0.6rem 0; border-bottom: 1px solid var(--gray-800); transition: color 0.2s; }
            .nav-center a:hover { color: var(--white); }
            .nav-center a.active { color: var(--accent); }
        }"""
        
        # Find where to insert: before first @media that starts with (max-width
        max_media = re.search(r'(\s*)@media\s*\(max-width', content)
        if max_media:
            content = content[:max_media.start()] + mobile_dropdown + content[max_media.start():]
        else:
            content = content.replace('</style>', mobile_dropdown + '\n    </style>')
        
        print(f'added dropdown CSS in {name}.html')

    with open(path, 'w') as f:
        f.write(content)

    print(f'✓ {name}.html')
