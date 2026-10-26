import asyncio
import logging

from app.services.auction import finalize_due_auctions


logger = logging.getLogger(__name__)


async def run_auction_finalizer(interval_seconds: int = 30) -> None:
    while True:
        try:
            closed_count = await finalize_due_auctions()
            if closed_count:
                logger.info("Finalized %s expired auction(s).", closed_count)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Auction finalization cycle failed; it will be retried.")

        await asyncio.sleep(interval_seconds)