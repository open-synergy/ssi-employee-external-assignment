.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================================
Employee External Assignment Agreement - Revenue Recognition
==========================================================================

Glue module that bridges ``employee_external_assignment_agreement`` to the
Performance Obligation (PoB) engine in ``ssi_revenue_recognition``, enabling
PSAK 115 (IFRS 15) revenue recognition for labor-supply / outsourcing agreements.

Each agreement detail (job position) maps to one PoB with ``over_time`` timing
and as-invoiced recognition (PSAK 115 para B16) via payslip line linkage.
Other fees and variable fees each map to a ``point_in_time`` PoB.


Work Instruction
================

Employee External Assignment Type
-----------------------------------

* `Create Employee External Assignment Type <docs/employee_external_assignment_type/01-create.html>`_

Employee External Assignment Agreement
-----------------------------------------

* `Create Employee External Assignment Agreement <docs/employee_external_assignment_agreement/01-create.html>`_
* `Edit Employee External Assignment Agreement <docs/employee_external_assignment_agreement/02-edit.html>`_
* `Approve Employee External Assignment Agreement <docs/employee_external_assignment_agreement/05-approve.html>`_
* `Create PoB - Employee External Assignment Agreement <docs/employee_external_assignment_agreement/07-create-pob.html>`_

Employee External Assignment Agreement Payment Term
-------------------------------------------------------

* `Approve Employee External Assignment Agreement Payment Term <docs/employee_external_assignment_agreement_payment_term/05-approve.html>`_


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-employee-external-assignment/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
