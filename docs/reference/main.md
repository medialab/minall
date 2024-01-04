---
icon: material/file-code-outline
---

# Minall

To facilitate the project's use as a Python library and as a CLI tool, `minall`'s workflow is managed via an exportable class, `Minall`.

By creating a class instance of `Minall`, the following preliminary steps are taken:

- API credentials for the `minet` clients are parsed. (param: `config`)
- File paths to the workflow's eventual output, CSV files for the target URLs (`links.csv`) and their shared content (`shared_content.csv`), are prepared. This includes the creation of any necessary parent directories. (param: `out_dir`)
- The SQLite database connection is created. The connection can either be in-memory or, if a file path is provided, to an embedded SQLite database. If the user wants `Minall` to create and store the workflow's results in an SQLite database file, simply providing a file path will also create the file. (param: `database`)
- Through the SQLite connection, SQL tables are created for the user-provided data files. A file of target URLs is necessary, whose data will be parsed and inserted into the 'links' SQL table. (param: `links_file`, `url_col`, `shared_content_file`)
- The class instance remembers whether to (a) deploy all of the `minall` enrichment workflow or (b) only collect the generalized Buzzsumo metadata. (param: `buzzsumo_only`)

---

::: minall.main
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2
