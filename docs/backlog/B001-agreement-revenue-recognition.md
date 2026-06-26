# B001 — Integrasi Revenue Recognition (PSAK 115) untuk Employee External Assignment Agreement

| Field | Nilai |
| --- | --- |
| **ID** | B001 |
| **Status** | PLANNING |
| **Prioritas** | 🟢 tinggi |
| **Modul target** | `ssi_employee_external_assignment_agreement_revenue_recognition` (baru) |
| **Repo** | ssi-employee-external-assignment |
| **Dibuat** | 2026-06-26 |

> Glue module (meniru `ssi_service_revenue_recognition`) yang menghubungkan
> `employee_external_assignment_agreement` ke engine `performance_obligation` (PoB) di
> `ssi_revenue_recognition`, dan mengotomasi pembuatan PoB dari agreement.

---

## 1. Konteks & Tujuan

Membuat modul jembatan yang mengotomasi pembuatan **Performance Obligation (PoB)** dari
`employee_external_assignment_agreement`, mengikuti pola modul referensi
`ssi_service_revenue_recognition` (yang menghubungkan `service.contract` → PoB via
`account.analytic.account`).

Engine PoB ada di repo lain (`ssi-revenue-recognition`, modul `ssi_revenue_recognition`)
dan menerapkan PSAK 115 (IFRS 15). PoB terhubung ke "kontrak" hanya lewat
`source_analytic_account_id` (sebuah `account.analytic.account`) — **bukan** lewat
field langsung ke model transaksi. Pola ini wajib dipertahankan.

## 2. Analisa Desain

### 2.1 Analisa PSAK 115 (IFRS 15)

**Substansi transaksi:** labor-supply / outsourcing — entitas memasok tenaga kerja per
job position sepanjang periode agreement, ditagih per periode dari payslip aktual +
management fee + other/variable fee.

| Langkah PSAK 115 | Pemetaan di desain ini |
| --- | --- |
| 1. Identifikasi kontrak | Agreement → `account.analytic.account`-nya (sudah dibuat di `action_open`, post_open_action `_10_create_analytic_account`). |
| 2. Identifikasi PoB | **Per `detail` (job position)** = 1 PoB. Pasokan bulanan satu peran = "series of distinct services, same pattern of transfer" (para 22–23) → 1 PoB **over time**. Ditambah 1 PoB untuk tiap `other_fee`, `variable_fee`, dan management fee (sesuai keputusan scope). |
| 3. Tentukan harga transaksi | Dari compensation term / engine payment-term (digerakkan payslip aktual). |
| 4. Alokasi harga ke PoB | Per-PoB; bersinggungan dengan `pob_planned_amount` di engine (gap G2/D1 di `ssi-revenue-recognition`, **di luar scope** modul ini). |
| 5. Akui pendapatan | **Over time, per periode saat lapse**, jumlah = **gaji aktual yang ditagih di periode itu** → ini **as-invoiced practical expedient (PSAK 115 para B16)**: hak atas imbalan berkorelasi langsung dengan nilai yang ditransfer. |

### 2.2 Keputusan terkunci (hasil tanya-jawab dengan user)

| Kode | Keputusan |
| --- | --- |
| K1 — Grain PoB | **Per `detail` (job position)** = 1 PoB. |
| K2 — Timing & metode | **Over time, per periode lapse**; yang ditagih & diakui = gaji aktual yang dibayar di periode tersebut (as-invoiced / B16). |
| K3 — Scope elemen | **Detail + other fee + variable fee + management fee** semuanya jadi PoB. |
| K4 — Otomasi acceptance | Analisa kelayakan dilakukan (lihat §2.4); rekomendasi: PoB-creation dulu (Fase 1), otomasi acceptance jadi Fase 2. |
| K5 — Fulfillment method | **Payslip-line linkage**: glue modul extend `performance_obligation_acceptance` dengan `payslip_line_ids` (Many2many → `hr.payslip.line`) + computed float `qty_payslip_fulfillment = sum(payslip_line_ids.total)`. Field ini didaftarkan sebagai `fulfillment_field_id` pada PoB detail. Fase 2 mengisi `payslip_line_ids` secara otomatis. |

### 2.3 Constraint engine PoB (terverifikasi dari source)

`performance_obligation` inherit `mixin.product_line_price`, sehingga:

- `product_id` **required** → tiap PoB butuh produk representatif.
- `price_unit` **required**; `price_subtotal = price_unit × uom_quantity`.
- `amount_accepted = qty_accepted × price_unit` (proporsi qty terhadap harga tetap).
- Fulfillment diukur lewat `performance_obligation_acceptance.qty_fulfilled` (via
  `fulfillment_field_id`).

**Konvensi jumlah pengakuan (dikunci — K5):**
konvensi **amount-as-quantity** untuk PoB tenaga kerja: `price_unit = 1.0`,
`uom_quantity = 0.0` (diisi manual di PoB form setelah dibuat), dan tiap acceptance
periode `qty_fulfilled` dibaca dari `qty_payslip_fulfillment` (sum total payslip lines
yang di-link ke acceptance tersebut). Revenue yang diakui **persis sama** dengan tagihan
aktual periode itu. `fulfillment_field_id` diarahkan ke `qty_payslip_fulfillment`.

### 2.4 Analisa kelayakan otomasi acceptance (K4)

**Kesimpulan: layak, dengan satu kompleksitas nyata.**

Agreement sudah punya engine periodik: `payment_term` → memuat `external_assignment_ids`
+ `payslip_ids` → membangun `rule_ids` (per salary rule) → membuat invoice. Saat
`payment_term` mencapai `done`, periode (`date_start/date_end`) dan jumlah tertagih
diketahui.

- **Trigger:** `@ssi_decorator.post_done_action()` pada
  `employee_external_assignment_agreement.payment_term` → auto-buat satu
  `performance_obligation_acceptance` per PoB terdampak untuk periode itu, lalu isi
  `payslip_line_ids` dengan payslip lines yang relevan.
- **Kompleksitas (harus dipecahkan):** `rule_ids` payment-term dikelompokkan per *salary
  rule*, sedangkan PoB per *detail/job*. Jalur resolusi:
  `payslip_line.slip_id.employee_id` → `external_assignment.employee_id` →
  `external_assignment.job_id` → `agreement.detail.job_id` → PoB detail tersebut.
  Kumpulkan semua `payslip_line` per detail, link ke `payslip_line_ids` acceptance →
  `qty_payslip_fulfillment` terhitung otomatis.
- **Rekomendasi:** kirim **pembuatan PoB** dulu (Fase 1, `payslip_line_ids` diisi manual),
  lalu lapisi **otomasi pengisian `payslip_line_ids`** sebagai **Fase 2** setelah
  pemetaan rule→detail tervalidasi di data nyata.

### 2.5 Desain extend `performance_obligation_acceptance` (K5)

Glue modul extend model engine dengan field baru tanpa memodifikasi engine:

```python
# models/performance_obligation_acceptance.py
class PerformanceObligationAcceptance(models.Model):
    _name = "performance_obligation_acceptance"
    _inherit = ["performance_obligation_acceptance"]

    payslip_line_ids = fields.Many2many(
        comodel_name="hr.payslip.line",
        relation="pob_acceptance_payslip_line_rel",
        column1="acceptance_id",
        column2="payslip_line_id",
        string="Payslip Lines",
    )
    qty_payslip_fulfillment = fields.Float(
        string="Payslip Fulfillment Amount",
        compute="_compute_qty_payslip_fulfillment",
        store=True,
        digits="Account",
    )

    @api.depends("payslip_line_ids.total")
    def _compute_qty_payslip_fulfillment(self):
        for rec in self:
            rec.qty_payslip_fulfillment = sum(rec.payslip_line_ids.mapped("total"))
```

Saat `action_create_pob` di detail, `fulfillment_field_id` di-set ke field
`qty_payslip_fulfillment` (dicari via `ir.model.fields`):

```python
fulfillment_field = self.env["ir.model.fields"].search([
    ("model", "=", "performance_obligation_acceptance"),
    ("name", "=", "qty_payslip_fulfillment"),
], limit=1)
```

## 3. Rencana Implementasi

### Struktur modul

```
ssi_employee_external_assignment_agreement_revenue_recognition/
├── __init__.py
├── __manifest__.py          # depends: ssi_employee_external_assignment_agreement, ssi_revenue_recognition; auto_install=True
├── models/
│   ├── __init__.py
│   ├── employee_external_assignment_type.py          # + pob_analytic_group_id, pob_product_id (labor), config
│   ├── employee_external_assignment_agreement.py     # + pob_ids, amount_total_pob, amount_diff_pob, action_open_pob; post_open_action _20_ wiring
│   ├── employee_external_assignment_agreement_detail.py        # + pob_id compute, action_create_pob, _prepare_pob_data (over_time/input/payslip)
│   ├── employee_external_assignment_agreement_other_fee.py     # + pob_id compute, action_create_pob (point_in_time)
│   ├── employee_external_assignment_agreement_variable_fee.py  # + pob_id compute, action_create_pob (point_in_time)
│   ├── performance_obligation_acceptance.py          # + payslip_line_ids, qty_payslip_fulfillment
│   └── employee_external_assignment_agreement_payment_term.py  # Fase 2: post_done_action → auto acceptance + isi payslip_line_ids
├── views/
│   ├── employee_external_assignment_type.xml         # pob_analytic_group_id, pob_product_id
│   ├── employee_external_assignment_agreement.xml    # tombol "Create PoB" per baris + halaman "Performance Obligations"
│   └── performance_obligation_acceptance.xml         # kolom/field payslip_line_ids di form acceptance
├── README.rst
├── i18n/  (.pot via CI, jangan manual)
└── static/description/icon.png
```

Tidak perlu security/menu baru (glue, seperti `ssi_service_revenue_recognition`).

### Fase 1 — PoB auto-creation (inti)

1. Scaffold modul + `__manifest__.py` + `__init__.py` + header copyright + `README.rst` +
   icon; sinkronkan file config standar repo.
2. Extend `employee_external_assignment_type`: tambah `pob_analytic_group_id` dan
   `pob_product_id` (produk jasa tenaga kerja representatif, untuk mengisi `product_id`
   PoB yang required), plus config timing per-elemen bila perlu.
3. Extend `performance_obligation_acceptance`: tambah `payslip_line_ids` (Many2many →
   `hr.payslip.line`) dan `qty_payslip_fulfillment` (computed float, store=True) sesuai
   §2.5. Tambah view field `payslip_line_ids` di form acceptance.
4. Extend `employee_external_assignment_agreement`: `pob_ids` (compute dari
   `analytic_account_id` → `source_analytic_account_id`), `amount_total_pob` /
   `amount_diff_pob`, `action_open_pob`, dan `@post_open_action()` bernomor `_20_` untuk
   backfill `source_analytic_account_id` ke PoB yang belum ter-link (AA baru ada setelah
   `_10_create_analytic_account` di modul sumber).
5. Extend `detail`: `pob_id` compute + `action_create_pob` + `_prepare_pob_data` →
   `revenue_recognition_timing="over_time"`, `progress_completion_method="input"`,
   `price_unit=1.0`, `uom_quantity=0.0`, produk dari `type_id.pob_product_id`,
   `fulfillment_field_id` → field `qty_payslip_fulfillment` (dicari via `ir.model.fields`).
6. Extend `other_fee` dan `variable_fee`: `pob_id` compute + `action_create_pob` →
   `point_in_time`, `fulfillment_field_id` → `qty_manual_fulfillment` (bawaan engine).
7. Views: tombol "Create PoB" per baris detail/other_fee/variable_fee + halaman
   "Performance Obligations" di agreement; field config di type; `payslip_line_ids` di
   form acceptance.
8. Install/upgrade di Docker
   (`invoke install -m ssi_employee_external_assignment_agreement_revenue_recognition`);
   smoke test manual.

### Fase 2 — otomasi acceptance (commit terpisah)

9. Extend `payment_term` dengan `@post_done_action()`: untuk tiap PoB detail terdampak
   periode ini, buat satu `performance_obligation_acceptance` + isi `payslip_line_ids`
   dengan payslip lines yang relevan. Mapping: `payslip_line.slip_id.employee_id` →
   `external_assignment.employee_id` → `external_assignment.job_id` →
   `agreement.detail.job_id` → PoB detail. `qty_payslip_fulfillment` terhitung otomatis.
10. Unit test (`SavepointCase`, tagged) untuk pembuatan PoB + pemetaan acceptance.

**Commit:** per-modul, `[ADD] ssi_employee_external_assignment_agreement_revenue_recognition`;
push via `rebase-repo.sh` + `push-odoo-module-revision.sh 14.0` (hanya saat user minta).

## 4. Open Items / Risiko

- ~~Konvensi jumlah pengakuan~~ — **Dikunci (K5)**: amount-as-quantity via
  `qty_payslip_fulfillment`.
- Sumber `pob_product_id`: satu produk representatif per type (paling simpel, cukup untuk
  Fase 1).
- Apakah management fee jadi PoB tersendiri atau dilebur ke PoB tenaga kerja.
- Fase 2: ambiguitas pemetaan payslip line → detail bila satu employee mengisi lebih dari
  satu job/detail dalam satu agreement (resolusi: filter by `external_assignment.job_id`
  yang aktif di periode payment_term).

---

## Progress Log

- 2026-06-26 — Perencanaan — dokumen rencana B001 dibuat dari analisa modul referensi
  (`ssi_service_revenue_recognition`), engine `ssi_revenue_recognition`, dan struktur
  `ssi_employee_external_assignment_agreement`. Keputusan K1–K4 dikunci. Belum ada kode.
- 2026-06-26 — Refinement — analisa kode referensi terverifikasi (pola `pob_ids` compute,
  `post_open_action _20_`, `fulfillment_field_id`). Keputusan K5 dikunci: fulfillment via
  `payslip_line_ids` + `qty_payslip_fulfillment` di extend `performance_obligation_acceptance`.
  Struktur modul, langkah Fase 1, dan langkah Fase 2 diperbarui. Plan siap dieksekusi.
