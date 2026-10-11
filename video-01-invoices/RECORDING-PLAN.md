# Video 1 Recording Plan: Invoices on Autopilot

The automation is built and live. This is the plan for turning it into the first video.
Budget: about 6 hours spread over the week. Nothing here needs money.

## Part 1. Before you press record (45 min)

### Protect the live workflow
1. In n8n, open the workflow list. On "Invoices on Autopilot" click the three dots, **Duplicate**. Name the copy `Invoices on Autopilot (recording)`.
2. Open the copy and delete every node so the canvas is blank. You will rebuild it on camera.
3. Open the live one and **Unpublish** it for the recording session. If both run, every test email writes two rows. Publish it again when you are done.

### Clean the demo data
1. In the Google Sheet, delete rows 2 onward on both tabs. Keep the header rows.
2. In Gmail, archive the four test emails (select, then the archive icon). Keep the Invoices label and the filter.
3. Rename the n8n credentials so the email address never appears on screen: Credentials page → Gmail credential → rename to `Gmail (demo)`; Google Sheets credential → `Google Sheets (demo)`; Gemini credential → `Gemini (free key)`.

### Clean the screen
1. Chrome: create a new profile called "Recording". No bookmarks bar, no extensions, no personal tabs. Sign in to the channel Gmail only.
2. Browser zoom 125% on n8n, Gmail and Sheets. Viewers watch on phones.
3. Dark mode in n8n (Settings → Personal → Theme). Light mode in Gmail and Sheets is fine.
4. Close every other app. Do Not Disturb on. Hide the Mac dock (System Settings → Desktop & Dock → automatically hide).
5. Display: 1920x1080 if you can set it, otherwise record at native and scale in editing.

### OBS (free, obsproject.com)
| Setting | Value |
|---|---|
| Scene | one scene, one source: Display Capture |
| Video | base and output 1920x1080, 30 fps |
| Recording format | MKV, then File → Remux to MP4 after recording |
| Audio | mic on its own track, desktop audio muted |
| Hotkey | set Start/Stop Recording to one key you can find without looking |

Do a 20-second test recording and play it back before the real session.

## Part 2. Shot list (2 hours of recording for about 10 minutes of video)

Record each clip separately. Press stop between clips. A clip with a mistake you did not plan to show gets re-recorded, not fixed in editing.

| Clip | Script section | What is on screen | Target length |
|---|---|---|---|
| 01 | Hook | Gmail inbox with three invoice emails arriving, then the Sheet filling. Record this LAST, after the full test works, by sending the three emails again. | 20 s |
| 02 | Promise | The finished workflow on the n8n canvas, zoomed to fit. Record LAST too. | 15 s |
| 03 | The problem | Open Brightlane PDF by hand, copy vendor, switch to Sheet, paste, repeat for amount. Move slowly. | 40 s |
| 04 | Step 1 · label | Gmail search options box, fill in `invoice OR "tax invoice"`, tick Has attachment, Create filter, choose label Invoices. | 60 s |
| 05 | Step 2 · trigger | Blank canvas → add Gmail Trigger → credential → Simplify off → Download Attachments on → Label Invoices → Fetch Test Event → Binary tab shows attachment_0. Send the Brightlane email to yourself just before this clip. | 90 s |
| 06 | Step 3 · read PDF | Add Extract from File → Extract From PDF → type `attachment_0` → Execute step → text appears. Show the `data` default first and the error it gives, then fix it. That is the first gotcha. | 60 s |
| 07 | The gotcha · scanned | Add If → expression → "is not empty" → Execute → Brightlane goes to True. Explain the scanned case in voice-over. | 60 s |
| 08 | Step 4 · AI | Add Information Extractor → paste Text expression → add five attributes → system prompt → add Gemini model → pick your key → Execute → clean JSON. Mention the leading-space mistake. | 120 s |
| 09 | Step 5 · sheet | Add Google Sheets Append → pick sheet → map seven columns → Execute → row appears in the Sheet (switch tab to show it). | 90 s |
| 10 | Needs check | From the False output add second Sheets node → Needs check tab → map four columns. No execute. | 40 s |
| 11 | Publish | Click Publish, name the version, confirm. | 15 s |
| 12 | The test | Send CloudNest, Sharma and Patel emails. Cut to the Sheet. Rows appear. Click Needs check tab, Patel is there. | 60 s |
| 13 | Outro | Workflow canvas, then the Sheet. | 20 s |

Tips:
- Pause one full second before and after every click.
- Do not talk while recording. Voice comes later and you will match clips to it.
- After each clip, write down the clip number and whether it was good.

## Part 3. Voice (45 min)

**Own voice (recommended).** Zero policy risk, builds trust fastest, costs nothing.
1. Quiet room, phone on airplane mode, record with the Mac's QuickTime (File → New Audio Recording) or in OBS with the screen source hidden.
2. Read the script one section at a time. If you stumble, pause two seconds and read the sentence again. The pause makes the cut easy.
3. Clean it free at podcast.adobe.com (Enhance Speech).

**AI voice (if you really do not want your voice).** ElevenLabs free tier is enough for one video a week. Pick one calm voice and never change it. Tick "altered or synthetic content" at upload and keep the line "Narration uses an AI voice" in the description.

## Part 4. Edit (90 min)

Free editors: DaVinci Resolve (Mac, powerful) or CapCut desktop (simpler). Pick one and keep it.

1. Lay the voice track down first. It sets the timing.
2. Drop clips in order under the voice. Trim each clip to match the sentence it illustrates. Speed up long typing to 2x or 3x.
3. Add a step label in the top left for each step: "Step 2 of 5 · Gmail trigger". Same font and position every time.
4. Blur anything personal: the Gmail address in the top right of Gmail, any credential name that slipped through.
5. Zoom in (120 to 150%) on the exact box you are typing in during clips 05 to 09. Phones cannot read n8n at full width.
6. Export: 1080p, 30 fps, MP4, H.264.

## Part 5. Upload checklist

| Field | Value |
|---|---|
| Title | I automated my invoices in 20 minutes (no code) |
| Visibility | Scheduled, Tuesday 15:00 IST |
| Thumbnail | left: messy inbox screenshot, right: clean sheet, text "INVOICES: AUTOMATED" |
| Description | use the template in the playbook, add the template link and the Sheet template link |
| Chapters | 0:00 Hook · 0:35 The manual way · 1:15 Label the emails · 2:15 Gmail trigger · 3:45 Read the PDF · 4:45 Scanned invoices · 5:45 AI reads it · 7:45 Write to the sheet · 9:15 Test · 10:00 Next |
| Altered or synthetic content | tick only if you used an AI voice |
| Tags | from the channel keywords list |
| End screen | subscribe + "next video" placeholder |
| Pinned comment | "Template and sheet links are in the description. Stuck on a step? Reply with the step number." |

## Part 6. Template files for the description (20 min)

1. n8n: workflow three dots → **Download**. The JSON has no secrets, but open it in a text editor and search for your email address and the sheet ID just to be sure. Replace the sheet ID with `YOUR_SHEET_ID`.
2. Google Sheet: File → Make a copy → name it `Invoices Tracker (template)` → delete data rows → Share → Anyone with the link, Viewer.
3. Upload the JSON to Gumroad as a free product "Invoices on Autopilot template" (price 0, ask for email). Put the Gumroad link and the Sheet link in the description.

## Time budget for the week

| Day | Task | Time |
|---|---|---|
| Mon | Part 1 prep, OBS test | 45 min |
| Tue | Clips 03 to 11 | 90 min |
| Wed | Clips 12, 01, 02 and any re-dos; voice | 75 min |
| Thu | Edit | 90 min |
| Fri | Thumbnail, upload, schedule, Gumroad template | 60 min |
| Sat | Republish the live workflow, delete the recording copy, LinkedIn post about the video | 20 min |
