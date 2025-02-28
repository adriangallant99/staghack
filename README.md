# Staghack Project

## Description
This project is designed to analyze and visualize data related to deer population and their habitats. It uses various data science libraries to process and present the data in a meaningful way. The goal is to build an algorithm that minimizes the time between the registration of a patient to a portal and the time of the first appointment with a healthcare provider.

## Getting Started

### Prerequisites
Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/adriangallant99/staghack.git
    cd staghack
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the required libraries:**
    ```bash
    pip install pandas numpy matplotlib pytest
    ```

### Running the Project
To run the project, execute the main script:
```bash
python src/main.py
```

## Usage
To use this project, follow these steps:
1. Ensure your data files are in the `data` directory.
2. Run the main script to process and visualize the data.
3. View the generated plots and analysis results in the `data/output` directory.

## Project Structure
```
staghack/
├── __pycache__/
├── .gitignore
├── .vscode/
│   └── launch.json
├── data/
│   ├── Appointment Data.csv
│   ├── New Patient Data.csv
│   ├── original_data/
│   ├── output/
│   ├── pattern_map.json
│   ├── Provider Schedule Data.csv
│   └── Provider State Data.csv
├── docs/
│   ├── HACKATHON_README.md
│   ├── items_2_3/
│   ├── items_4_5/
│   └── items_6/
├── playground/
│   └── adrian-test.ipynb
├── README.md
├── src/
│   ├── __init__.py
│   ├── analysis/
│   ├── preprocessing/
│   ├── scheduling/
│   ├── util/
│   └── main.py
└── tests/
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License
None

## Contact
For any questions or issues, please contact the project maintainer at [adriangallant99@gmail.com].
