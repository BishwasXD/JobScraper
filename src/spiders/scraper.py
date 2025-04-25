import asyncio
from playwright.async_api import async_playwright
import random


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

JOB_LISTINGS_WE_WORK_REMOTELY = []


async def main():
    """starts a background playwright engine which returns an object """
    p = await async_playwright().start()
    try:
        """launch chromium firefox or safari, blink feature is a feature used by chrome to detect bot so we disable that in our engine"""
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920,
                      "height": 1080
                      },
            locale="en-US"
        )
        page = await context.new_page()
        await asyncio.sleep(random.uniform(1, 3))
        await page.goto("https://weworkremotely.com", wait_until="load")
        await asyncio.sleep(random.uniform(2, 5))
        await page.mouse.wheel(0, random.randint(200, 600))
        await asyncio.sleep(random.uniform(1, 2))
        await page.wait_for_selector('#job_list')
        container = page.locator('#job_list')
        job_lists = container.locator('ul')
        lists = job_lists.locator('li')
        count = await lists.count()
        for i in range(count):
            try:
                job = lists.nth(i)
                title = await job.locator('.new-listing__header').inner_text()
                company = await job.locator('.new-listing__company-name').inner_text()
                job = lists.nth(i)
                description_container = job.locator('.new-listing__categories')
                description_lists = description_container.locator('p')
                description_count = await description_lists.count()
                DESCRIPTIONS = []
                for j in range(description_count):
                    des = await description_lists.nth(j).inner_text()
                    DESCRIPTIONS.append(des)

                job_information = {
                    'DESCRIPTION': DESCRIPTIONS,
                    'title': title,
                    'company': company
                }
                JOB_LISTINGS_WE_WORK_REMOTELY.append(job_information)

            except Exception as e:
                print('EXCEPTION', e)
                print('TIMEOUT OCCURED GRACEFULLY BREAKING')
                break
        print('FINISHED SCRAPING, DETAILS : ', JOB_LISTINGS_WE_WORK_REMOTELY)

    finally:
        await browser.close()
        await p.stop()

asyncio.run(main())
