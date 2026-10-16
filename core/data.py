"""All portfolio content lives here so it is easy to edit in one place."""

PROFILE = {
    "name": "Farhan Alam",
    "short_name": "Farhan",
    "email": "farhanalam8510@gmail.com",
    "location": "Kanpur, Uttar Pradesh, India",
    "github": "https://github.com/farhanalam851",
    "linkedin": "https://www.linkedin.com/in/farhan-alam-b590b8408",
    "instagram": "https://www.instagram.com/webby_farhan",
    "instagram_handle": "@webby_farhan",
    "stat_projects": 4,
    "stat_tech": 9,
    "reply_hours": 24,
    "roles": [
        "Django developer",
        "Python full-stack builder",
        "REST API engineer",
        "BCA student, shipping real projects",
    ],
}

# Logos for the moving strips (devicon slugs). "invert" = dark glyph that needs lightening in dark mode.
LOGOS_ROW_1 = [
    {"name": "HTML5", "icon": "html5/html5-original.svg"},
    {"name": "CSS3", "icon": "css3/css3-original.svg"},
    {"name": "JavaScript", "icon": "javascript/javascript-original.svg"},
    {"name": "Python", "icon": "python/python-original.svg"},
    {"name": "Django", "icon": "django/django-plain.svg", "invert": True},
    {"name": "Bootstrap", "icon": "bootstrap/bootstrap-original.svg"},
]
LOGOS_ROW_2 = [
    {"name": "PostgreSQL", "icon": "postgresql/postgresql-original.svg"},
    {"name": "MySQL", "icon": "mysql/mysql-original.svg"},
    {"name": "SQLite", "icon": "sqlite/sqlite-original.svg"},
    {"name": "Git", "icon": "git/git-original.svg"},
    {"name": "GitHub", "icon": "github/github-original.svg", "invert": True},
    {"name": "VS Code", "icon": "vscode/vscode-original.svg"},
]

SKILLS = [
    {"name": "Python", "icon": "python/python-original.svg", "tag": "Core language",
     "text": "Backend logic, automation and clean, readable code behind every project."},
    {"name": "Django", "icon": "django/django-plain.svg", "invert": True, "tag": "Main framework",
     "text": "Auth, ORM models, admin, orders, invoices and production deployments."},
    {"name": "Django REST Framework", "icon": "django/django-plain.svg", "invert": True, "tag": "APIs",
     "text": "Serializers, validation, routing and CRUD endpoints ready for any frontend."},
    {"name": "JavaScript", "icon": "javascript/javascript-original.svg", "tag": "Interactivity",
     "text": "DOM, events, localStorage and modular code for fast, lively interfaces."},
    {"name": "HTML5", "icon": "html5/html5-original.svg", "tag": "Structure",
     "text": "Semantic, accessible markup that search engines and screen readers love."},
    {"name": "CSS3", "icon": "css3/css3-original.svg", "tag": "Styling",
     "text": "Responsive layouts, animation and design that does not look like a template."},
    {"name": "Bootstrap", "icon": "bootstrap/bootstrap-original.svg", "tag": "UI toolkit",
     "text": "Grid, components and utilities, customised so sites feel unique."},
    {"name": "SQL Databases", "icon": "postgresql/postgresql-original.svg", "tag": "PostgreSQL / MySQL / SQLite",
     "text": "Relational design for customers, products and orders that stays consistent."},
    {"name": "Git & GitHub", "icon": "git/git-original.svg", "tag": "Workflow",
     "text": "Version control and clean repositories you can actually review."},
]

PROJECTS = [
    {
        "title": "F.F Manufacturer - Leather Belts Store",
        "kind": "Client project - Django",
        "featured": True,
        "summary": "A retail and wholesale store for a Kanpur leather-belt manufacturer, with "
                   "verified business accounts, GST invoicing and pan-India shipping.",
        "points": [
            "Men and women categories with product reviews and ratings",
            "Wholesale registration with GSTIN verification and bulk pricing",
            "Cart, checkout, order tracking and customer accounts",
        ],
        "stack": ["Django", "Bootstrap", "JavaScript", "SQL"],
        "link": "https://github.com/farhanalam851/ffmanufacturer",
        "live_url": "https://ffmanufacturer.vercel.app/",
    },
    {
        "title": "Lala Sarees - Saree Store",
        "kind": "Client project - Django",
        "summary": "An elegant online saree shop for a Kanpur retailer, covering collections, "
                   "occasions and wholesale buyers.",
        "points": [
            "Collections and occasion filters (wedding, party, festive, bridal)",
            "Bag, checkout with UPI, cards and COD, plus GST invoices",
            "Wholesale enquiries for boutiques and verified businesses",
        ],
        "stack": ["Django", "Bootstrap", "JavaScript", "SQL"],
        "link": "https://github.com/farhanalam851/lalasarees_site",
        "live_url": "https://lalasarees-site.vercel.app/",
    },
    {
        "title": "Django REST API",
        "kind": "Backend - DRF",
        "summary": "CRUD-oriented API with serializers, validation and clean URL routing, "
                   "built to power any web or mobile client.",
        "points": ["Model serialization and request validation",
                   "Request / response handling with DRF"],
        "stack": ["Django REST Framework", "Python"],
        "link": "https://github.com/farhanalam851",
    },
    {
        "title": "JavaScript Mini Apps",
        "kind": "Frontend - JavaScript",
        "summary": "Amazon clone, Todo list, Tic Tac Toe, Rock Paper Scissors and a calculator "
                   "that sharpen DOM, events and state skills.",
        "points": ["localStorage persistence", "Modular, event-driven code"],
        "stack": ["JavaScript", "HTML", "CSS"],
        "link": "https://github.com/farhanalam851",
    },
]

SERVICES = [
    {"icon": "bi-briefcase", "title": "Business websites",
     "text": "Fast, professional sites for companies, shops and individuals that make you look credible online."},
    {"icon": "bi-bag-check", "title": "E-commerce stores",
     "text": "Catalogues, carts, orders, payments and invoices, built on the same stack as my client stores."},
    {"icon": "bi-window-stack", "title": "Custom web apps",
     "text": "Dashboards, portals and internal tools shaped around how your business really works."},
    {"icon": "bi-diagram-3", "title": "REST APIs",
     "text": "Secure, documented Django REST endpoints for your frontend or mobile app."},
    {"icon": "bi-cloud-arrow-up", "title": "Deployment & upkeep",
     "text": "Your site live, secure and kept running smoothly after launch."},
]

PROCESS = [
    ("01", "Talk", "You tell me the goal, audience and deadline. I reply within a day."),
    ("02", "Plan", "We agree scope, pages and features before any code is written."),
    ("03", "Build", "Frontend, backend and database, with progress you can see."),
    ("04", "Launch", "Deployment, handover and support when something needs a tweak."),
]

JOURNEY = [
    {"when": "Now", "title": "BCA, Dr. Virendra Swarup Institute of Computer Studies",
     "text": "Currently pursuing a Bachelor of Computer Applications while building client-style projects."},
    {"when": "Building", "title": "Freelance web development",
     "text": "Taking on websites and web apps for businesses through Instagram @webby_farhan."},
    {"when": "Before", "title": "Class XII, The Ganges World School",
     "text": "Where the interest in computers turned into a plan to build for the web."},
]

FOCUS = ["Full-stack web development", "Django & DRF", "JavaScript", "REST APIs",
         "Database design", "Production-ready client projects"]
