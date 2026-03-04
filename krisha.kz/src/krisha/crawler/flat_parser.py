import json
import logging
from typing import Any

from bs4 import BeautifulSoup

import krisha.common.msg as msg
from krisha.entities.flat import Flat

logger = logging.getLogger()


class FlatParser:
    """Pars content data and create Flat object."""

    @staticmethod
    def _get_pars_data(content: BeautifulSoup) -> dict:
        script = content.find("script", id="jsdata")
        if not script:
            raise ValueError(msg.CR_SOUP_FIND_ERROR.format("jsdata"))
        string = script.text.strip()
        start_index = string.find("{")
        end_index = string.rfind("}")
        if start_index == -1 or end_index == -1:
            raise ValueError(msg.CR_JS_PARS_ERROR)
        json_string = string[start_index : end_index + 1]
        try:
            data = json.loads(json_string)
            return data
        except Exception as error:
            raise ValueError(msg.CR_JSON_ERROR.format(error)) from error

    @staticmethod
    def _get_advert(pars_data: dict, key: str) -> dict:
        advert = pars_data.get(key)
        if not isinstance(advert, dict) or not advert:
            raise ValueError(msg.CR_KEY_DATA_ERROR.format(key))
        return advert

    @staticmethod
    def _get_adverts(pars_data: dict, key: str) -> dict:
        adverts = pars_data.get(key)
        if (
            not isinstance(adverts, list)
            or not adverts
            or not isinstance(adverts[0], dict)
            or not adverts[0]
        ):
            raise ValueError(msg.CR_KEY_DATA_ERROR.format(key))
        return adverts[0]

    @staticmethod
    def _get_sub_data(data: Any, key: str, required=False) -> Any:
        sub_data = data.get(key)
        if not sub_data:
            if required:
                raise ValueError(msg.CR_KEY_GET_ERROR.format(key))
            logger.warning(msg.CR_KEY_GET_ERROR.format(key))
        return sub_data

    @classmethod
    def get_flat(cls, content: BeautifulSoup, url: str) -> Flat:
        pars_data = cls._get_pars_data(content)
        advert = cls._get_advert(pars_data, "advert")
        adverts = cls._get_adverts(pars_data, "adverts")
        address = cls._get_sub_data(adverts, "fullAddress")
        photos = cls._get_sub_data(advert, "photos")
        lat_lon = cls._get_sub_data(advert, "lat_lon")

        dt_specs = {
            dt.get("data-name").split(".")[-1]: dt.find_next_sibling("dd").get_text(strip=True)
            for dt in content.find_all("dt", attrs={"data-name": True})
            if dt.find_next_sibling("dd")
        }

        info_specs = {
            div.get("data-name").split(".")[-1]: div.find("div", class_="offer__advert-short-info").get_text(strip=True)
            for div in content.find_all("div", class_="offer__info-item", attrs={"data-name": True})
            if div.find("div", class_="offer__advert-short-info")
        }

        specs = {**info_specs, **dt_specs}  # dt_specs wins on key conflicts

        flat_data = {
            "id": advert.get("id"),
            "room": advert.get("rooms"),
            "square": advert.get("square"),
            "city": address.split(",")[0] if address else None,
            "photo": photos[0].get("src") if photos else None,
            "url": url,
            "price": advert.get("price"),
            "lat": cls._get_sub_data(lat_lon, "lat") if lat_lon else None,
            "lon": cls._get_sub_data(lat_lon, "lon") if lat_lon else None,
            **specs,
        }

        return Flat(**flat_data)