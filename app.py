from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
import time
import pandas as pd


app = Flask(__name__)
app.secret_key = "change_this_secret_for_production"

EXCEL_FILE = "participants.xlsx"
ADMIN_PASSWORD = "admin123"  # simple hard‑coded password for demo


def load_participants():
  """Load participants Excel file or return empty DataFrame with proper columns."""
  if not os.path.exists(EXCEL_FILE):
    columns = [
      "name",
      "college",
      "email",
      "phone",
      "round1_score",
      "time_taken_seconds",
      "round2_answer1",
      "round2_answer2",
      "round2_score",
    ]
    return pd.DataFrame(columns=columns)

  df = pd.read_excel(EXCEL_FILE)

  # Ensure required columns exist
  required_columns = [
    "name",
    "college",
    "email",
    "phone",
    "round1_score",
    "time_taken_seconds",
    "round2_answer1",
    "round2_answer2",
    "round2_score",
  ]
  for col in required_columns:
    if col not in df.columns:
      df[col] = None
  return df


def save_participants(df: pd.DataFrame):
  df.to_excel(EXCEL_FILE, index=False)


def final_score(row):
  """
  Compute final_score based on:
  0.4 * round1_score
  0.5 * round2_score
  0.1 * time_efficiency_score
  """
  round1 = row.get("round1_score", 0) or 0
  round2 = row.get("round2_score", 0) or 0

  # Time efficiency: faster than full 10 minutes gets higher score.
  # Max 10 points, 0 if time_taken is missing.
  time_taken = row.get("time_taken_seconds", None)
  max_seconds = 10 * 60
  if pd.isna(time_taken) or not time_taken:
    time_efficiency_score = 0
  else:
    # Clamp between 0 and max_seconds
    time_taken = max(1, min(max_seconds, float(time_taken)))
    time_efficiency_score = (max_seconds - time_taken) / max_seconds * 10.0

  return (0.4 * float(round1)) + (0.5 * float(round2)) + (0.1 * float(time_efficiency_score))


# -------------------- Round 1 Questions --------------------

ROUND1_QUESTIONS = [
  {
    "id": 1,
    "question": "Which of the following is a supervised learning algorithm?",
    "options": ["K‑Means Clustering", "Linear Regression", "Apriori", "DBSCAN"],
    "answer": "Linear Regression",
  },
  {
    "id": 2,
    "question": "Which evaluation metric is most suitable for imbalanced classification?",
    "options": ["Accuracy", "Precision‑Recall", "Mean Squared Error", "R‑Squared"],
    "answer": "Precision‑Recall",
  },
  {
    "id": 3,
    "question": "Which of these is used to prevent overfitting in neural networks?",
    "options": ["Dropout", "Batch Size", "Momentum", "Learning Rate"],
    "answer": "Dropout",
  },
  {
    "id": 4,
    "question": "What does PCA (Principal Component Analysis) primarily do?",
    "options": [
      "Classification",
      "Clustering",
      "Dimensionality Reduction",
      "Hyperparameter Tuning",
    ],
    "answer": "Dimensionality Reduction",
  },
  {
    "id": 5,
    "question": "Which library is commonly used in Python for data manipulation?",
    "options": ["NumPy", "Pandas", "Matplotlib", "Seaborn"],
    "answer": "Pandas",
  },
  {
    "id": 6,
    "question": "Which of the following is NOT a type of neural network?",
    "options": ["CNN", "RNN", "SVM", "GAN"],
    "answer": "SVM",
  },
  {
    "id": 7,
    "question": "In k‑fold cross validation, k usually refers to:",
    "options": ["Number of features", "Number of classes", "Number of splits", "Batch size"],
    "answer": "Number of splits",
  },
  {
    "id": 8,
    "question": "Which SQL command is used to remove a table and its data?",
    "options": ["DELETE", "DROP", "REMOVE", "TRUNCATE"],
    "answer": "DROP",
  },
  {
    "id": 9,
    "question": "Which of the following is a non‑relational database?",
    "options": ["MySQL", "PostgreSQL", "MongoDB", "SQLite"],
    "answer": "MongoDB",
  },
  {
    "id": 10,
    "question": "Which Python keyword is used to handle exceptions?",
    "options": ["catch", "error", "except", "final"],
    "answer": "except",
  },
]

ROUND1_DURATION_SECONDS = 10 * 60  # 10 minutes


@app.route("/")
def home():
  return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
  message = ""
  if request.method == "POST":
    name = request.form.get("name", "").strip()
    college = request.form.get("college", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()

    if not (name and college and email and phone):
      message = "Please fill in all fields."
    else:
      df = load_participants()
      if (df["email"].astype(str).str.lower() == email).any():
        message = "This email is already registered."
      else:
        new_row = {
          "name": name,
          "college": college,
          "email": email,
          "phone": phone,
          "round1_score": 0,
          "time_taken_seconds": None,
          "round2_answer1": "",
          "round2_answer2": "",
          "round2_score": 0,
        }
        df = df.append(new_row, ignore_index=True)
        save_participants(df)
        message = "Registration successful! You can now log in."

  return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
  message = ""
  if request.method == "POST":
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()

    df = load_participants()
    mask = (df["email"].astype(str).str.lower() == email) & (
      df["phone"].astype(str) == phone
    )

    if mask.any():
      participant = df[mask].iloc[0]
      session["user_email"] = participant["email"]
      session["user_name"] = participant["name"]
      return redirect(url_for("dashboard"))
    else:
      message = "Invalid email or phone."

  return render_template("login.html", message=message)


def login_required(func):
  from functools import wraps

  @wraps(func)
  def wrapper(*args, **kwargs):
    if "user_email" not in session:
      return redirect(url_for("login"))
    return func(*args, **kwargs)

  return wrapper


@app.route("/dashboard")
@login_required
def dashboard():
  name = session.get("user_name")
  return render_template("dashboard.html", name=name)


@app.route("/round1", methods=["GET", "POST"])
@login_required
def round1():
  if request.method == "GET":
    # Save start time in session
    session["round1_start_time"] = time.time()
    return render_template(
      "round1.html",
      questions=ROUND1_QUESTIONS,
      duration_seconds=ROUND1_DURATION_SECONDS,
    )

  # POST: evaluate answers
  start_time = session.get("round1_start_time", time.time())
  end_time = time.time()
  time_taken = end_time - start_time

  score = 0
  for q in ROUND1_QUESTIONS:
    user_answer = request.form.get(f"q{q['id']}", "")
    if user_answer == q["answer"]:
      score += 1

  email = session.get("user_email")
  df = load_participants()
  mask = df["email"].astype(str).str.lower() == str(email).lower()
  if mask.any():
    df.loc[mask, "round1_score"] = score
    df.loc[mask, "time_taken_seconds"] = int(time_taken)
    save_participants(df)

  return render_template("round1_result.html", score=score, total=len(ROUND1_QUESTIONS))


@app.route("/round2", methods=["GET", "POST"])
@login_required
def round2():
  buggy_program1 = """# Buggy Python program 1
numbers = [1, 2, 3, 4, 5]
for i in range(1, len(numbers)):
    print(numbers[i])  # Expect to print all numbers including first element
"""

  buggy_program2 = """# Buggy Python program 2
def add(a, b):
    return a - b  # Should add, not subtract

result = add(2, 3)
print("Result:", result)  # Expect 5
"""

  message = ""
  if request.method == "POST":
    answer1 = request.form.get("answer1", "")
    answer2 = request.form.get("answer2", "")
    email = session.get("user_email")

    df = load_participants()
    mask = df["email"].astype(str).str.lower() == str(email).lower()
    if mask.any():
      df.loc[mask, "round2_answer1"] = answer1
      df.loc[mask, "round2_answer2"] = answer2
      # round2_score column exists; admin will update later manually
      save_participants(df)
      message = "Round 2 answers submitted successfully!"
    else:
      message = "Could not find your registration. Please contact organizers."

  return render_template(
    "round2.html",
    buggy_program1=buggy_program1,
    buggy_program2=buggy_program2,
    message=message,
  )


@app.route("/admin", methods=["GET", "POST"])
def admin():
  if request.method == "POST":
    password = request.form.get("password", "")
    if password == ADMIN_PASSWORD:
      session["admin_logged_in"] = True
    else:
      flash("Incorrect admin password.", "error")

  if not session.get("admin_logged_in"):
    return render_template("admin_login.html")

  df = load_participants()
  if not df.empty:
    df = df.copy()
    df["final_score"] = df.apply(final_score, axis=1)
    df = df.sort_values("final_score", ascending=False)
    table_records = df.to_dict(orient="records")
  else:
    table_records = []

  return render_template("admin.html", participants=table_records)


@app.route("/admin/logout")
def admin_logout():
  session.pop("admin_logged_in", None)
  return redirect(url_for("admin"))


@app.route("/admin/download")
def download_excel():
  if not session.get("admin_logged_in"):
    return redirect(url_for("admin"))

  # Always save current DataFrame first to make sure file exists and columns are correct
  df = load_participants()
  save_participants(df)

  return send_file(EXCEL_FILE, as_attachment=True)


if __name__ == "__main__":
  # Make sure file exists with correct columns when starting
  df_init = load_participants()
  save_participants(df_init)
  app.run(debug=True)

