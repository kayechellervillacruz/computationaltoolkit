
<img width="1787" height="820" alt="image" src="https://github.com/user-attachments/assets/57d5aa40-7054-4526-93df-925596ae8cf7" />


# Computational Science Toolkit

The **Computational Science Toolkit** is a modern, responsive web application designed to streamline the exploration and execution of numerical methods. Built with Streamlit, this tool serves as a professional-grade interface for students and researchers to perform complex mathematical computations with ease.

This project prioritizes clean architecture and a modern "dark-mode" desktop experience, allowing users to focus on computational results rather than interface navigation.

---

## Features

The toolkit is organized into three primary modules, each housing robust numerical algorithms:

### 1. Single Variable Equations

Solve for the roots of equations with high precision using established numerical methods:

* **Bisection Method:** Reliable interval-based root finding.
* **Linear Interpolation:** Efficient approximation using linear segments.
* **Method of Secants:** Fast convergence without requiring derivative calculations.
* **Newton's Method:** Rapid, high-order convergence using function derivatives.

### 2. System of Linear Equations

Handle matrix operations and complex system solving:

* **Matrix Algebra:** Perform Addition, Subtraction, and Multiplication on dynamically scaled matrices.
* **Gaussian Elimination:** Solve square systems of linear equations using partial pivoting and back substitution.

### 3. Approximations & Data Analysis

Process coordinate data and analyze patterns:

* **Least Squares Approximation:** Fit polynomial curves to coordinate data sets.
* **Cubic Splines:** Perform piece-wise polynomial interpolation.
* **Principal Component Analysis (PCA):** Analyze data dimensionality and extract principal components.

---

##  Tech Stack

* **UI Framework:** [Streamlit](https://streamlit.io/)
* **Numerical Computation:** [NumPy](https://numpy.org/), [SciPy](https://scipy.org/)
* **Symbolic Math:** [SymPy](https://www.sympy.org/)
* **Data Handling:** [Pandas](https://pandas.pydata.org/)

---

##  Project Structure

The project follows a modular architecture to ensure maintainability and separation of concerns:

```text
ComputationalToolkit/
├── app.py             # Main routing and application entry point
├── requirements.txt   # Dependency list
├── style.css          # Custom dark-themed CSS and UI styling
├── utils.py           # Shared helper functions (formatting, UI renderers)
├── assets/            # Branding and visual assets
└── modules/           # Mathematical algorithm modules
    ├── bisection.py
    ├── gaussian.py
    ├── interpolation.py
    ├── least_squares.py
    ├── matrix.py
    ├── newton.py
    ├── pca.py
    ├── secant.py
    └── spline.py

```

---

##  Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/computational-toolkit.git
cd ComputationalToolkit

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the application:**
```bash
streamlit run app.py

```



---

##  Design Philosophy

This toolkit was built to resemble professional desktop engineering software. It features:

* **Dark-themed UI** with high-contrast elements for reduced eye strain.
* **Responsive Layout** optimized for desktop and tablet usage.
* **Modular Component Architecture** allowing for easy additions of new mathematical methods without cluttering the main logic.
