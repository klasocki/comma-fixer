from fastapi import APIRouter, HTTPException
import logging

from commafixer.src.fixer import CommaFixer
from commafixer.routers.common import fix_commas_request_handler


logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

logger.info('Loading the main comma fixer model...')
router.model = CommaFixer()


@router.post('/')
async def fix_commas(data: dict):
    json_field_name = 's'
    return fix_commas_request_handler(json_field_name, data, logger, router.model)
