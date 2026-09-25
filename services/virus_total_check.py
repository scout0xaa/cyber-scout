import httpx

from config import VIRUSTOTAL_API_KEY

async def check_virustotal(domain: str) -> dict:
    if not VIRUSTOTAL_API_KEY:
        return {
            "status": "unavailable",
            "message": "VirusTotal API key is missing",
        }

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.HTTPError:
        return {
            "status": "unavailable",
            "message": "VirusTotal is unavailable",
        }

    if response.status_code == 404:
        return {
            "status": "unknown",
            "message": "Domain was not found",
        }

    if response.status_code == 429:
        return {
            "status": "unavailable",
            "message": "VirusTotal rate limit exceeded",
        }

    response.raise_for_status()

    stats = response.json()["data"]["attributes"]["last_analysis_stats"]


    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    harmless = stats.get("harmless", 0)

    detections = malicious + suspicious
    total = sum(stats.values())

    if malicious > 3:
        reputation = "dangerous"
    elif malicious > 0 or suspicious > 0:
        reputation = "suspicious"
    else:
        reputation = "clean"

    return {
        "status": reputation,
        "malicious": malicious,
        "suspicious": suspicious,
        "harmless": harmless,
        "detections": detections,
        "total": total,
    }
