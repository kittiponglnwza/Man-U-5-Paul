# Football AI — Nexus Engine v9.0

ระบบวิเคราะห์และทำนายผลฟุตบอล Premier League ด้วย Machine Learning + Neural Networks
รันด้วย Streamlit · Python 3.10+

---

# 🗂 Dataset

## แหล่งข้อมูล

ใช้ข้อมูลการแข่งขันย้อนหลังของ Premier League ฤดูกาล:

```
data/
 ├── season 2020.csv
 ├── season 2021.csv
 ├── season 2022.csv
 ├── season 2023.csv
 ├── season 2024.csv
 └── season 2025.csv
```

แต่ละฤดูกาลมีประมาณ 380 แมตช์
รวมข้อมูลฝึกสอนมากกว่า ~2,000 แมตช์

---

## โครงสร้างข้อมูลดิบ

ตัวอย่างคอลัมน์หลัก:

* HomeTeam / AwayTeam
* FTHG / FTAG (Full Time Goals)
* Shots / Shots on Target
* Possession
* Match Date

---

## Feature Engineering (src/features.py)

ระบบสร้างฟีเจอร์ขั้นสูง เช่น:

* Rolling goals (3–5 นัดล่าสุด)
* Rolling points average
* Home / Away strength split
* Goal difference momentum
* Form-based signals
* Expected goal proxy (xG-like features)

ทุกฟีเจอร์ถูกสร้างแบบ time-safe
ไม่มีข้อมูลอนาคต (No Data Leakage)

---

# 🤖 Model Architecture

ระบบใช้ Hybrid / Ensemble Architecture

---

## 1️⃣ Core Machine Learning Engine

โมเดลหลัก:

* LightGBM / Gradient Boosting

### Two-Stage Model Structure

Stage 1 → ทำนาย: Draw vs Not Draw
Stage 2 → ถ้า Not Draw → ทำนาย: Home Win vs Away Win

เหตุผล:

* ผล "เสมอ" เป็นคลาสที่ทายยาก
* การแยก stage ช่วยเพิ่ม Recall และเสถียรภาพของโมเดล

---

## 2️⃣ Goal Model (Poisson Regression)

ใช้ Poisson Regressor เพื่อคำนวณ:

* λ_home (Expected Home Goals)
* λ_away (Expected Away Goals)

จากนั้นสร้าง:

* Scoreline Probability Matrix
* Over/Under Probability
* Win probability จากการรวมความน่าจะเป็นของสกอร์

---

## 3️⃣ Neural Network Boost (MLPClassifier)

ใช้ Multi-Layer Perceptron 2 เวอร์ชัน:

* Hidden Layers (128, 64)
* Hidden Layers (256, 128, 64)

NN ไม่ได้ใช้เดี่ยว ๆ
แต่ใช้ "Blending" รวมความน่าจะเป็นกับ LightGBM

ข้อดี:

* จับ nonlinear pattern ลึก ๆ
* เพิ่มความเสถียรของ F1-score
* ลด overfitting บางกรณี

---

## 4️⃣ Class Imbalance Handling

ใช้ SMOTE เพื่อแก้ปัญหา Draw มีจำนวนน้อย

---

## 5️⃣ Probability Calibration

ใช้ CalibratedClassifierCV (Isotonic)

เพื่อให้เปอร์เซ็นต์ความน่าจะเป็นมีความสมจริงมากขึ้น

---

# 📊 Evaluation Strategy

* Rolling-Origin Backtest (2020 → 2025)
* Accuracy
* Macro F1-Score
* Confusion Matrix
* ROI Simulation
* Monte Carlo Season Simulation

ประเมินแบบ forward-time เท่านั้น

---

# 🧠 System Identity

FOOTBALL AI v9.0 คือ Football Analytics Engine ที่รวม:

* Advanced Feature Engineering
* Hybrid ML + Neural Network
* Statistical Goal Modeling
* Time-Aware Validation
* Simulation & Backtesting

ระดับความเข้มข้น: Academic / Junior Data Scientist Level

---

# 🚀 Run

ติดตั้ง dependencies:

```
pip install -r requirements.txt
```

รัน Streamlit:

```
python -m streamlit run ui/app_ui.py
```

เทรน pipeline:

```
python -m pipelines.train_pipeline
```
