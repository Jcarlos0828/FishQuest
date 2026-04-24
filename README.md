# FishQuest

Monorepo of APIs for accessing and tracking aquatic species data.

## Architecture

```mermaid
graph TD
    FQ["FishQuest\nMonorepo"]

    OSL["OpenSeaLife\n:8006\nAccess to FishBase / SeaLifeBase"]
    FT["FishTrack\n:8005\nSpecies checklist by aquarium"]

    COM_BASE["common/base\nBaseApiModel · BaseService"]
    COM_HEALTH["common/health\nschemas · queries"]
    COM_CATALOG["common/catalog\nschemas · queries"]

    HF["HuggingFace\ndatasets/cboettig/fishbase\n216 FishBase tables · 199 SeaLifeBase tables"]

    FQ --> OSL
    FQ --> FT

    OSL --> COM_BASE
    OSL --> COM_HEALTH
    OSL --> COM_CATALOG

    FT --> COM_BASE

    COM_HEALTH --> COM_BASE
    COM_CATALOG --> COM_BASE

    OSL --> HF
```

## APIs

| API | Port | Description |
|---|---|---|
| [OpenSeaLife](apis/OpenSeaLife/README.md) | `8006` | Centralizes access to FishBase and SeaLifeBase via HuggingFace |
| [FishTrack](apis/FishTrack/README.md) | `8005` | Species checklist by aquarium |

## Structure

```
FishQuest/
├── apis/
│   ├── common/          # Shared schemas and queries across APIs
│   │   ├── base/        # BaseApiModel and BaseService
│   │   ├── health/      # Domain: health checks
│   │   └── catalog/     # Domain: table discovery
│   ├── OpenSeaLife/     # FishBase/SeaLifeBase access API
│   └── FishTrack/       # Species checklist API
└── docs/                # User story documentation
```

## Commands (monorepo)

```bash
make run-opensealife   # Start OpenSeaLife on :8006
make run-fishtrack     # Start FishTrack on :8005
make install           # Install dependencies for both APIs
make lint              # ruff check across the monorepo
make format            # ruff format across the monorepo
make typecheck         # mypy across the monorepo
```
