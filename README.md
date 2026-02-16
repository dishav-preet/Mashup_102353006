# YouTube Mashup Generator

A Python-based project that generates mashups from YouTube videos using both a Command-Line Interface (CLI) and a Web-Based Interface.

---

##  Project Description

This project performs the following steps:

1. Downloads YouTube videos of a given singer
2. Converts videos to MP3 format
3. Trims the first N seconds of each audio
4. Merges them into a single mashup file
5. (Web version) Sends the mashup as a ZIP file via email

---

# Program 1 – CLI Version

Command-line mashup generator.

###  Usage

```bash
python 102353006.py "Singer Name" 20 30 output.mp3
```
Parameters
*Singer Name → Artist to search
*20 → Number of videos (must be >10)
*30 → Duration in seconds (must be >20)
*output.mp3 → Final mashup file

## Program 2 – Web Version (Flask)

Web-based mashup service with HTML + CSS interface.

 Run Web App
 ```bash
cd Program2
python app.py
```
Then open in browser:
```bash
http://127.0.0.1:5000
```

User inputs:
-Singer Name
-Number of Videos
-Duration
-Email Address

The mashup is generated and sent via email.

Technologies Used
-Python
-Flask
-yt-dlp
-FFmpeg
-Node.js
-pydub
-HTML & CSS
-smtplib

Security
Email credentials are stored using environment variables:
```bash
setx EMAIL_USER "your_email"
setx EMAIL_PASS "your_app_password"
```

Warning:
YouTube may block automated downloads depending on network.


###submitted by:
Dishapreet Kaur
Roll No: 102353006
