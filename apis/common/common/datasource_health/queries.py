import duckdb


def _query_species_count(url: str) -> int:
    con = duckdb.connect()
    result = con.execute(f"SELECT COUNT(*) FROM read_parquet('{url}')").fetchone()
    con.close()
    if result is None:
        return 0
    return int(result[0])
