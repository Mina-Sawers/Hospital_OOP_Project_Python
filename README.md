# Hospital Management System

## Overview
The Hospital Management System is a Python-based desktop application featuring a Graphical User Interface (GUI). It relies on Object-Oriented Programming (OOP) principles to manage hospital departments, patients, and staff. 

The application follows the **Model-View-Controller (MVC)** architectural pattern. This design physically separates the application's internal data handling from its user interface, allowing multiple developers to work on different parts of the system simultaneously without causing conflicts.

---

## Project Structure (MVC Architecture)

Our repository is organized to maintain a clean separation of concerns. Here is a breakdown of where different components of the application live:

*   **`models/` (The Backend Logic)**
    *   Contains the pure OOP data structures (`Person`, `Patient`, `Staff`, `Department`, `Hospital`).
    *   These files handle data relationships and business logic. There is absolutely no GUI code in this directory.
*   **`views/` (The Frontend GUI)**
    *   Contains all the code responsible for drawing the screen, windows, buttons, and input forms.
    *   Responsible only for displaying data and capturing user input, not processing it.
*   **`controllers/` (The Application Glue)**
    *   Acts as the bridge between the `models` and `views`. 
    *   When a user clicks a button in the view, the controller processes that action, updates the models accordingly, and tells the view to refresh.
*   **`data/` (Data Persistence)**
    *   Stores the JSON or database files used to save the hospital state when the application is closed.
*   **`tests/` (Quality Assurance)**
    *   Contains unit tests to ensure that the core backend models and data storage functions behave as expected.

---

## Installation & Setup

Follow these steps to set up the project on your local machine.

### 1. Prerequisites
*   Ensure you have **Python 3.8+** installed.
*   (Optional but recommended) Install `git` for version control.

### 2. Clone the Repository
```bash
git clone [Insert your repository URL here]
