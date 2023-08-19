from fastapi import APIRouter, HTTPException
import logging

from src.baseline import BaselineCommaFixer


logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

logger.info('Loading the baseline model...')
router.model = BaselineCommaFixer()


@router.post('/fix-commas/')
async def fix_commas_with_baseline(data: dict):
    json_field_name = 's'
    if json_field_name in data:
        logger.debug('Fixing commas.')
        return {json_field_name: router.model.fix_commas(data['s'])}
    else:
        msg = f"Text '{json_field_name}' missing"
        logger.debug(msg)
        raise HTTPException(status_code=400, detail=msg)
