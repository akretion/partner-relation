import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-akretion-partner-relation",
    description="Meta package for akretion-partner-relation Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-partner_relation>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
