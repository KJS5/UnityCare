# UnityCare FullStack V9 — OpenRouter Typed AI Chat

UnityCare is a full-stack family care coordination web app with real account creation, login validation, SQLite persistence, manual data entry, and an AI assistant powered through OpenRouter.

The assistant now uses a normal typed chat input. Users can write their own questions, and each message is sent from the backend to OpenRouter with the saved UnityCare data for the logged-in user.

## Main features

- Real sign up and login validation
- Internal pages require a valid session
- SQLite database persistence
- Care recipient profile management
- Family member management
- Task management
- Medication management
- Appointment management
- Care journal
- Notifications
- Typed OpenRouter AI chat assistant
- OpenRouter integration through server environment variables
- English and Arabic UI support
- RTL layout for Arabic
- Glassmorphism responsive design

## Important security note

Do not hardcode your OpenRouter key inside `server.py`, `app.js`, GitHub, or any public file. Add it as an environment variable on Render or in a local `.env` file.

If a key was posted publicly or committed to GitHub, rotate it from the OpenRouter dashboard and use a new key.

## Local setup

Python 3.10 or newer is recommended.

Install requirements:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the same folder as `server.py`:

```text
UNITYCARE_SECRET=replace-with-a-long-random-secret
OPENROUTER_API_KEY=paste-your-openrouter-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_NAME=UnityCare
OPENROUTER_SITE_URL=http://localhost:8787
PORT=8787
HOST=0.0.0.0
```

Run the app:

```bash
python server.py
```

Open:

```text
http://localhost:8787
```

## Render setup

In Render, go to your UnityCare web service, then add these environment variables:

```text
UNITYCARE_SECRET=replace-with-a-long-random-secret
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_NAME=UnityCare
OPENROUTER_SITE_URL=https://your-render-link.onrender.com
```

Then redeploy the service.

Recommended Render commands:

```text
Build Command: pip install -r requirements.txt
Start Command: python server.py
```

If your app files are inside a subfolder, set Render's Root Directory to that folder.

## How the AI assistant works

1. The user logs in.
2. The user manually adds care recipient information, family members, tasks, medications, appointments, and journal entries.
3. The user opens the AI Assistant page.
4. The user writes a question in the AI chat box.
5. The backend collects the saved SQLite data for that logged-in user.
6. The backend sends the typed question and saved app data to OpenRouter.
7. The assistant response is saved in SQLite chat history and shown on the page.

The assistant is instructed to:

- Use only saved UnityCare data.
- Say clearly when data is missing.
- Avoid inventing family members, medications, tasks, or appointments.
- Avoid medical diagnosis.
- Remind users to confirm medication or health concerns with a doctor or pharmacist.
- Reply in the user's selected language.

## Authentication test

Try this before presenting:

1. Open `http://localhost:8787/#dashboard` before logging in.
2. It should send you back to login.
3. Try random login details.
4. It should reject them.
5. Create an account through Sign Up.
6. Add care data manually.
7. Open AI Assistant and type a question.

## Folder structure

```text
UnityCare_FullStack_V9_TYPED_OPENROUTER/
  server.py                  Backend server + SQLite API + OpenRouter typed assistant
  requirements.txt           Python dependencies
  .env.example               Example environment settings
  data/
    .gitkeep                 SQLite database is created here when the app runs
  static/
    index.html
    styles.css
    app.js
    favicon.svg
    assets/
      unitycare-logo.svg
```

## Cast / present it

Open the website in Chrome, click the three dots, choose **Cast**, select your TV or projector, then choose **Cast tab**. Press `F11` for fullscreen.
