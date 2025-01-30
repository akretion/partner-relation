import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-akretion-partner-relation",
    description="Meta package for akretion-partner-relation Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-partner_relation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 9.0',
    ]
)
