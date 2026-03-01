# AI & Data Science Symposium – Local Web App

This is a **simple local web application** for a college symposium conducted by the
Department of Artificial Intelligence and Data Science.

Tech stack:

- Backend: **Flask (Python)**
- Frontend: **HTML + CSS + JavaScript**
- Storage: **Excel file (`participants.xlsx`) using pandas + openpyxl**

## Features

- **Registration Page**
  - Fields: Name, College, Email, Phone
  - Saves details into `participants.xlsx`
  - Automatically creates the Excel file if it does not exist
  - Prevents duplicate registration by email

- **Login Page**
  - Login using Email + Phone
  - Validates data from `participants.xlsx`
  - On success, redirects to **Dashboard**

- **Dashboard**
  - Greets the participant by name
  - Buttons to start **Round 1 (MCQ)** and open **Round 2 (Debugging)**

- **Round 1 – MCQ Round**
  - 10 MCQ questions stored in a Python list (`ROUND1_QUESTIONS` in `app.py`)
  - **10 minute timer** with JavaScript (`static/round1_timer.js`)
  - Auto-submits when time is over
  - Calculates score
  - Saves `round1_score` and `time_taken_seconds` to `participants.xlsx`

- **Round 2 – Debugging Round**
  - Shows 2 buggy Python programs
  - Participant types corrected code in text areas
  - Saves answers in `round2_answer1` and `round2_answer2` columns in Excel
  - `round2_score` column exists (admin updates manually later)

- **Admin Page (Password Protected)**
  - Password is defined in `app.py` as `ADMIN_PASSWORD` (default: `admin123`)
  - Shows a table of all participants with:
    - Round 1 score
    - Time taken (seconds)
    - Round 2 score
    - Computed **final score**
  - Button to download/export the current `participants.xlsx` file

- **Ranking Logic**
  - Implemented as `final_score(row)` in `app.py`
  - Uses:
    - `round1_score`
    - `round2_score`
    - `time_taken_seconds` to compute a `time_efficiency_score`
  - `final_score` formula:

  \[
  final\_score = 0.4 \times round1\_score + 0.5 \times round2\_score + 0.1 \times time\_efficiency\_score
  \]

  - Admin view sorts participants in **descending order of final_score**

## Project Structure

- `app.py` – main Flask application
- `templates/`
  - `base.html` – shared layout
  - `register.html` – registration page
  - `login.html` – login page
  - `dashboard.html` – participant dashboard
  - `round1.html` – MCQ round page
  - `round1_result.html` – Round 1 result page
  - `round2.html` – debugging round page
  - `admin_login.html` – admin login page
  - `admin.html` – admin dashboard (participants table + export button)
- `static/`
  - `style.css` – basic styling
  - `round1_timer.js` – JavaScript countdown timer + auto-submit for Round 1
- `participants.xlsx` – automatically created and updated by the app (Excel database)

## How to run the app

1. Open a terminal in this folder (where `app.py` is located).
2. Create/activate a virtual environment (optional but recommended).
3. Install dependencies:

   ```bash
   pip install flask pandas openpyxl
   ```

4. Run the Flask app:

   ```bash
   python app.py
   ```

5. Open your browser and go to:

   ```text
   http://127.0.0.1:5000
   ```

## Notes

- The app is designed to be **beginner friendly** and easy to modify.
- For real events, change `ADMIN_PASSWORD` and `app.secret_key` in `app.py`.
- All participant data is stored locally in `participants.xlsx` in the same folder as `app.py`.*** End Patch``` */}
