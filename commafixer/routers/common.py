from fastapi import HTTPException
from logging import Logger

from comma_fixer_interface import CommaFixerInterface


def fix_commas_request_handler(
        json_field_name: str,
        data: dict[str, str],
        logger: Logger,
        model: CommaFixerInterface
) -> dict[str, str]:
    if json_field_name in data:
        logger.debug('Fixing commas.')
        return {json_field_name: model.fix_commas(data['s'])}
    else:
        msg = f"Text '{json_field_name}' missing"
        logger.debug(msg)
        raise HTTPException(status_code=400, detail=msg)
