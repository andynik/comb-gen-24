import pandas as pd

# Load the Parquet file
df = pd.read_parquet('combinatorics4.parquet')

# Group by the 'source' column and count the number of problems per source
problem_summary = df['source'].value_counts()

# Calculate the total number of problems
total_problems = problem_summary.sum()

# Print the result
print(problem_summary)

# Prepare the LaTeX table
table_header = r"""
\begin{table}[h]
    \centering
    \begin{tabular}{|l|r|}
        \hline
        Source & Number of Samples \\
        \hline
"""

table_footer = r"""
        \hline
        \textbf{Total} & \textbf{%s} \\
        \hline
    \end{tabular}
    \caption{Breakdown of the dataset sources.}
    \label{tab:dataset_sources}
\end{table}
""" % f"{total_problems:,}"

# Create the table body from the problem summary
table_body = "\n".join(
    f"        {source} & {count:,} \\\\" for source, count in problem_summary.items()
)

# Combine header, body, and footer
latex_table = table_header + table_body + table_footer

# Print the LaTeX table
print(latex_table)