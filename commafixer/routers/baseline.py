from fastapi import APIRouter
import logging

from commafixer.src.baseline import BaselineCommaFixer
from common import fix_commas_request_handler

logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

logger.info('Loading the baseline model...')
router.model = BaselineCommaFixer()


@router.post('/fix-commas/')
async def fix_commas_with_baseline(data: dict):
    json_field_name = 's'
    return fix_commas_request_handler(json_field_name, data, logger, router.model)
