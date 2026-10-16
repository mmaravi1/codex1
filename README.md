# Lingua Scout

A small, dependency-free language-learning web app. It includes starter phrases, speech playback, saved words, a practice counter, and a live language overview from Wikipedia.

## Run

With Node.js installed, run:

```powershell
node server.js
```

Then open `http://localhost:3000` in a browser.

The app requests public web content directly from Wikipedia at runtime. If that request is unavailable, the offline starter lesson remains usable.
