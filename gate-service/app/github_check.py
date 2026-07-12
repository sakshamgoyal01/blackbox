import httpx

from app.config import settings


def main():
    token = settings.GITHUB_TOKEN

    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is not set in your .env file."
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = httpx.get(
        "https://api.github.com/user",
        headers=headers,
        timeout=30,
    )

    print(f"HTTP Status: {response.status_code}")

    if response.status_code != 200:
        print(response.text)
        return

    user = response.json()

    print("\n✅ GitHub Authentication Successful\n")

    print(f"Login      : {user['login']}")
    print(f"Name       : {user.get('name')}")
    print(f"ID         : {user['id']}")
    print(f"Profile    : {user['html_url']}")


if __name__ == "__main__":
    main()