import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-employee-external-assignment",
    description="Meta package for open-synergy-ssi-employee-external-assignment Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_employee_external_assignment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
