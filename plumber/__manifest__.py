{
    "name": "Plumber",
    "version": "1.0",
    "category": "Services",
    "summary": "Plumbing Dispatch Management Module",
    "description": """
    This module lets you manage plumbing job requests. That's it so far.
    """,
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/dispatch_request_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
