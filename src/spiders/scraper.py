import requests
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import random

from db.queries import add_to_wwr, add_to_remoteok, add_to_remote_co


JOB_LISTINGS_WE_WORK_REMOTELY = []
JOB_LISTINGS_REMOTE_OK = []
JOB_LISTINGS_REMOTE_CO = []

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
REMOTE_OK_API_URL = "https://remoteok.com/api"

"""
CLOUDFLARE SUCKS
"""
# async def scrape_indeed(page, p, browser, timeout=3000):
#     job_position = 'python developer'
#     job_location = 'remote'
#     date_posted = 20
#     url = construct_indeed_url(job_position, job_location, date_posted)
#     try:
#         print('INSIDE TRY URL IS', url, page)
#         await page.goto(url,  wait_until="load")
#         await page.screenshot(path='/home/bishwas/pdebug.png', full_page=True)
#         # await page.wait_for_selector('.cardOutline')
#         job_container = page.locator('.cardOutline')
#         print('JOB CONTAINERS', job_container)
#         for i in await job_container.element_handles():
#             print(i)
#
#     except Exception as e:
#         print('EXCEPTION OCCURED WHILE SCRAPING INDEED, EXCEPTION: ', e)
#
#     finally:
#         await browser.close()
#         await p.stop()
#
#
# def construct_indeed_url(job_position, job_location, date_posted):
#     return f'https://www.indeed.com/jobs?q={"+".join(job_position.split())}&l={job_location}&fromage={date_posted}'


def get_remoteok_jobs(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        for data in json_data:
            job_description = {
                "company": data.get("company", ""),
                "position": data.get("position", ""),
                "tags": data.get("tags", []),
                "location": data.get("location", ""),
                "salary_min": data.get("salary_min", 0),
                "salary_max": data.get("salary_max", 0),
            }
            JOB_LISTINGS_REMOTE_OK.append(job_description)
        return JOB_LISTINGS_REMOTE_OK[1:]

    else:
        print("ERROR WHILE FETCHING")


async def scrape_working_nomads(page, p, browser):
    await page.goto(
        "https://www.workingnomads.com/jobs",
        wait_until="domcontentloaded",
        timeout=60000,
    )
    await asyncio.sleep(2)
    await page.mouse.wheel(0, random.randint(200, 600))
    await asyncio.sleep(random.uniform(5, 6))
    await page.mouse.wheel(0, 1000)
    await page.screenshot(path="/home/bishwas/nomads.png", full_page=True)
    await page.wait_for_selector("#job-list")
    lists = await page.locator("#job-list")
    job_wrapper = lists.locator(".job-wrapper")
    print(await job_wrapper.count())


async def scrape_remote_ok(page, p, browser):
    await page.goto("https://remoteok.com/remote-dev-jobs/", wait_until="load")
    await asyncio.sleep(2)
    await page.mouse.wheel(0, random.randint(200, 600))
    await asyncio.sleep(random.uniform(5, 6))
    await page.mouse.wheel(0, 1000)
    await page.wait_for_selector("#jobsboard")
    rows = page.locator("#jobsboard tbody tr[data-id]")
    print("HERE", await rows.count())

    for i in range(await rows.count()):
        try:
            row = rows.nth(i)
            title = await row.locator("a h2").inner_text()
            subtitle = await row.locator(
                ".company.position.company_and_position span h3"
            ).inner_text()
            divs = row.locator(".description div")
            DESCRIPTIONS = []
            for j in range(await divs.count()):
                info = await divs.nth(j).inner_text()
                DESCRIPTIONS.append(info)

            job_description = {
                "title": title.strip(),
                "subtitle": subtitle.strip(),
                "descriptions": DESCRIPTIONS,
            }
            JOB_LISTINGS_REMOTE_OK.append(job_description)
            print(job_description)
        except Exception as e:
            print("EXCEPTION OCCURED GRACEFULLY BREAKING", e)
            break

    print(JOB_LISTINGS_REMOTE_OK)
    await browser.close()


async def scrape_wwr(page, timeout=3000):
    await page.goto("https://weworkremotely.com", wait_until="load")
    await asyncio.sleep(random.uniform(2, 5))
    await page.mouse.wheel(0, random.randint(200, 600))
    await asyncio.sleep(random.uniform(1, 2))
    await page.wait_for_selector("#job_list")
    container = page.locator("#job_list")
    job_lists = container.locator("ul")
    lists = job_lists.locator("li")
    count = await lists.count()
    for i in range(count):
        try:
            job = lists.nth(i)
            title = await job.locator(".new-listing__header").inner_text()
            company = await job.locator(".new-listing__company-name").inner_text()
            job = lists.nth(i)
            description_container = job.locator(".new-listing__categories")
            description_lists = description_container.locator("p")
            description_count = await description_lists.count()
            DESCRIPTIONS = []
            for j in range(description_count):
                des = await description_lists.nth(j).inner_text()
                DESCRIPTIONS.append(des)

            job_information = {
                "DESCRIPTION": DESCRIPTIONS,
                "title": title,
                "company": company,
            }
            JOB_LISTINGS_WE_WORK_REMOTELY.append(job_information)

        except Exception as e:
            print("EXCEPTION", e)
            print("TIMEOUT OCCURED GRACEFULLY BREAKING")
            break
    print("FINISHED SCRAPING WWR, DETAILS : ", JOB_LISTINGS_WE_WORK_REMOTELY)
    print("TOTAL JOBS SCRAPPED FROM WWR", len(JOB_LISTINGS_WE_WORK_REMOTELY))
    # add_to_wwr(JOB_LISTINGS_WE_WORK_REMOTELY)
    return JOB_LISTINGS_WE_WORK_REMOTELY


async def scrape_remote_co(page, p, browser):
    await page.goto("https://remote.co/remote-jobs/developer", wait_until="load")
    await asyncio.sleep(random.uniform(2, 5))
    await page.mouse.wheel(0, random.randint(200, 600))
    await asyncio.sleep(random.uniform(1, 2))
    await page.wait_for_selector("#job-table-wrapper")
    job_cards = page.locator("#job-table-wrapper > div > div")
    for i in range(await job_cards.count()):
        job = job_cards.nth(i)
        title_el = job.locator("a")
        company_el = job.locator("h3")
        title = await title_el.inner_text() if await title_el.count() > 0 else "-"
        company = await company_el.inner_text() if await company_el.count() > 0 else "-"
        TAGS = []
        apply_link = await title_el.get_attribute("href")
        tags = job.locator("ul > li")
        for j in range(await tags.count()):
            tag = await tags.nth(j).inner_text()
            TAGS.append(tag)
        job_information = {
            "tags": TAGS,
            "role": title,
            "company": company,
            "apply_link": f"https://remote.co{apply_link}",
        }
        JOB_LISTINGS_REMOTE_CO.append(job_information)
    print("JOB LISTINGS FOR REMOTE.CO: ", JOB_LISTINGS_REMOTE_CO)
    print("TOTAL JOBS SCRAPED: ", len(JOB_LISTINGS_REMOTE_CO))
    add_to_remote_co(JOB_LISTINGS_REMOTE_CO)


async def main():
    """starts a background playwright engine which returns an object"""
    p = await async_playwright().start()
    try:
        """launch chromium firefox or safari, blink feature is a feature used by chrome to detect bot so we disable that in our engine"""
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
        )
        page = await context.new_page()
        await stealth_async(page)
        await asyncio.sleep(random.uniform(1, 3))
        # results = asyncio.gather(scrape_wwr(page))
        # await scrape_indeed(page, p, browser)
        # await scrape_remote_ok(page, p, browser)
        # job_listings = get_remoteok_jobs(REMOTE_OK_API_URL)
        # add_to_remoteok(job_listings)
        # await scrape_working_nomads(page, p, browser)
        await scrape_remote_co(page, p, browser)

    except Exception as e:
        print("EXCEPTION OCCURED IN MAIN, EXCEPTION: ", e)


asyncio.run(main())
