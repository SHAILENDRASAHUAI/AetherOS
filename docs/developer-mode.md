# Developer Mode

## SDK Surface

- API contract seed: `sdk/api/openapi.yaml`
- Plugin manifest schema: `sdk/plugins/plugin-manifest.schema.json`
- Extension track: `sdk/extensions/`

## Local Validation

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Build Pipeline

```bash
./scripts/build.sh
```
