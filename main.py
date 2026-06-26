import logging
from dotenv import load_dotenv
from src.ingestion import run_ingestion
from src.processing import run_processing
from src.delivery import send_newsletter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    load_dotenv()

    log.info("Step 1/3: Fetching trending repos and downloading READMEs...")
    try:
        repos = run_ingestion()
    except Exception as e:
        log.error(f"Ingestion failed: {e}", exc_info=True)
        raise
    log.info(f"  → {len(repos)} repos ingested.")

    log.info("Step 2/3: Running LLM map-reduce pipeline...")
    try:
        html_report = run_processing(repos)
    except Exception as e:
        log.error(f"Processing failed: {e}", exc_info=True)
        raise
    log.info("  → Report generated.")

    log.info("Step 3/3: Sending newsletter...")
    try:
        result = send_newsletter(html_report)
    except Exception as e:
        log.error(f"Email delivery failed: {e}", exc_info=True)
        raise
    log.info(f"  → Email sent. Result: {result}")


if __name__ == "__main__":
    main()
