from dotenv import load_dotenv
import os
import yagmail as yg
import pandas as pd
import time

load_dotenv()

password = os.getenv('EMAIL_PASS')
r_email = os.getenv('EMAIL')

# yag = yg.SMTP(r_email, password)

details = pd.read_csv('plumber.csv')
failed_emails = []
success_emails = []

start_overall = time.time()
for index, detail in details.head(2).iterrows():
    start = time.time()
    name = detail['name']
    email = detail['email']
    website = detail['website']

    subject = f"{name} - Top 3 on Google?"
    content = f"""
    Hi {name},

    Noticed {name} currently not showing up in the top 3 on Google, which usually means you’re missing out on a lot of potential customers searching for your service.

    We at Google Optimization Agency help local businesses get into the top 3 on Google AND Google Maps within 90 days - guaranteed.

    Attached is an image that shows you how we helped Golden Thai get into the top 3 on Google and Google Maps in just 60 days.

    Based on your local competition I'm extremely confident we can do the same for you.

    Can I send a 2-minute video showing exactly how we'd do this for you?"""

    attachmets = ['image.jpeg','image (2).jpeg']
    try:
        with yg.SMTP(r_email, password) as yag:
            yag.send(
                to=email,
                subject=subject,
                contents=content,
                attachments=attachmets
            )
        timetaken = time.time() - start
        print(f"Email sent to: {name} in {timetaken:.2f} seconds")
        success_emails.append(index + 2)

    except Exception as e:
        print(f"Failed to send to {name}: {e}")
        failed_emails.append(index + 2)

    time.sleep(20)  # increase wait time

print(f"{len(success_emails)} emails sent successfully!, {len(failed_emails)} failed.")
if failed_emails:
    print("Failed emails(their row numbers):", failed_emails)
# print("Successful emails:", success_emails)
overall_timetaken = time.time() - start_overall
print(f"Process completed in {overall_timetaken:.2f} seconds")  
