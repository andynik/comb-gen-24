import pandas as pd

# Add "prism" and "prisms" to geometry-related keywords
geometry_keywords = [
    "triangle", "circle", "square", "rectangle", "geometry",
    "angle", "perimeter", "area", "radius", "diameter",
    "arc", "circumference", "parallel", "segment", "chord",
    "polygon", "volume", "surface area", "isometry", "prism", "prisms"
]

# Function to check for geometry-related terms in the "problem" column
def contains_geometry_terms(row):
    problem_text = str(row['problem']).lower()
    return any(keyword in problem_text for keyword in geometry_keywords)

# Load the Parquet file
file_path = 'combinatorics3.parquet'
df = pd.read_parquet(file_path)

# Filter out the geometry-related problems
non_geometry_df = df[~df.apply(lambda row: contains_geometry_terms(row), axis=1)]

# Save the filtered DataFrame to a new Parquet file
output_parquet_path = 'filtered_combinatorics3.parquet'
non_geometry_df.to_parquet(output_parquet_path)

# Save the filtered DataFrame to a JSON file
output_json_path = 'filtered_combinatorics3.json'
non_geometry_df.to_json(output_json_path, orient='records', lines=True)

# Report the number of filtered problems
filtered_count = len(non_geometry_df)
print(f"Filtered geometry-related problems: {filtered_count}")
print(f"Filtered data saved to {output_parquet_path} and {output_json_path}")