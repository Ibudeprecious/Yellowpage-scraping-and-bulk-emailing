from dotenv import load_dotenv
import os
import yagmail as yg
import pandas as pd
import time

load_dotenv()

password = os.getenv('EMAIL_PASS')
r_email = os.getenv('EMAIL')

if r_email:
    r_email = r_email.strip('\'"')
if password:
    password = password.strip('\'"')

print("EMAIL loaded:", bool(r_email))
print("PASSWORD length:", None if password is None else len(password))

details = pd.read_csv('electrician.csv')
failed_emails = []
success_emails = []

start_overall = time.time()
for index, detail in details.head(150).iterrows():
    start = time.time()
    name = detail['name']
    email = detail['email']
    website = detail['website']

    subject = f"{name} - Top 3 on Google?"
    # Build plain-text and HTML alternatives (no attachments)
    plain_text = f"""Hi {name},

Noticed {name} currently not showing up in the top 3 on Google, which usually means you’re missing out on a lot of potential customers searching for your service.

We at Google Optimization Agency help local businesses get into the top 3 on Google AND Google Maps within 90 days - guaranteed.

If you'd like the case study image or PDF I can send it on request.

Can I send a 2-minute video showing exactly how we'd do this for you?

Regards,
{r_email}

If you don't want to receive these emails, reply with 'unsubscribe' to this message.
"""

    html_body = f"""<p>Hi {name},</p>
<p>Noticed {name} currently not showing up in the <strong>top 3 on Google</strong>, which usually means you’re missing out on a lot of potential customers searching for your service.</p>
<p>We at Google Optimization Agency help local businesses get into the top 3 on Google AND Google Maps within <strong>90 days - guaranteed</strong>.</p>
<p>If you'd like the case study image or PDF I can send it on request.</p>
<p>Can I send a 2-minute video showing exactly how we'd do this for you?</p>
<p>Regards,<br>{r_email}</p>
<p style="font-size:small;color:gray;">If you don't want to receive these emails, reply with 'unsubscribe'.</p>
"""

    try:
        with yg.SMTP(r_email, password) as yag:
            yag.send(
                to=email,
                subject=subject,
                contents=[plain_text, html_body],
                headers={"List-Unsubscribe": f"<mailto:{r_email}>"}
            )
        timetaken = time.time() - start
        print(f"Email sent to: {name} in {timetaken:.2f} seconds")
        success_emails.append(index + 2)

    except Exception as e:
        print(f"Failed to send to {name}: {e}")
        failed_emails.append(index + 2)

    time.sleep(60)  # slower send rate to reduce throttling/spam signals

print(f"{len(success_emails)} emails sent successfully!, {len(failed_emails)} failed.")
if failed_emails:
    print("Failed emails(their row numbers):", failed_emails)
# print("Successful emails:", success_emails)
overall_timetaken = time.time() - start_overall
print(f"Process completed in {overall_timetaken:.2f} seconds")  
