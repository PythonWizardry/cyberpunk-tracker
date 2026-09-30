from bs4 import BeautifulSoup
from curl_cffi import requests
from curl_cffi.requests import AsyncSession
import asyncio
from backend.db.models import QuestType

WIKI_BASE = "https://cyberpunk.fandom.com"
BASE_URL = f"{WIKI_BASE}/wiki/Cyberpunk_2077_"

MAIN_QUESTS_URL = f"{BASE_URL}Main_Jobs"
SIDE_QUESTS_URL = f"{BASE_URL}Side_Jobs"
GIGS_URL = f"{BASE_URL}Gigs"


def parse_quests(html: str, quest_type: QuestType) -> list[dict]:

    soup = BeautifulSoup(html, "lxml")
    quests = []

    for table in soup.find_all("table", class_="table-progress-tracking"):
        for row in table.select("tbody tr"):
            tds = row.find_all("td")
            if len(tds) < 2:
                continue  # skip header rows (they use <th>, not <td>)

            title_td = tds[1]
            a = title_td.find("a")
            if not a:
                continue

            quests.append({
                "name": a.get_text(strip=True),
                "quest_type": quest_type,
                "wiki_url": WIKI_BASE + a["href"]
            })

    return quests


async def fetch(session: AsyncSession, url: str, quest_type: QuestType):
    resp = await session.get(url, impersonate="chrome124")
    resp.raise_for_status()
    return parse_quests(resp.text, quest_type)


async def scrape_all_quests() -> list[dict]:
    async with AsyncSession(impersonate="chrome124") as session:
        main_quests, side_quests, gigs = await asyncio.gather(
            fetch(session, MAIN_QUESTS_URL, QuestType.main),
            fetch(session, SIDE_QUESTS_URL, QuestType.side),
            fetch(session, GIGS_URL, QuestType.gig),
        )
    return main_quests + side_quests + gigs


if __name__ == "__main__":
    quests = asyncio.run(scrape_all_quests())
    for q in quests:
        print(q)
    print(len(quests))


# def testing_scrapper():
#     resp = requests.get(MAIN_QUESTS_URL, impersonate="chrome124")
#     resp.raise_for_status()
#     print(f"Status: {resp.status_code} | Size: {len(resp.text)} bytes")

#     quests = parse_quests(resp.text, QuestType.main)
#     print(f"Found {len(quests)} quests:")
#     for q in quests:
#         print(f"  {q['name']}  ->  {q['wiki_url']}")


# testing_scrapper()
