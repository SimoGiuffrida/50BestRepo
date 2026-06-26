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
    repos = run_ingestion()
    log.info(f"  → {len(repos)} repos ingested.")

    log.info("Step 2/3: Running LLM map-reduce pipeline...")
    html_report = run_processing(repos)
    log.info("  → Report generated.")

    log.info("Step 3/3: Sending newsletter...")
    result = send_newsletter(html_report)
    log.info(f"  → Email sent. Result: {result}")


if __name__ == "__main__":
    main()
