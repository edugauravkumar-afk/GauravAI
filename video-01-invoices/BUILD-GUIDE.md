# Video 1 Build Guide: Invoices on Autopilot (n8n)

What you build: an invoice email arrives, the PDF is read by AI, and vendor, dates, amount
and currency land in a Google Sheet. Scanned invoices with no readable text go to a
"Needs check" tab instead of producing blank rows.

Time: about 2 hours the first time. Do it once off camera, then record.
Sample invoices are in `sample-invoices/` next to this file. Never use real invoices on camera.

## Part 0. Accounts (30 min, once)

1. **Gmail.** Use the channel Gmail. Create a label named `Invoices`.
2. **Google Sheet.** Create a sheet named `Invoice Log`.
   - Tab 1, `Invoices`, header row: `Vendor | Invoice date | Amount | Currency | Due date | Email link | Added at`
   - Tab 2, `Needs check`, header row: `From | Subject | Email link | Added at`
3. **n8n.** Go to n8n.io and start the Cloud free trial. 14 days, no card. After the trial,
   Starter is about $24 a month, or $20 a month billed yearly.
4. **AI key.** Go to aistudio.google.com, click Get API key, then Create API key. The free
   tier is enough for testing and recording.
5. **Second email account.** You need it to send test invoices to the channel Gmail.

## Part 1. Gmail filter (5 min)

1. In Gmail, click the filter icon at the right of the search bar.
2. Has the words: `invoice OR "tax invoice"`. Tick Has attachment.
3. Create filter, tick Apply the label, choose `Invoices`, create.

## Part 2. The workflow (60-90 min)

Create a new workflow named `Invoices on Autopilot`. Rename each node as you go; the names
look good on camera.

### Node 1: Gmail Trigger, renamed "New invoice email"
1. Click the plus, search Gmail, choose **On message received**.
2. Credential: Sign in with Google using the channel Gmail.
3. Poll Times: Every Minute while testing.
4. **Simplify: OFF.** With it on, attachments never arrive.
5. Filters, Label Names or IDs: `Invoices`.
6. Options, add **Download Attachments: ON**.
7. From your second account, email the Brightlane sample invoice to the channel Gmail with
   subject "Invoice October". Wait until Gmail labels it.
8. Click **Fetch Test Event**. In the output, open the Binary tab. You should see
   `attachment_0`, a PDF.

> Important: the expressions below refer to this node as `Gmail Trigger`. If you rename it,
> use drag-and-drop mapping instead of typing expressions, or keep the original name and
> change only the label shown on the canvas.

### Node 2: Extract from File, renamed "Read the PDF"
1. Plus, search Extract from File, choose **Extract From PDF**.
2. Input Binary Field: `attachment_0`.
3. Test step. The output has a `text` field with the invoice text.

### Node 3: If, renamed "Is it scanned?"
1. Plus, search If.
2. Condition: value `{{ ($json.text || '').trim() }}`, type String, operation **is empty**.
3. True means scanned (no text). False means a normal PDF.

### Node 4 (False branch): Information Extractor, renamed "AI reads the invoice"
1. From the False output, plus, search Information Extractor.
2. Text: `{{ $json.text }}`
3. Schema Type: **From Attribute Descriptions**. Add five attributes:

| Name | Type | Description | Required |
|---|---|---|---|
| vendor | String | Company that sent the invoice | yes |
| invoice_date | String | Invoice date as YYYY-MM-DD | yes |
| amount | Number | Total amount due including tax. Number only, no currency symbol | yes |
| currency | String | Three-letter currency code such as USD, GBP or INR | yes |
| due_date | String | Due date as YYYY-MM-DD. Leave empty if no due date is printed | no |

4. Options, System Prompt Template: add this line at the end:
   `Only use information printed on the invoice. Never guess a value that is not there.`
5. Under the node, click the plus on **Model**, choose **Google Gemini Chat Model**,
   create a credential with your AI Studio key, and pick a current Flash model from the list.
6. Test step. The output has `output.vendor`, `output.amount` and the rest.

### Node 5: Google Sheets, renamed "Add to invoice log"
1. Plus after node 4, search Google Sheets, choose **Append row in sheet**.
2. Document: `Invoice Log`. Sheet: `Invoices`.
3. Mapping Column Mode: Map Each Column Manually.

| Column | Value |
|---|---|
| Vendor | `{{ $json.output.vendor }}` |
| Invoice date | `{{ $json.output.invoice_date }}` |
| Amount | `{{ $json.output.amount }}` |
| Currency | `{{ $json.output.currency }}` |
| Due date | `{{ $json.output.due_date }}` |
| Email link | `https://mail.google.com/mail/u/0/#all/{{ $('Gmail Trigger').item.json.id }}` |
| Added at | `{{ $now.toFormat('yyyy-MM-dd HH:mm') }}` |

4. Test step. A row appears in the sheet.

### Node 6 (True branch): Google Sheets, renamed "Flag for manual check"
1. From the True output of node 3, add Google Sheets, **Append row in sheet**, sheet `Needs check`.
2. From and Subject: drag the from and subject fields from the Gmail Trigger output on the
   left panel into the boxes. Dragging avoids typing the wrong path.
3. Email link and Added at: same expressions as node 5.

## Part 3. Full test (15 min)

Email all four sample invoices to the channel Gmail, one email each, subject starting
"Invoice". Expected result:

| Sample file | Lands in | Vendor | Invoice date | Amount | Currency | Due date |
|---|---|---|---|---|---|---|
| invoice-brightlane-design.pdf | Invoices | Brightlane Design Studio | 2026-10-01 | 1308 | GBP | 2026-10-31 |
| invoice-cloudnest-hosting.pdf | Invoices | CloudNest Hosting Inc. | 2026-10-02 | 71 | USD | 2026-10-16 |
| invoice-sharma-accounting.pdf | Invoices | Sharma & Co. Chartered Accountants | 2026-10-03 | 14750 | INR | 2026-10-18 |
| invoice-patel-supplies-SCANNED.pdf | Needs check | sender and subject only | | | | |

## Part 4. Switch it on (2 min)

Turn the workflow on with the Active toggle (called Publish in newer n8n versions).
Change Poll Times to every 5 minutes.

## Part 5. Make the template (10 min)

1. Workflow menu, Download. n8n leaves credentials out of the file.
2. Make a copy of the Google Sheet with headers only and set sharing to "anyone with the link can view".
3. Put both links in the video description.

## If something breaks

| What you see | Cause | Fix |
|---|---|---|
| No `attachment_0` in node 1 | Simplify is on, or Download Attachments is off | Turn Simplify off, Download Attachments on, fetch again |
| Node 2 text is gibberish or empty | The PDF is a scanned image | Expected for the scanned sample. It should go down the True branch. |
| Error 429 from Gemini | Free-tier rate limit | Wait one minute and run again |
| Sheet columns missing in node 5 | Header row missing or sheet not refreshed | Add the header row, reselect the sheet |
| Trigger never fires | Label name differs, workflow off, or email not labelled yet | Check the label in Gmail, switch the workflow on, wait a minute |

Stuck on anything else: take a screenshot of the n8n screen with the error and send it to
Claude with the step number.

Sources checked for node names and settings: n8n docs for Information Extractor and Extract
from File; n8n community threads on Gmail Trigger attachments; n8n pricing pages; Gemini API
free tier guides (October 2026).
