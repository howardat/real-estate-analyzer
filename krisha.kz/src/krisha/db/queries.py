import json
import logging

import krisha.common.msg as msg
from krisha.crawler.flat_parser import Flat
from krisha.db.base import DBConnection

logger = logging.getLogger()

_FIXED_KEYS = {"id", "room", "square", "city", "photo", "url", "price"}


def insert_flats_data_db(
    connector: DBConnection,
    flats_data: list[Flat],
) -> None:
    """Insert flats data to DB."""
    insert_flats_query = """
        INSERT OR IGNORE
        INTO flats(id, url, room, square, city, photo, specs)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    insert_price_query = """
        INSERT OR IGNORE
        INTO prices(flat_id, price)
        VALUES (?, ?);
        """

    flats_rows = []
    prices_rows = []
    for flat in flats_data:
        data = vars(flat)
        specs = {k: v for k, v in data.items() if k not in _FIXED_KEYS}
        flats_rows.append(
            (
                data.get("id"),
                data.get("url"),
                data.get("room"),
                data.get("square"),
                data.get("city"),
                data.get("photo"),
                json.dumps(specs, ensure_ascii=False) if specs else None,
            )
        )
        prices_rows.append((data.get("id"), data.get("price")))

    with connector as con:
        con.executemany(insert_flats_query, flats_rows)
        con.executemany(insert_price_query, prices_rows)
        con.commit()
        logger.info(msg.DB_INSERT_OK)
