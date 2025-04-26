import numpy as np
import pandas as pd


# Function to perform the permutation test
def permutation_test(sample1, sample2, num_permutations=10000):
    obs_diff = np.abs(np.mean(sample1) - np.mean(sample2))
    pooled = np.hstack([sample1, sample2])
    n = len(sample1)

    count = 0
    for _ in range(num_permutations):
        np.random.shuffle(pooled)
        new_diff = np.abs(np.mean(pooled[:n]) - np.mean(pooled[n:]))
        if new_diff >= obs_diff:
            count += 1

    return count / num_permutations


# Function to generate a complete LaTeX table
def latex_table(p_values, variations):
    # Escape underscores for LaTeX
    escaped_variations = [var.replace('_', r'\_') for var in variations]

    lines = [
        r"\begin{table}[ht]",
        r"\centering",
        r"\caption{Permutation Test p-values Comparing Variations to Answer}",
        r"\begin{tabular}{|l|" + "c|" * len(escaped_variations) + r"}",
        r"\hline",
        "Variation & " + " & ".join(escaped_variations) + r" \\",
        r"\hline",
        "answer & "
    ]

    data_line = ""
    for var in variations:
        if var == 'answer':
            data_line += " & "
        else:
            p_value = p_values['answer'][var]
            significance = '*' if p_value < 0.05 else ''
            data_line += f"{p_value:.3f}{significance} & "

    data_line = data_line.rstrip(' & ') + r" \\"

    # Complete the table
    lines.extend([data_line, r"\hline", r"\end{tabular}", r"\end{table}"])

    return "\n".join(lines)


def main():
    # Load the dataset
    df = pd.read_parquet('dataset_5583/combinatorics_5583_final.parquet')
    # df = pd.read_parquet('combinatorics_5583_final.parquet')

    # Columns to compare with 'answer'
    compare_columns = ['answer', 'original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']

    # Dictionary to store p-values
    p_values = {'answer': {}}

    # Perform permutation tests with 'answer'
    for col in compare_columns[1:]:
        p_value = permutation_test(df['answer'].values, df[col].values)
        p_values['answer'][col] = p_value

    # Generate and print LaTeX table
    latex = latex_table(p_values, compare_columns[1:])
    print(latex)


if __name__ == "__main__":
    main()