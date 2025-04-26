import pandas as pd

def main():
    # Load the dataset from the .parquet file
    # df = pd.read_parquet('combinatorics4_final_test_1000.parquet')
    df = pd.read_parquet('dataset_5583/combinatorics_5583_final.parquet')

    # Define the columns of interest
    columns_of_interest = ['problem', 'fictional', 'adversarial', 'contdis']

    # Calculate the average size (length) for each column of interest and round to the nearest integer
    average_sizes = {col: round(df[col].apply(lambda x: len(str(x))).mean()) for col in columns_of_interest}

    # Define a mapping from column names to their LaTeX-friendly names
    column_names = {
        'problem': 'Original',
        'fictional': 'Fictional',
        'adversarial': 'Adversarial',
        'contdis': 'Contextual disguise'
    }

    # Construct the LaTeX table
    latex_table = r"""
    \begin{table*}[h!]
        \centering
        \begin{tabular}{|l|c|}
        \hline
        Version & Average Size \\
        \hline
    """

    for col in columns_of_interest:
        latex_table += f"        {column_names[col]} & {average_sizes[col]} \\\\ \n"

    latex_table += r"""        \hline
        \end{tabular}
        \caption{Average length of the problem versions.}
        \label{tab:var_len}
    \end{table*}
    """

    # Print the LaTeX table
    print(latex_table)

if __name__ == '__main__':
    main()