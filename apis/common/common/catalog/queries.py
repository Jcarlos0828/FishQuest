import duckdb


def _describe_table(url: str) -> list[dict[str, str]]:
    try:
        con = duckdb.connect()
        rows = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{url}')").fetchall()
        con.close()
        return [{"name": row[0], "type": row[1]} for row in rows]
    except Exception:
        return []
