from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os


def aggregate_financial_data(
        file_path: str,
        exclude_income_cols: Optional[list[str]] = None,
        exclude_expense_cols: Optional[list[str]] = None
) -> pd.DataFrame:
    """
    Reads and aggregates financial data from an Excel file.

    Args:
        file_path (str): Path to the Excel file.
        exclude_income_cols (List[str], optional): Income category columns to exclude.
        exclude_expense_cols (List[str], optional): Expense category columns to exclude.

    Returns:
        pd.DataFrame: Monthly aggregated financial data with 'Income', 'Expense', and 'Savings' columns indexed by month.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    exclude_income_cols = exclude_income_cols or []
    exclude_expense_cols = exclude_expense_cols or []

    # Read the Excel file (all sheets)
    xls = pd.ExcelFile(file_path)
    all_data = []

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=[0, 1])
        df = df.iloc[1:]  # Drop header and 'Previous savings' rows

        # Flatten the multi-level columns
        df.columns = [' '.join(str(s).strip() for s in col if str(s) != 'nan') for col in df.columns]

        # Identify columns
        date_col = [col for col in df.columns if 'Date' in col][0]
        income_sum_col = [col for col in df.columns if 'Incomes sum' in col][0]
        expense_sum_col = [col for col in df.columns if 'Expenses sum' in col][0]
        savings_col = [col for col in df.columns if 'Savings' in col][0]

        # Convert to numeric
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df[income_sum_col] = pd.to_numeric(df[income_sum_col], errors='coerce')
        df[expense_sum_col] = pd.to_numeric(df[expense_sum_col], errors='coerce')
        df[savings_col] = pd.to_numeric(df[savings_col], errors='coerce')

        for col in exclude_income_cols:
            col = f"Incomes {col}"
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[income_sum_col] = df[income_sum_col] - df[col].fillna(0)

        for col in exclude_expense_cols:
            col = f"Expenses {col}"
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[expense_sum_col] = df[expense_sum_col] - df[col].fillna(0)

        df = df[[date_col, income_sum_col, expense_sum_col, savings_col]].dropna(subset=[date_col])
        df = df.rename(columns={
            date_col: 'Date',
            income_sum_col: 'Income',
            expense_sum_col: 'Expense',
            savings_col: 'Savings'
        })

        all_data.append(df)

    full_data = pd.concat(all_data)
    full_data = full_data.dropna(subset=['Date'])
    full_data.set_index('Date', inplace=True)

    monthly_data = full_data.resample('ME').agg({
        'Income': 'sum',
        'Expense': 'sum',
        'Savings': 'last'  # Already aggregated in the source
    })

    return monthly_data


def plot_financial_summary(monthly_data: pd.DataFrame) -> None:
    """
    Plots a financial summary from aggregated monthly data (assumed to be in currency units, e.g., RUB or USD).

    Interprets all values as being in millions.
    
    Args:
        monthly_data (pd.DataFrame): A DataFrame indexed by month with 'Income', 'Expense', and 'Savings' columns.
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(monthly_data.index, monthly_data['Income'], color='green', label='Monthly Income')
    ax1.plot(monthly_data.index, monthly_data['Expense'], color='red', label='Monthly Expense')

    ax2 = ax1.twinx()
    ax2.bar(monthly_data.index, monthly_data['Savings'], width=20, alpha=0.5, color='blue', label='Monthly Savings')

    ax1.set_xlabel('Time line')
    ax1.set_ylabel('Income / Expense')
    ax2.set_ylabel('Savings')
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    fig.autofmt_xdate()

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title('Monthly Financial Overview')
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# All
# data = aggregate_financial_data("D:\\GoogleDisk\\Money-management\\xls-backups\\2025_04_12\\Главный_RUB_20250412_131419.xlsx")
# plot_financial_summary(data)

# Investment excluded
# data = aggregate_financial_data(
#     "D:\\GoogleDisk\\Money-management\\xls-backups\\2025_05_08\\Главный_RUB_20250508_183425.xlsx",
#     exclude_income_cols=["Инвестиции"],
#     exclude_expense_cols=["Инвестиции"]
# )
# plot_financial_summary(data)

# Only Investment
# data = aggregate_financial_data(
#     "D:\\GoogleDisk\\Money-management\\xls-backups\\2025_04_12\\Главный_RUB_20250412_131419.xlsx",
#     exclude_income_cols=[
#         "Другое",
#         "ЗП Нелли",
#         "ЗП Руслан"
#     ],
#     exclude_expense_cols=[
#         "Валюта",
#         "Дети",
#         "Другое",
#         "Ежемесячные",
#         "Ипотека/Недвижимость",
#         "Кредиты и долги",
#         "Образование",
#         "Отдых",
#         "Подарки",
#         "Ремонт (материалы)",
#         "Ремонт (мебель/техн.)",
#         "Ремонт (работа)"
#     ]
# )
# plot_financial_summary(data)
