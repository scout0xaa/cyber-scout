import httpx

from config import GOOGLE_SAFE_BROWSING_KEY


async def check_google_safe_browsing(url: str) -> dict:
    if not GOOGLE_SAFE_BROWSING_KEY:
        return {
            "status": "unavailable",
            "message": "Google Safe Browsing API key is missing",
        }

    endpoint = (
        "https://safebrowsing.googleapis.com/v4/threatMatches:find"
        f"?key={GOOGLE_SAFE_BROWSING_KEY}"
    )
    payload = {
        "client": {
            "clientId": "cyber-scout",
            "clientVersion": "1.0",
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
    except httpx.HTTPError:
        return {
            "status": "unavailable",
            "message": "Google Safe Browsing is unavailable",
        }

    matches = response.json().get("matches", [])

    if matches:
        return {
            "status": "dangerous",
            "threats": [match.get("threatType", "UNKNOWN") for match in matches],
        }

    return {
        "status": "clean",
        "threats": [],
    }
