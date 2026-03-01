# Portfolio Hub – GitHub/LinkedIn/LeetCode + AI Resume

This is a **simple, static portfolio app** you can open directly in your browser. It lets you:

- Add your **GitHub, LinkedIn, LeetCode and other links**
- Preview a clean **portfolio card** with your info
- Call an **AI model (OpenAI‑compatible)** using your own API key to generate a tailored resume

No build tools or backend required – everything is plain HTML/CSS/JS.

## Files

- `index.html` – main UI
- `styles.css` – styling (dark, modern layout)
- `app.js` – logic for saving profile and calling the AI API

## How to run

1. Open this folder: `user portfolio`.
2. Double‑click `index.html` (or open it via your browser’s “Open file” option).
3. You should see **Portfolio Hub** in your browser.

> Tip: For best results, serve it via a simple HTTP server (for example `python -m http.server` from this folder) instead of the `file://` URL, but it also works directly as a file.

## Using your profiles

In the **Profile & Links** card:

- Enter your **full name** and **headline**.
- Add:
  - GitHub username (or full URL)
  - LinkedIn URL
  - LeetCode username (or full URL)
  - Any other links (one per line).
- Write a short **bio/summary**.
- Click **Save profile**.

Your data is stored **only in `localStorage` in your browser** (no server, no cookies) and used:

- To render the **portfolio preview** on the right
- As structured context when generating your AI resume

## AI‑powered resume

In the **AI‑Powered Resume** card:

1. **Model provider**: currently assumes an **OpenAI‑compatible** Chat Completions API.
2. **API base URL**: e.g. `https://api.openai.com` (or another compatible endpoint).
3. **API key**: paste your key here – it is used only in your browser to call the provider.
4. **Model name**: e.g. `gpt-4.1-mini` (or any model your provider supports).
5. **Target role / industry**: what kind of job you want the resume tailored to.
6. **Extra instructions**: tone, technologies to emphasize, seniority, etc.
7. Click **Generate resume**.

The app sends a `POST` request to:

```text
{API_BASE_URL}/v1/chat/completions
```

with a system prompt that instructs the model to behave like an **expert resume writer**, plus a user message that contains:

- Your target role
- Your saved profile (as JSON)
- Any extra instructions

The generated resume appears in the **textarea** below. Use **Copy to clipboard** to paste it into your editor or PDF tool.

## Privacy & security notes

- Your **API key is never stored** in localStorage – it only lives in memory while the page is open and is sent **only** to the base URL you configure.
- Your profile data is stored in localStorage under `portfolioHubProfile_v1`. Use **Reset** to clear it.

## Customizing

- Tweak layout and colors in `styles.css`.
- Adjust the system/user prompts in `app.js` inside `generateResume()` to match your style.
- Extend the form (e.g. add tech stack, years of experience) and include those fields in the JSON profile sent to the AI.

This should give you a solid starting point for a **personal portfolio + AI resume generator** that you can extend or deploy anywhere as static files.
