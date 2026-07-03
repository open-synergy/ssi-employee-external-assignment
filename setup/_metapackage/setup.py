import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-employee-external-assignment",
    description="Meta package for open-synergy-ssi-employee-external-assignment Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_employee_external_assignment',
        'odoo14-addon-ssi_employee_external_assignment_agreement',
        'odoo14-addon-ssi_employee_external_assignment_agreement_operating_unit',
        'odoo14-addon-ssi_employee_external_assignment_agreement_revenue_recognition',
        'odoo14-addon-ssi_employee_external_assignment_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
