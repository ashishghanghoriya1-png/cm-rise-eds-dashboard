import asyncio
import os
from playwright.async_api import async_playwright

async def capture_all_powerbi_pages_via_keyboard():
    url = "https://app.powerbi.com/view?r=eyJrIjoiYWMyNTNmMDctNjIyMC00OWNhLTk0YjktZjM4NDc2MTdjZTA5IiwidCI6ImRmM2Q4Y2MyLTI2YmEtNDBlZC04NDBmLTliZGY0ODgxMTQzYiJ9"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1600, "height": 1000})
        page = await context.new_page()
        
        print("Navigating to Power BI Report URL...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(10)
        
        artifact_dir = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa"
        
        # Click on report area to focus
        await page.click("body")
        
        # Press PageUp 5 times to go to Page 1
        for _ in range(5):
            await page.keyboard.press("PageUp")
            await asyncio.sleep(2)
            
        for page_num in range(1, 5):
            print(f"\n--- Page {page_num} ---")
            img_name = f"powerbi_page_{page_num}.png"
            img_path = os.path.join(artifact_dir, img_name)
            await page.screenshot(path=img_path, full_page=True)
            
            body_text = await page.evaluate("document.body.innerText")
            print(f"Extracted snippet for Page {page_num}:")
            print(body_text[:1000])
            
            # Press PageDown to go to next page
            await page.keyboard.press("PageDown")
            await asyncio.sleep(4)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_all_powerbi_pages_via_keyboard())
