# Weather App server
**Django server for weather app deployed on azure**<br>


## 🚀 Quick Start

### Prerequisites

* [Python 3.12](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/)
* [Rust](https://www.rust-lang.org/tools/install)
* [Node.js (16+)](https://nodejs.org/)
* [npm](https://www.npmjs.com/) (bundled with Node.js)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/RudyKarpus/Weather-App-Server.git
   cd weather-app-server
   ```

2. **Ensure Docker Desktop is running**

3. **Build and run the application**

   ```bash
   docker build -t weather-app-server .
   docker run -d -p 8000:8000 weather-app-server
   ```

4. **Access the api**
   Navigate to [http://localhost:8000](http://localhost:8000)

---

<a name="documentation"></a>

## 📚 Documentation

### 🧠 General Overview

* Project documentation available [here](https://rudykarpus.github.io/Weather-App-Server/)

### 🧪 API Documentation

* Swagger available at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) (when app is running)

### 🛠️ Building with Sphinx (Python)

1. **Install development dependencies**

   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Generate HTML docs**
   From inside `server/docs`:

   **Linux**:

   ```bash
   make html
   xdg-open build/html/index.html
   ```

   **Windows**:

   ```bash
   .\make.bat html
   Start-Process .\build\html\index.html
   ```

---


