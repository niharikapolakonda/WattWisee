import streamlit as st
import pandas as pd

# -------------------------------
# 1. Page configuration
# -------------------------------
st.set_page_config(
    page_title="WattWise",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------
# 2. Application heading
# -------------------------------
st.title("⚡ WattWise")
st.subheader("Electricity Usage Detective")

st.write(
    "Upload electricity readings to analyze consumption "
    "and identify unusually high usage."
)

# -------------------------------
# 3. Upload CSV file
# -------------------------------
uploaded_file = st.file_uploader(
    "Choose your electricity readings CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Clean column headings
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
        )

        # Required columns
        required_columns = [
            "date",
            "time",
            "consumption_kwh"
        ]

        # Check for missing columns
        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            st.error(
                f"Missing columns: {missing_columns}"
            )

            st.write(
                "Columns found in your CSV:",
                list(df.columns)
            )

            st.info(
                "Required headings: date, time, consumption_kwh"
            )

            st.stop()

        # -------------------------------
        # 4. Clean the data
        # -------------------------------

        # Convert date into date format
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        # Convert time into text and remove spaces
        df["time"] = (
            df["time"]
            .astype(str)
            .str.strip()
        )

        # Convert consumption to numeric values
        df["consumption_kwh"] = pd.to_numeric(
            df["consumption_kwh"],
            errors="coerce"
        )

        # Remove invalid readings
        df = df.dropna(
            subset=[
                "date",
                "time",
                "consumption_kwh"
            ]
        )

        # Remove negative electricity readings
        df = df[
            df["consumption_kwh"] >= 0
        ]

        if df.empty:
            st.error(
                "No valid electricity readings found."
            )
            st.stop()

        # -------------------------------
        # 5. Create date and time column
        # -------------------------------

        # Combine date and time
        df["datetime"] = pd.to_datetime(
            df["date"].dt.strftime("%Y-%m-%d")
            + " "
            + df["time"],
            errors="coerce"
        )

        # Remove invalid date/time combinations
        df = df.dropna(
            subset=["datetime"]
        )

        # Sort readings by date and time
        df = df.sort_values("datetime")

        if df.empty:
            st.error(
                "No valid date and time readings found."
            )
            st.stop()

        # -------------------------------
        # 6. Display uploaded readings
        # -------------------------------
        st.subheader("Uploaded Electricity Readings")

        st.dataframe(
            df[
                [
                    "date",
                    "time",
                    "consumption_kwh"
                ]
            ],
            width="stretch"
        )

        # -------------------------------
        # 7. Calculate electricity usage
        # -------------------------------
        total_usage = df[
            "consumption_kwh"
        ].sum()

        average_usage = df[
            "consumption_kwh"
        ].mean()

        highest_usage = df[
            "consumption_kwh"
        ].max()

        # -------------------------------
        # 8. Dashboard metrics
        # -------------------------------
        st.subheader("Electricity Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Consumption",
            f"{total_usage:.2f} kWh"
        )

        col2.metric(
            "Average Reading",
            f"{average_usage:.2f} kWh"
        )

        col3.metric(
            "Highest Reading",
            f"{highest_usage:.2f} kWh"
        )

        # -------------------------------
        # 9. Electricity usage chart
        # -------------------------------
        st.subheader("Electricity Usage Over Time")

        chart_df = df.set_index("datetime")

        st.line_chart(
            chart_df["consumption_kwh"]
        )

        # -------------------------------
        # 10. Unusual usage detection
        # -------------------------------
        st.subheader("Unusual Electricity Usage Alerts")

        # Set alert threshold to 1.5 times average
        threshold = average_usage * 1.5

        st.write(
            f"Alert threshold: {threshold:.2f} kWh"
        )

        # Find readings above threshold
        unusual_readings = df[
            df["consumption_kwh"] > threshold
        ]

        if not unusual_readings.empty:

            st.warning(
                "Unusually high electricity consumption detected!"
            )

            st.dataframe(
                unusual_readings[
                    [
                        "date",
                        "time",
                        "consumption_kwh"
                    ]
                ],
                width="stretch"
            )

        else:
            st.success(
                "No unusually high readings detected."
            )

    except Exception as error:
        st.error(
            f"An error occurred while processing the file: {error}"
        )

else:
    st.info(
        "Upload Electricity_readings.csv to start "
        "analyzing electricity consumption."
    )