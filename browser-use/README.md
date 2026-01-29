Browser Use
===========

- Setup

```
$ uv venv --python 3.11
Using CPython 3.11.5 interpreter at: /usr/local/anaconda3/bin/python3.11
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

$ source .venv/bin/activate

$ uv pip install browser-use

$ uv pip install playwright

$ uv run playwright install chromium
Downloading Chromium 143.0.7499.4 (playwright build v1200) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1200/chromium-mac-arm64.zip
(node:38756) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
(Use `node --trace-deprecation ...` to show where the warning was created)
159.6 MiB [====================] 100% 0.0s
Chromium 143.0.7499.4 (playwright build v1200) downloaded to /Users/terrence/Library/Caches/ms-playwright/chromium-1200
Downloading Chromium Headless Shell 143.0.7499.4 (playwright build v1200) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1200/chromium-headless-shell-mac-arm64.zip
(node:38818) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
(Use `node --trace-deprecation ...` to show where the warning was created)
89.7 MiB [====================] 100% 0.0s
Chromium Headless Shell 143.0.7499.4 (playwright build v1200) downloaded to /Users/terrence/Library/Caches/ms-playwright/chromium_headless_shell-1200

$ uv pip install -r requirements.txt
```

- Run

```
$ python agent.py
```

- What you want a LLM Agent to do

![Browser Use - Code](Browser%20Use%20-%20Code.png)

- What LLM Agent `Browser Use` can do

![Browser Use - Sign in](Browser%20Use%20-%20Sign%20in.png)

![Browser Use - Send notification](Browser%20Use%20-%20Send%20notification.png)

![Browser Use - Authentication](Browser%20Use%20-%20Authentication.png)

![Browser Use - Stay signed in](Browser%20Use%20-%20Stay%20signed%20in.png)

- Cross Origin Error

![Browser Use - Cross Origin Error](Browser%20Use%20-%20Cross%20Origin%20Error.png)

To work around this, you can:

1. use standalone browser like `Chromium` or `Google Chrome`
2. login with `Google` or `Microsoft` account
3. export all cookies, JSON format, with `Cookie-Editor` _https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm_ extension
4. replace **"sameSite": null** and **"sameSite": "no_restriction"** with **"sameSite": "None"**; **"sameSite": "lax"** with **"sameSite": "Lax"**; **"sameSite": "strict"** with **"sameSite": "Strict"**
5. bind **cookies.json** file in the browser in **agent.py**

![Browser Use - Cookie-Editor](Browser%20Use%20-%20Cookie-Editor.png)

or, you can:

- use standalone browser like `Chromium` or `Google Chrome` in **agent.py**

![Browser Use - Login Workaround](Browser%20Use%20-%20Login%20Workaround%201.png)

![Browser Use - Login Workaround](Browser%20Use%20-%20Login%20Workaround%202.png)

References
----------

- Browser Use Documentation, _https://docs.browser-use.com/_
- Enable AI to control your browser, _https://github.com/browser-use/browser-use_
