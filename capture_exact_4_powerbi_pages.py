import asyncio
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from playwright.async_api import async_playwright

async def capture_all_4_powerbi_tabs_js():
    url = "https://app.powerbi.com/view?r=eyJrIjoiYWMyNTNmMDctNjIyMC00OWNhLTk0YjktZjM4NDc2MTdjZTA5IiwidCI6ImRmM2Q4Y2MyLTI2YmEtNDBlZC04NDBmLTliZGY0ODgxMTQzYiJ9"
    
    tabs_to_click = [
        ("Overview", "powerbi_tab1_overview.png"),
        ("Digital Course", "powerbi_tab2_digital_course.png"),
        ("CLSS", "powerbi_tab3_clss.png"),
        ("Filler", "powerbi_tab4_filler.png"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1600, "height": 1000})
        page = await context.new_page()
        
        print("Navigating to Power BI Report URL...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(10)
        
        artifact_dir = r"C:\Users\Peepul\.gemini\antigravity\brain\f3d36a05-31c4-4ca8-978f-d6e3730b02aa"
        
        for tab_name, img_filename in tabs_to_click:
            print(f"\n==========================================")
            print(f"JS CLICKING POWER BI TAB: '{tab_name}'")
            print(f"==========================================")
            
            clicked = await page.evaluate(f'''(label) => {{
                const btns = Array.from(document.querySelectorAll("button"));
                const target = btns.find(b => b.getAttribute("aria-label") === label || b.innerText.trim() === label);
                if (target) {{
                    target.click();
                    return true;
                }}
                return false;
            }}''', tab_name)
            
            print(f"JS Click status for '{tab_name}': {clicked}")
            await asyncio.sleep(8)
            
            # Take screenshot
            local_path = img_filename
            art_path = os.path.join(artifact_dir, img_filename)
            await page.screenshot(path=local_path, full_page=True)
            await page.screenshot(path=art_path, full_page=True)
            print(f"Saved screenshot: '{art_path}'")
            
            # Extract text
            body_text = await page.evaluate("document.body.innerText")
            print(f"\n--- Extracted Text for '{tab_name}' ---")
            print(body_text[:3000])
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_all_4_powerbi_tabs_js())
