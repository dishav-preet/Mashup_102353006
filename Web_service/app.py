from flask import Flask, render_template, request
import zipfile
import smtplib
from email.message import EmailMessage
from mashup_script import create_mashup
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        try:
            singer = request.form["singer"]
            videos = int(request.form["videos"])
            duration = int(request.form["duration"])
            user_email = request.form["email"]

            output_file = "mashup.mp3"

            # Create mashup
            create_mashup(singer, videos, duration, output_file)

            # Zip the file
            zip_name = "mashup.zip"
            with zipfile.ZipFile(zip_name, "w") as zipf:
                zipf.write(output_file)

            # Send email
            send_email(user_email, zip_name)

            message = "Mashup created and sent successfully! 🎵"

        except Exception as e:
            message = f"Error: {str(e)}"

    return render_template("index.html", message=message)


def send_email(to_email, file_name):

    # Get credentials from environment variables
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")

    if not sender_email or not sender_password:
        raise Exception("Email credentials not set in environment variables.")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File 🎵"
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content("Your mashup file is attached.")

    with open(file_name, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="zip",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


if __name__ == "__main__":
    app.run(debug=True)
