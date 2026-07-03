# docs/ — Dokumentasi kerja repo `ssi-employee-external-assignment`

Folder ini menyimpan **dokumen kerja internal** (rencana fitur, analisa desain, catatan
keputusan) yang dibaca AI & tim sebelum mengerjakan fitur. Ini **bukan** dokumentasi
pengguna dan **bukan** README modul.

> Bahasa: dokumen kerja boleh Bahasa Indonesia. Catatan: **konten di dalam modul Odoo**
> (label field, `_description`, help, README.rst modul) tetap **wajib Bahasa Inggris**
> sesuai standar SSI.

## Struktur

```
docs/
├── README.md          # file ini — menjelaskan mekanisme
├── BACKLOG.md         # register (index) seluruh item backlog — SUMBER KEBENARAN status
└── backlog/
    ├── TEMPLATE.md    # template untuk item backlog baru
    └── B<NNN>-<slug>.md   # satu file per item backlog (rencana/analisa detail)
```

## Mekanisme Backlog

Backlog = daftar pekerjaan yang **direncanakan / belum selesai** (fitur, perbaikan,
analisa desain). Setiap item backlog punya:

1. **Satu baris di [BACKLOG.md](BACKLOG.md)** — register ringkas: ID, judul, status,
   prioritas, modul target, link ke dokumen detail.
2. **Satu file detail di `backlog/B<NNN>-<slug>.md`** — rencana lengkap, analisa,
   langkah implementasi, dan **Progress Log** item tersebut.

### Cara menambah item backlog

1. Tentukan ID berikutnya: `B001`, `B002`, … (lihat nomor terakhir di `BACKLOG.md`).
2. Salin `backlog/TEMPLATE.md` → `backlog/B<NNN>-<slug>.md`, isi header & konten.
3. Tambahkan satu baris ke tabel di `BACKLOG.md`.

### Status item (lifecycle)

`PLANNING` → `APPROVED` → `IN PROGRESS` → `DONE` (atau `ON HOLD` / `CANCELLED`).

Ubah status **di dua tempat**: baris di `BACKLOG.md` dan header file detailnya. Saat ada
kode yang landing, catat di **Progress Log** file detail (format:
`YYYY-MM-DD — <fase> — <module> v<versi> — <ringkasan> — <commit>`).

### Saat item selesai (`DONE`)

File detail tetap disimpan sebagai arsip keputusan (jangan dihapus); statusnya menjadi
`DONE` di register. Pengetahuan permanen yang masih relevan untuk pemeliharaan
dipindahkan ke `README.md` repo atau `CLAUDE.md` (bila ada).
