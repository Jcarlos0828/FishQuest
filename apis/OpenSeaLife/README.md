# OpenSeaLife API

## Definition

OpenSeaLife is the centralized access API for **FishBase** and **SeaLifeBase**, the two most comprehensive taxonomic and ecological reference databases for aquatic species worldwide.

## Problem It Solves

FishBase (`fishbase.se`) and SeaLifeBase (`sealifebase.org`) do not expose structured HTTP query endpoints. There is also no official guide pointing to their dataset on HuggingFace. OpenSeaLife acts as the entry point: it discovers the dataset structure, exposes its tables with column schemas, and centralizes data access for other APIs and consumers within the FishQuest ecosystem.

## Data Source

Data is fetched from the public dataset [`cboettig/fishbase`](https://huggingface.co/datasets/cboettig/fishbase) on HuggingFace, which contains the full database in Parquet format, organized by server and version:

| Server | Available tables | Current version |
|---|---|---|
| `fishbase` | 216 tables | `v25.04` |
| `sealifebase` | 199 tables | `v25.04` |

Historical versions available: `v19.04`, `v21.06`, `v23.01`, `v23.05`, `v24.07`, `v25.04`.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Checks connectivity and returns the species count for the selected server |
| `GET` | `/tables` | Lists all available tables with their column schemas |

## Port

`8006`

## Running

```bash
make run
# Server at http://localhost:8006
# Swagger UI at http://localhost:8006/docs
```
