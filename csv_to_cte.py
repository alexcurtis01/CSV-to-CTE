import pandas as pd

def csv_to_cte(file_path, cte_name):
    df = pd.read_csv(file_path)

    # Remove any single quotes that would disrupt SQL query
    df.columns = [col.replace("'", "''") for col in df.columns]
    df = df.applymap(lambda x: str(x).replace("'", "''"))

    cte_query = f"WITH {cte_name} AS (\n"

    # Iterate over the rows of the df to generate each SELECT statement
    for i, row in df.iterrows():
        select_statement = "    SELECT " + ", ".join([f"'{row[col]}' AS [{col}]" for col in df.columns])

        # Append UNION ALL if not the last row
        if i < len(df) - 1:
            select_statement += " UNION ALL"

        # Add the SELECT statement to the CTE query
        cte_query += select_statement + "\n"

    # Close the CTE query
    cte_query += ")"

    # Save the CTE query to txt file
    with open("CTE.txt", 'w') as file:
        file.write(cte_query)

csv_to_cte("MemberList.csv", "MemberList")