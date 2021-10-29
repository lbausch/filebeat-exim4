[![Tests](https://github.com/lbausch/filebeat-exim4/actions/workflows/main.yml/badge.svg)](https://github.com/lbausch/filebeat-exim4/actions/workflows/main.yml)

# filebeat-exim4 <!-- omit in toc -->
Fully tested Filebeat module to ingest Exim 4 logs

- [Installation](#installation)
- [Configuration](#configuration)
- [Further Reading](#further-reading)

## Installation
+ Copy `module/exim4` to `/usr/share/filebeat/module/`
+ Copy `modules.d/exim4.yml.disabled` to `/etc/filebeat/modules.d/exim4.yml`

## Configuration
All configuration is done in `/etc/filebeat/modules.d/exim4.yml`.

By default both main and reject logs are ingested. This behaviour can be changed by setting the corresponding `enabled` flag to `true` or `false` respectively:

```yaml
- module: exim4
  main:
    enabled: true

  reject:
    enabled: false
```

The module expects the main log in `/var/log/exim/main.log` and the reject log in `/var/log/exim/reject.log`. It's possible to use custom paths for the logs by specifying `var.paths`:

```yaml
- module: exim4
  main:
    enabled: true

    var.paths:
      - /var/log/exim_mainlog

  reject:
    enabled: true

    var.paths:
      - /var/log/exim_rejectlog
```

## Further Reading
+ https://www.exim.org/exim-pdf-current/doc/spec.pdf
