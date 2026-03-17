import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from playwright.async_api import async_playwright
from datetime import date
import pandas as pd

TARGET_SITES = [
    {'site': 'booking_com',  'url': 'https://www.booking.com',          'sector': 'travel'},
    {'site': 'expedia',      'url': 'https://www.expedia.com/Hotels',    'sector': 'travel'},
    {'site': 'makemytrip',   'url': 'https://www.makemytrip.com',        'sector': 'travel'},
    {'site': 'cleartrip',    'url': 'https://www.cleartrip.com',         'sector': 'travel'},
    {'site': 'amazon',       'url': 'https://www.amazon.in/s?k=laptop',  'sector': 'retail'},
    {'site': 'flipkart',     'url': 'https://www.flipkart.com/laptops',  'sector': 'retail'},
    {'site': 'myntra',       'url': 'https://www.myntra.com',            'sector': 'retail'},
    {'site': 'ajio',         'url': 'https://www.ajio.com',              'sector': 'retail'},
    {'site': 'nykaa',        'url': 'https://www.nykaa.com',             'sector': 'retail'},
    {'site': 'meesho',       'url': 'https://www.meesho.com',            'sector': 'retail'},
    {'site': 'bigbasket',    'url': 'https://www.bigbasket.com',         'sector': 'retail'},
    {'site': 'netflix',      'url': 'https://www.netflix.com/in',        'sector': 'saas'},
    {'site': 'hotstar',      'url': 'https://www.hotstar.com',           'sector': 'saas'},
    {'site': 'swiggy',       'url': 'https://www.swiggy.com',            'sector': 'food'},
    {'site': 'zomato',       'url': 'https://www.zomato.com',            'sector': 'food'},
]

async def extract_ui_text(page):
    try:
        items = await page.evaluate("""
            () => {
                const selectors = [
                    'button', '[role="button"]', 'input[type="submit"]',
                    'a[href]', 'label', '[class*="decline"]',
                    '[class*="cookie"] button', '[class*="banner"] button',
                    '[class*="urgency"]', '[class*="scarcity"]', '[class*="timer"]'
                ];
                const elements = document.querySelectorAll(selectors.join(','));
                return Array.from(elements)
                    .map(el => (el.innerText || el.value || '').trim())
                    .filter(t => t.length > 2 && t.length < 200);
            }
        """)
        return list(set(items))
    except Exception:
        return []

async def scrape_all():
    records = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for target in TARGET_SITES:
            try:
                page = await browser.new_page()
                await page.set_extra_http_headers({'User-Agent': 'Mozilla/5.0'})
                await page.goto(target['url'], wait_until='domcontentloaded', timeout=25000)
                await page.wait_for_timeout(2000)
                texts = await extract_ui_text(page)
                for txt in texts:
                    records.append({
                        'site':         target['site'],
                        'sector':       target['sector'],
                        'url':          target['url'],
                        'ui_text':      txt,
                        'scraped_date': str(date.today())
                    })
                print(f'[OK] {target["site"]:15} — {len(texts)} UI texts')
                await page.close()
            except Exception as e:
                print(f'[ERR] {target["site"]}: {e}')
        await browser.close()
    return pd.DataFrame(records)

if __name__ == '__main__':
    print('Starting scraper...')
    df = asyncio.run(scrape_all())
    df.to_csv('dark_pattern_scraped.csv', index=False)
    print(f'\nDone. Saved {len(df)} rows to dark_pattern_scraped.csv')