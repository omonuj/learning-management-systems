# Contributing

Thanks for your interest in improving the Learning Management System.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
make install
cp .env.example .env   # then edit values
make migrate
make run
```

## Workflow

1. Create a feature branch off `main`.
2. Make your change with tests where it makes sense.
3. Run the checks locally before pushing:

   ```bash
   make lint
   make check
   make test
   ```

4. Open a pull request. CI (lint, Django checks, migrations, tests) must be
   green before merge.

## Commit style

Keep commits focused and write a short imperative subject line
(e.g. "Add cart total serializer").
