from dotenv import load_dotenv
import os
import yagmail as yg
import pandas as pd
import time

load_dotenv()

password = os.getenv('EMAIL_PASS')
r_email = os.getenv('EMAIL')

# yag = yg.SMTP(r_email, password)

details = pd.read_csv('Marketing Agencies for Page 4_details.csv')
failed_emails = []
success_emails = []

start_overall = time.time()
for index, detail in details.head(59).iterrows():
    start = time.time()
    name = detail['Business Name']
    email = detail['Email']

    subject = f"{name}, let us handle your next presentation"
    content = f"""
    Hi {name},

    Your creatives should be brainstorming the next big campaign, not wrestling with PowerPoint.

    We know how frustrating it is when a great strategy gets bogged down by tedious slide formatting. That's why we're offering to take the worst part of pitching off your hands.

    For just $10 per slide, we’ll handle the design, alignment, and branding, ensuring every deck you send out is sharp, professional, and consistent.

    The Benefit is Simple: You eliminate the design stress and instantly free up your team to focus on billable client strategy—not slide maintenance.

    Let us build your next winning presentation.

    Ready to see how fast we can turn your ideas into a flawless deck?

    Send us your topic on whatsapp: https://wa.me/2349012452831
    """

    try:
        with yg.SMTP(r_email, password) as yag:
            yag.send(
                to=email,
                subject=subject,
                contents=content,
                # headers={
                #     "List-Unsubscribe": f"<mailto:{r_email}>"
                # }
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
