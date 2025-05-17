# generate_screenshots.py
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Folders
html_root = Path(".")
tiers = ["tier1", "tier2", "tier3", "tier4"]
screenshot_root = Path("screenshots")

def take_screenshot(context, html_file: Path, output_path: Path):
    file_url = f"file://{html_file.resolve()}"
    page = context.new_page()
    page.goto(file_url)

    # Wait for network and dynamic content
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    page.screenshot(path=str(output_path), full_page=True)
    print(f"✅ Screenshot saved: {output_path}")
    page.close()

def main():
    single_file = Path(sys.argv[1]) if len(sys.argv) > 1 else None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        context = browser.new_context()

        if single_file:
            if not single_file.exists() or not single_file.suffix == ".html":
                print(f"❌ File not found or not an HTML file: {single_file}")
                sys.exit(1)

            # Determine tier based on parent folder name
            tier_name = single_file.parent.name
            output_dir = screenshot_root / tier_name
            output_dir.mkdir(parents=True, exist_ok=True)

            output_path = output_dir / f"{single_file.stem}.png"
            take_screenshot(context, single_file, output_path)

        else:
            for tier in tiers:
                tier_path = html_root / tier
                output_dir = screenshot_root / tier
                output_dir.mkdir(parents=True, exist_ok=True)

                for html_file in tier_path.glob("*.html"):
                    output_path = output_dir / f"{html_file.stem}.png"
                    take_screenshot(context, html_file, output_path)

        browser.close()

if __name__ == "__main__":
    main()
