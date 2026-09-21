import os
import pandas as pd
import numpy as np

def generate_scam_dataset(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Labeled real-world examples: 1 = Suspicious / Scam, 0 = Benign
    data = [
        # SCAM EXAMPLES (label=1)
        ("URGENT! Your SBI account will be blocked today. Verify your KYC immediately by clicking http://sbi-kyc-update.xyz and submit your OTP.", 1),
        ("Dear customer, your BESCOM electricity power will be disconnected tonight at 9:30 PM due to unpaid bill. Contact electricity officer immediately on 9876543210.", 1),
        ("Congratulations! You have won a cash prize of Rs 50,000 in Kaun Banega Crorepati lucky draw. Click http://kbc-reward-claim.top to claim money now.", 1),
        ("Your Paytm wallet KYC has expired. Please call customer care at +919812345678 or transfer Rs 10 to reactivate wallet immediately.", 1),
        ("Dear user, suspicious login detected from unknown device. Share OTP sent to your mobile number with customer care representative to block unauthorized transaction.", 1),
        ("Earn Rs 5,000 per day by rating hotels from home on Telegram! Initial registration fee of Rs 500 refundable after first task. Pay via UPI.", 1),
        ("Income Tax Refund of Rs 15,490 approved. Please update your bank account number and UPI PIN at http://it-refund-gov.link to receive credit.", 1),
        ("HDFC Bank Alert: Credit card reward points worth Rs 9,850 expiring tonight. Redeem points for cash now by clicking http://hdfc-points-claim.click", 1),
        ("Hi Mom, my phone broke and I am messaging from friend's number. Urgently need Rs 8,500 to pay medical bill. Please send to UPI: friend99@okhdfcbank immediately.", 1),
        ("Your parcel delivery is on hold due to missing address details. Pay Rs 25 redelivery fee at http://indiapost-update.info within 2 hours or parcel will be returned.", 1),
        ("Police notice: Legal action initiated against your phone number for illegal betting activity. Pay penalty of Rs 12,000 to avoid immediate arrest.", 1),
        ("Dear Customer, Your NetBanking access is disabled due to non-verification of Aadhaar. Click http://bank-secure-auth.xyz and enter password to restore.", 1),
        ("Work from home job offer: Amazon hiring product review specialists. Earn Rs 25,000 weekly. Scan this QR code to join premium group.", 1),
        ("Exclusive pre-approved loan of Rs 5,00,000 granted at 1% interest! Pay documentation fee Rs 2,999 to disburse loan in 10 minutes.", 1),
        ("Crypto doubling bot! Deposit 0.05 BTC or Rs 10,000 UPI and receive double in 24 hours guaranteed. Zero risk.", 1),
        ("Dear user, your SIM card will be deactivated within 24 hours due to TRAI regulations. Call telecom officer immediately at 9123456780.", 1),
        ("Emergency! Your nephew met with an accident and is in hospital. Needs urgent operation fee Rs 25,000. Send to UPI doctor.emergency@upi immediately.", 1),
        ("Amazon prize: You were selected as customer of the month! Claim iPhone 15 for just Rs 999 shipping fee. Click http://amzn-gift-claim.xyz", 1),
        ("Urgent notice from Axis Bank: Unauthorized transaction of Rs 49,999 initiated. To cancel transaction click link http://axis-dispute.top and enter OTP.", 1),
        ("Scan this QR code to receive Rs 2,000 refund from PhonePe customer support.", 1),
        ("You have an unpaid traffic challan of Rs 1,000. Pay immediately at http://echallan-vahan.link or your vehicle registration will be cancelled.", 1),
        ("Congratulations! Your mobile number won Rs 25 Lakh in UK Visa lottery. Contact agent on WhatsApp +447891234567 and pay customs clearance fee.", 1),

        # BENIGN EXAMPLES (label=0)
        ("Your monthly electricity bill for meter 482910 is Rs 1,240. Due date is 28th Sep. Pay conveniently via your utility board portal or authorized app.", 0),
        ("Your Amazon order #402-9182391 has been dispatched and will arrive by tomorrow, 6 PM. Track your package in the official Amazon app.", 0),
        ("Dear Customer, your savings account XXXXXX1290 has been credited with Rs 45,000 towards salary for Sep 2026. Available balance: Rs 78,920.", 0),
        ("OTP for logging into your Swiggy account is 849201. Valid for 10 minutes. Do NOT share this OTP with anyone, including delivery partners.", 0),
        ("Hey, are we still meeting for lunch at 1 PM today? Let me know so I can reserve a table at the cafe.", 0),
        ("Your flight 6E-204 from Bengaluru to Delhi is on schedule for departure at 15:45 from Terminal 1. Boarding gate opens at 15:00.", 0),
        ("Reminder: Your dentist appointment with Dr. Sharma is confirmed for Wednesday at 4:30 PM. Reply NO to reschedule.", 0),
        ("Your subscription to Spotify Premium will renew on 5th Oct for Rs 119. You can manage your subscription settings anytime in your account.", 0),
        ("Dear Customer, statement for your HDFC Bank credit card ending 4012 for billing cycle Sep 2026 has been sent to your registered email.", 0),
        ("Thank you for dining at Barbeque Nation. Your invoice amount of Rs 2,150 has been settled. We would love your feedback on the dining experience.", 0),
        ("Your Uber ride receipt: Rs 342 charged to your payment method for trip from Indiranagar to Whitefield. Thank you for riding with Uber.", 0),
        ("Team, please remember to submit your weekly timesheets before Friday 5 PM through the corporate intranet portal.", 0),
        ("Your book order has been delivered to the reception desk. Please collect it at your convenience.", 0),
        ("Can you please share the slide deck from yesterday's presentation when you get a chance? Thanks!", 0),
        ("Dear policyholder, your health insurance policy #918204 is due for annual renewal on 15th Oct. Visit our official website to view terms.", 0),
        ("Hi Rahul, sent you the notes from today's machine learning lecture. Let's study for the midterms this weekend.", 0),
        ("Your payment of Rs 599 for mobile recharge of 9845012345 was successful. Unlimited calls and 2GB/day valid for 28 days.", 0),
        ("Meeting invite: ScamShield Project Sync on Monday at 10:00 AM via Google Meet.", 0),
        ("Good morning! Don't forget mom's birthday dinner tomorrow evening at 7:30 PM.", 0),
        ("Your package has been placed in your apartment parcel locker #12. Access code is sent to your resident app.", 0),
        ("Class schedule update: The operating systems lab on Thursday is shifted to Room 302.", 0),
        ("Thank you for your order at Domino's Pizza. Your pizza is in the oven and will be delivered in 20 minutes.", 0)
    ]

    df = pd.DataFrame(data, columns=["text", "label"])
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path} with {len(df)} samples.")
    return df

if __name__ == "__main__":
    generate_scam_dataset("ml/datasets/demo_scam_dataset.csv")
