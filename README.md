# 🌿 Virtual Herbal Garden – AYUSH Medicinal Plant Explorer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![AI](https://img.shields.io/badge/AI-Anthropic%20SDK-orange)


### 🪴 An Interactive AI-Powered Virtual Herbal Garden for AYUSH Medicinal Plants

</div>

---

# 📖 Overview

The **Virtual Herbal Garden** is an interactive digital platform designed to preserve, explore, and promote knowledge about medicinal plants used in the AYUSH sector.

This project combines:

* 🌱 Traditional herbal knowledge
* 🤖 AI-powered interaction
* 🌍 Virtual exploration
* 📚 Educational content
* 🧠 Smart search & bookmarking

Users can explore medicinal plants through an immersive virtual experience featuring detailed plant information, multimedia content, guided tours, and AI-assisted learning.

---

# ✨ Features

## 🌿 Medicinal Plant Library

* Detailed medicinal plant database
* Botanical & common names
* Medicinal benefits and uses
* Habitat & cultivation methods
* AYUSH relevance

---

## 🧠 AI Herbal Assistant

* AI chatbot using **Anthropic SDK**
* Ask questions about:

  * Medicinal uses
  * Cultivation
  * Herbal remedies
  * Plant identification
  * Traditional AYUSH practices

---

## 🔍 Advanced Search & Filters

Search plants by:

* Medicinal use
* Plant category
* Region
* Herbal properties
* Botanical name

---

## 🖼 Multimedia Integration

* High-quality plant images
* Educational videos
* Audio descriptions
* Interactive learning content

---

## 🌐 Virtual Tours

Guided tours based on themes:

* Immunity boosting herbs
* Digestive health plants
* Skin care medicinal plants
* Ayurvedic essentials
* Home herbal remedies

---

## ⭐ User Features

* User registration/login
* Bookmark favorite plants
* Add personal notes
* Save herbal collections
* Share information

---

## 📱 Responsive UI

* Mobile-friendly interface
* Modern and clean design
* Easy navigation
* Fast loading experience

---

# 🏗 Project Structure

```bash
virtual-herbal-garden/
│
├── app/
│   ├── models/
│   │   ├── plant.py
│   │   ├── user.py
│   │   ├── tour.py
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── plants.py
│   │   ├── users.py
│   │   ├── tours.py
│   │   └── ai.py
│   │
│   ├── static/
│   │   ├── images/
│   │   ├── videos/
│   │   ├── audio/
│   │   └── css/
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── __init__.py
│
├── tests/
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

---

# 🛠 Tech Stack

| Technology    | Purpose               |
| ------------- | --------------------- |
| Python        | Backend Development   |
| Flask         | Web Framework         |
| SQLite        | Database              |
| HTML/CSS/JS   | Frontend              |
| Anthropic SDK | AI Chat Integration   |
| Bootstrap     | Responsive UI         |
| REST API      | Backend Communication |

---

# ⚙ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/virtual-herbal-garden.git
cd virtual-herbal-garden
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
ANTHROPIC_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
FLASK_ENV=development
```

---

# ▶ Running the Project

```bash
python run.py
```

Application will run on:

```bash
http://127.0.0.1:5000
```

---

# 📸 Screenshots

## 🌱 Home Page

* Virtual herbal garden interface
* Search and explore plants

## 🌿 Plant Details

* Botanical information
* Medicinal uses
* Multimedia content

## 🤖 AI Chat Assistant

* Interactive herbal guidance
* AI-powered answers

---

# 🧪 Example Features

## Search Example

```python
/search?name=Tulsi
```

## AI Chat Example

```python
POST /ai/chat
{
  "message": "What are the medicinal uses of Ashwagandha?"
}
```

---

# 🌍 Future Enhancements

* 🌱 Full 3D interactive plant models
* 🥽 VR/AR integration
* 🌐 Multi-language support
* 📱 Mobile application
* 🎤 Voice assistant support
* 🧬 AI-based plant recognition
* ☁ Cloud deployment

---

# 🎯 Expected Impact

The Virtual Herbal Garden aims to:

* Promote AYUSH awareness
* Digitally preserve herbal knowledge
* Support students and researchers
* Encourage natural healthcare education
* Make medicinal plant knowledge accessible worldwide

---

# 🙌 Acknowledgements

Special thanks to:

* AYUSH Ministry
* Open-source community
* Medicinal plant researchers
* Flask & Python ecosystem

---

# ⭐ Support

If you like this project:

⭐ Star this repository
🍴 Fork the project
🛠 Contribute improvements

---

<div align="center">

## 🌿 “Nature itself is the best physician.” 🌿

</div>
