# OinkSaver
Oink Saver is a simple and engaging financial management tool designed to help individuals effectively manage their income, expenses, and savings. Built with Python using Tkinter and Matplotlib, this GUI application offers a user-friendly interface and intuitive data visualization to make financial management accessible and straightforward for everyone.

## Features
- Track Income, Expenses, and Savings: Add and manage transactions under distinct categories.
- Pie Chart Visualization: Get a visual overview of your income, expenses, and savings using dynamic pie charts created with Matplotlib.
- Log Editing and Deletion: Edit or delete transaction entries with ease for precise financial tracking.
- User-Friendly Tabs: Distinct tabs for income, expenses, and savings to simplify data input.
- Persistent Data: Save all financial records in a JSON file for easy data management and retrieval.

## Getting Started
**Prerequisites**

- Python 3.6+
- Required Libraries: Tkinter, Matplotlib
To install the necessary libraries, run:
```bash
pip install matplotlib
```
Tkinter is included in standard Python installations, so no additional installation is usually required.

## Installation
1. Clone this repository:
```
git clone https://github.com/username/oink-saver.git
```
2. Navigate to the project directory:
```
cd oink-saver
```
3. Run the application:
```
python main.py
```

## Usage

- Adding Transactions: Use the Income, Expense, or Savings tab to add your financial entries. Enter the relevant details, such as date, amount, and notes, and press "Submit".
- Editing or Deleting Transactions: Select a transaction from the log and click the "Edit" or "Delete" button.
- Viewing Insights: The pie chart on the right dynamically updates to reflect your current financial state.

## Project Structure
- main.py: The main application script containing the GUI and functionality.
- data.json: Stores all financial transaction data persistently.
- logo.png: The logo displayed in the application.

## Technologies Used
- Python: The programming language used for this project.
- Tkinter: A Python library for creating the GUI.
- Matplotlib: A library used to create pie charts for visual representation of financial data.
- JSON: Used for storing transaction data in a lightweight format.

## Future Enhancements
- Advanced Analytics: Implement predictive analytics to help users forecast expenses and income.
- Cloud Integration: Integrate with cloud platforms for data backup and multi-device support.
- User Authentication: Add user login to enable secure and personalized usage.

## Contributing
Contributions are welcome! If you have ideas to improve Oink Saver or want to fix any issues, feel free to submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Inspiration from popular budgeting apps like Mint and YNAB.
