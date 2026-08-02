# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee External Assignment Agreement - Revenue Recognition",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
        "Michael Viriyananda <viriyananda.michael@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "ssi_employee_external_assignment_agreement",
        "ssi_revenue_recognition",
        "web_tour",
    ],
    "data": [
        "views/employee_external_assignment_type.xml",
        "views/employee_external_assignment_agreement.xml",
        "views/performance_obligation_acceptance.xml",
        "views/assets.xml",
    ],
}
