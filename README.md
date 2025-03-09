# 🚄 **Korail Ticket Auto-Booking Bot**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/2e014356-7dfd-4117-8fdf-1a455dee4e8d">
</p>

## ⚠️ **Project Status (Important)**  

> ⚠️ **This project was last used in March 2024 and may no longer work due to UI changes on the Korail website.**  
> If you plan to run this project, **review the code and update it to match the latest environment.**  

## 🚀 **Why This Project Was Made Public**  

This project was originally developed as a private repository for **automating train ticket reservations on Korail**.  
However, at that time, I mistakenly included **sensitive account credentials (ID & password) in commits**, making the original repository unsuitable for public release.  

Thus, I created **a new public repository** with personal information removed, preserving the project's key functionalities for portfolio purposes.    
<br>
![image](https://github.com/user-attachments/assets/d3b346a7-90d5-41df-9a34-ae43670af616)

## 📌 **Project Overview**  

This project is a **Python-based bot that automates searching for and booking canceled Korail train tickets**.  
Since tickets are frequently canceled before departure, the bot continuously searches for available tickets and automatically books them when found.  
Previously, the project was also **deployed on AWS using Docker**, mainly for learning purposes.  

---

## ✨ **Key Features**  
### 🎫 **Automated Train Ticket Reservation**  
✅ **Auto-login to Korail website** using stored credentials  
✅ **Real-time seat availability search** for canceled tickets  
✅ **Automatic ticket booking** upon seat availability detection  

### 🤖 **Telegram Bot Integration**  
✅ **User-friendly Telegram bot commands** for setting train details  
✅ **Live updates on search & booking status** via Telegram messages  

### ☁️ **AWS Deployment (Previously Tested)**  
✅ The bot was **deployed on AWS with Docker** as a learning experiment  

---

## 🔧 **Installation & Setup**  

### 1️⃣ **Install Required Libraries**  

```bash
pip install -r requirements.txt
```

### 2️⃣ **Set Up Chrome WebDriver**  
- Uses `webdriver_manager` for **automatic installation**  
- Alternatively, download ChromeDriver manually and add it to the system PATH  

### 3️⃣ **Set Environment Variables**  
Create a `.env` file and add your **Telegram bot token**:  

```env
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

### 4️⃣ **Run the Program**  
To start the bot:  

```bash
python __init__.py
```

---

## 📂 **Project Folder Structure**  

```
/project-root
│── korail.py        # Main script for handling Korail ticket reservations  
│── telegram.py      # Handles Telegram bot interactions  
│── __init__.py      # Entry point for running the bot  
│── Dockerfile       # Docker configuration (previously used for AWS deployment)  
│── .env             # Environment file containing sensitive credentials  
```

---

## 📡 **How It Works**  

1️⃣ **User interacts with the Telegram bot** to input departure station, destination, date, and time.  
2️⃣ **The bot continuously searches for canceled tickets** on the Korail website.  
3️⃣ **If a ticket is found, the bot automatically books it**.  
4️⃣ **Booking confirmation and updates are sent to the user via Telegram**.  

---

## ⚙️ **Running Locally**  

If you want to run the bot on your local machine instead of AWS, update `korail.py`:  

```python
is_aws = False  # Set to False for local execution
```

This ensures that the program does **not** use AWS-specific configurations and runs locally on your system.  

---

## ⚠️ **Important Notes**  
- **This project may no longer work after March 2024** due to changes in the Korail website.  
- **If the website updates, modifications to the code may be required**.  
- **Since this project uses Selenium, ensure you have the correct Chrome WebDriver installed**.  
- **This project was previously tested on AWS using Docker**, but deployment is no longer maintained.  

---

## 📜 **License**  
This project is **intended for portfolio use only** and is not permitted for commercial use.  
