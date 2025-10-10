from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime


# ==============================
# OTP Email HTML Template
# ==============================
OTP_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OTP Verification</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #f5f7fa;
      font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    .container {{
      max-width: 600px;
      margin: 40px auto;
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    }}
    .header {{
      background: linear-gradient(135deg, #4a90e2, #007bff);
      color: white;
      text-align: center;
      padding: 30px 20px;
    }}
    .header h1 {{
      margin: 0;
      font-size: 28px;
      font-weight: 600;
    }}
    .content {{
      padding: 40px 30px;
      text-align: center;
      color: #333333;
    }}
    .content p {{
      font-size: 16px;
      margin-bottom: 20px;
      line-height: 1.6;
    }}
    .otp-box {{
      display: inline-block;
      font-size: 34px;
      letter-spacing: 10px;
      font-weight: bold;
      color: #ffffff;
      background: #28a745;
      padding: 18px 32px;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      margin: 25px 0;
    }}
    .button {{
      display: inline-block;
      background: #007bff;
      color: #ffffff !important;
      text-decoration: none;
      font-size: 16px;
      font-weight: 500;
      padding: 12px 25px;
      border-radius: 6px;
      margin-top: 20px;
      transition: background 0.3s ease;
    }}
    .button:hover {{
      background: #0056b3;
    }}
    .footer {{
      background: #f0f3f8;
      color: #888888;
      text-align: center;
      font-size: 14px;
      padding: 20px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <h1>🔐 OTP Verification</h1>
    </div>

    <!-- Content -->
    <div class="content">
      <p>Hello,</p>
      <p>We received a request to verify your account. Use the OTP below to complete your login or registration process:</p>
      <div class="otp-box">{otp}</div>
      <p>This OTP is valid for <strong>20 minutes</strong>. Please do not share it with anyone for security reasons.</p>
      <a href="#" class="button">Verify Now</a>
    </div>

    <!-- Footer -->
    <div class="footer">
      &copy; {year} <strong>Your Company</strong>. All Rights Reserved.<br>
      If you didn’t request this, you can safely ignore this email.
    </div>
  </div>
</body>
</html>
"""


# ==============================
# Celery Task to Send OTP Email
# ==============================
@shared_task(bind=True, name="send_otp_email_task")
def send_otp_email_task(self, to_email, otp):
    """
    Celery task to send a styled HTML OTP email.
    """
    subject = "Your OTP Code"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Fill placeholders (otp and year)
    html_content = OTP_EMAIL_TEMPLATE.format(
        otp=otp,
        year=datetime.now().year
    )

    # Create and send email
    mail = EmailMultiAlternatives(subject, "", from_email, [to_email])
    mail.attach_alternative(html_content, "text/html")
    mail.send(fail_silently=False)

    return f"✅ OTP email sent to {to_email}"
