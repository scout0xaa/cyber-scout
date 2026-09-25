import httpx
from services.security import get_security_info

async def get_http_info(link):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        if not link.startswith("https://") and not link.startswith("http://"):
            link = f'https://{link}'

        https = link.startswith("https://")

        response = await client.get(link)

        hsts, csp, x_frame_options = get_security_info(response)

        if len(response.history) != 0:
            for redirect in response.history:
                status_code_redirect = redirect.status_code
                location_redirect = redirect.headers.get("Location", "No redirect")
        else:
            status_code_redirect = ""
            location_redirect = 'No redirect'

        if response.status_code == 200:
            status = "OK"
        elif response.status_code == 301:
            status = "Moved Permanently"
        elif response.status_code == 302:
            status = "Found"
        elif response.status_code == 403:
            status = "Forbidden"
        elif response.status_code == 404:
            status = "Not Found"
        elif response.status_code == 500:
            status = "Internal Server Error"
        else:
            status = "Unknown"


        if "Server" in response.headers:
            server = response.headers["Server"]
        else:
            server = 'No server'

        return [
            https,
            response.status_code,
            status,
            server,
            status_code_redirect,
            location_redirect,
            hsts,
            csp,
            x_frame_options
            ]
