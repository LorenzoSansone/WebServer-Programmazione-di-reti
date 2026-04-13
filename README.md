# Web Server - Policlinico S. Orsola-Malpighi

This project is a Python-based Web Server developed for the **Networking Programming** course (a.a. 2020 / 2021). It serves a website dedicated to managing and displaying information for the **Policlinico S. Orsola - Malpighi** hospital in Bologna.

---

## 🚀 Features

* **Multi-user Access:** The server supports multiple simultaneous user connections.
* **Console Authentication:** Users must authenticate via the command line before accessing the web content.
* **Graceful Termination:** Supports keyboard interruption (Ctrl+C) to safely release the socket and exit the process.
* **Dynamic Updates:** Includes a threading mechanism to update site content periodically without busy waiting.
* **PDF Downloads:** Features a dedicated link for downloading a PDF summary of hospital services.

---

## 🛠️ Technical Specifications

### Libraries Used
* **`http.server`**: Defines classes for implementing HTTP servers.
* **`socketserver`**: Simplifies the construction of network servers.
* **`threading`**: Manages background tasks for content refreshing.
* **`signal`**: Handles the keyboard interrupt (Ctrl+C).
* **`sys`**: Used for console input and process termination.

### Credentials
To log in once the server is started, use the following credentials:
* **Username:** `user123`
* **Password:** `standardpass`

---

## 📂 Navigation & Content

The website provides several dedicated pages for hospital services:

| Service | Description |
| :--- | :--- |
| **Reparti** | A list of hospital departments with links to their official sites. |
| **Cerca un medico** | A directory of doctors available within the facility. |
| **Privacy cittadini** | Privacy management policies for patients. |
| **Numeri utili** | Contact information for the call center and administrative offices. |
| **Libera professione** | Details on private healthcare services and access methods. |

---

## ⚙️ Installation and Usage

1. **Start the Server:** Launch the script from your IDE or terminal:
   ```bash
   py WebServer.py [port]
