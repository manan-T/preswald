from preswald import text, table, connect, slider, plotly
import pandas as pd
import plotly.express as px

# App Title & Description
text("# 🌍 Global Health Explorer")
text("Explore global health indicators across countries and years using filters and visualizations.")

# Connect to Preswald backend
connect()

# Load dataset (directly from file path)
try:
    df = pd.read_csv("data/world_health_data.csv")

    # Show metadata
    text(f"### ✅ Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    table(pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    }))

    # Optional: show first few rows
    text("## 🔍 Preview: First 10 Rows")
    table(df.head(10))

    # Let user select a numeric column to filter
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        # For demonstration, pick the first numeric column as default
        # Replace with a dropdown/select widget if available in your UI
        selected_col = numeric_cols[0]
        text(f"### Filtering and plotting on: `{selected_col}`")
        threshold = slider(f"Minimum `{selected_col}` Filter", 
                           min_val=float(df[selected_col].min()), 
                           max_val=float(df[selected_col].max()), 
                           default=float(df[selected_col].median()))
        filtered_df = df[df[selected_col] > threshold]

        text(f"### Filtered View: {selected_col} > {threshold}")
        table(filtered_df.head(10))

        # Scatter plot: Selected Indicator over Time by Country
        if all(col in filtered_df.columns for col in ["year", selected_col, "country"]):
            fig = px.scatter(filtered_df, x="year", y=selected_col, color="country",
                             title=f"{selected_col.replace('_', ' ').title()} Over Time")
            plotly(fig)
        else:
            text(f"⚠️ Columns `year`, `{selected_col}`, or `country` not found for plotting.")
    else:
        text("⚠️ No numeric columns found for filtering or plotting. Please check the dataset.")

except Exception as e:
    text("### ❌ Error loading or processing CSV")
    text(str(e))
