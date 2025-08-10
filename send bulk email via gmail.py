from dotenv import load_dotenv
import os
import yagmail as yg
import pandas as pd
import time

load_dotenv()

password = os.getenv('EMAIL_PASS')
r_email = os.getenv('EMAIL')

# yag = yg.SMTP(r_email, password)

details = pd.read_csv(r'C:\Users\Precious\Downloads\Untitled spreadsheet - Sheet1.csv')
failed_emails = []
success_emails = []

start_overall = time.time()
for index, detail in details.head(50).iterrows():
    start = time.time()
    name = detail['Name']
    email = detail['Email']


    content = f"""
    Hi {name},

    I wanted to personally share with you an opportunity to explore Buzz2Serv — a new community-driven platform connecting local homeowners and businesses with trusted contractors.

    You can try it free for the first 3 months. We only take a commission when you get paid.

    Learn more here: https://buzz2serv.com/

    Best regards,
    Precious
    Buzz2Serv Team
    """

    try:
        with yg.SMTP(r_email, password) as yag:
            yag.send(
                to=email,
                subject=f"Hello {name}",
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
