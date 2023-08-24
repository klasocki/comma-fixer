from fastapi import APIRouter, HTTPException
import logging

from commafixer.src.fixer import CommaFixer


logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

logger.info('Loading the main comma fixer model...')
router.model = CommaFixer()


@router.post('/')
async def fix_commas(data: dict):
    json_field_name = 's'
    if json_field_name in data:
        logger.debug('Fixing commas.')
        return {json_field_name: router.model.fix_commas(data['s'])}
    else:
        msg = f"Text '{json_field_name}' missing"
        logger.debug(msg)
        raise HTTPException(status_code=400, detail=msg)
