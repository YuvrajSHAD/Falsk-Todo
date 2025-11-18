# Falsk-Todo
Not Your traditional todo app, read the whole story in readme.md 

# Todo-ish 🤷‍♂️

A hobby project that accidentally became a real webapp.

---

### Why I Built This

Honestly, I just wanted a place to jot down personal tasks and try out some Python-Flask-SQLAlchemy stuff for fun. At first, it was supposed to be local-only—a "useless" playground project.  
But, turns out my sister also wanted to use it (and keep her embarrassing tasks secret from me!).  
So I ended up adding a **login** system to keep everyone's tasks separate instead of one big list where everything got mixed up.  
That little feature snowballed into a multi-user, cloud-hosted, real database "thing." Now we're both stuck using it, I guess.

---

### What Can This Webapp Do?

- **User Accounts:** Register and log in to keep your todos separate (because siblings).
- **CRUD Tasks:** Add, edit, move, mark as done/undone—basic notebook experience but digital.
- **Sticky Notes UI:** Drag tasks around, organize by "page" like a real notebook.
- **Mobile Friendly:** Mostly works on mobile, but it's not a designer's portfolio, just saying.
- **OTP Login:** Extra non-annoying protection for your precious to-dos.
- **Fast enough:** Hosted using Vercel and Supabase, so it's basically always up (unless free hosting sleeps).

---

### Features

- Each user only sees their own tasks (privacy!).
- Supports creating, updating, and deleting todos.
- Drag-and-drop—and positional saving, for extra "notebook" vibes.
- Auth/OTP so friends, siblings, or enemies can't nuke your tasks.
- Minimal design (since it's just for us two).
- Can mark tasks as "done" and move them wherever you want.

---

### What's Next? (Future Plans & Dreams)

- **AI Assistant:**  
  Planning to slap on some AI to suggest tasks, motivate (or roast) you, or maybe help organize stuff.
- **Built-in Music Player:**  
  Because why open two tabs? Would love a little embedded, **ad-free** music player (probably YouTube-dl or some audio API magic).
- **Color Themes/Labels:**  
  Customize pages, add colors, and labels—procrastination just got fancier.
- **Reminders/Push Notifications:**  
  Letting you know about overdue stuff you’ve been ignoring.
- **Not-so-useless-anymore Mode:**  
  Maybe opening up for friends, if it ever gets stable (let’s be real, probably not).

---

### Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** Vanilla JS, basic HTML/CSS (Because React was too much for a "useless" project)
- **Database:** Supabase (PostgreSQL, free-tier vibes)
- **Auth:** Flask-Login, OTP for good measure
- **Hosting:** Vercel (Because deploy should be easy)

---

### Final Words

This project started as me messing around and ended up as a surprisingly useful little todo thing that works for me and my sister.  
If you somehow stumbled here and want to use it—uh, fork it or whatever, but it's truly just a personal playground.  
The most accurate description: **from useless to slightly less useless, thanks to family bug reports.**

### Anyone want to contribute

Help me update some UI changes like Edit & Mark done as seperate symbols instead of a list in a 3 dots scenario and trash icon would be nice so that i can drag and drop it in trash incase i my life hit have other plans

