import os
import re
import time
import numpy as np
import pandas as pd

INPUT_PATH = r'D:\Semester 2\Applied Computer Science\Question 9\weather_data.xls'
OUTPUT_PATH = r'D:\Semester 2\Applied Computer Science\Question 9\weather_data_cleaned.xlsx'
MONTH_COL_NAME = '1999'
INVALID_SENTINELS = {-9999}
NOISE_THRESHOLD = 0.001
MONTHS_FULL = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]
MONTH_RE = re.compile(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', re.I)

def looks_like_month(val):
    if pd.isna(val):
        return False
    s = str(val).strip()
    if not s:
        return False
    if MONTH_RE.match(s):
        return True
    if s.isdigit():
        try:
            v = int(s)
            return 1 <= v <= 12
        except Exception:
            return False
    return False

def normalize_month_label(val):
    if pd.isna(val):
        return val
    s = str(val).strip()
    if not s:
        return s
    corrections = {
        'fenruary': 'February',
        'febuary': 'February',
        'februray': 'February',
        'janurary': 'January'
    }
    low = s.lower()
    if low in corrections:
        return corrections[low]
    if s.isdigit():
        mapping = {str(i): MONTHS_FULL[i-1] for i in range(1,13)}
        return mapping.get(s, s)
    s_low = s.lower()
    for full in MONTHS_FULL:
        if s_low.startswith(full[:3].lower()):
            return full
    for full in MONTHS_FULL:
        if full[:3].lower() in s_low:
            return full
    return s

def safe_save_excel(df_cleaned, monthly_totals, yearly_total, average_monthly, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
            df_cleaned.to_excel(writer, sheet_name='Cleaned_Data', index=True)
            summary = pd.DataFrame({'Monthly Total': monthly_totals})
            summary.loc['Yearly Total'] = yearly_total
            summary.loc['Average Monthly'] = average_monthly
            summary.to_excel(writer, sheet_name='Summary', index=True)
        return out_path
    except PermissionError:
        base, ext = os.path.splitext(out_path)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        alt_path = f"{base}_v{timestamp}{ext}"
        with pd.ExcelWriter(alt_path, engine='openpyxl') as writer:
            df_cleaned.to_excel(writer, sheet_name='Cleaned_Data', index=True)
            summary = pd.DataFrame({'Monthly Total': monthly_totals})
            summary.loc['Yearly Total'] = yearly_total
            summary.loc['Average Monthly'] = average_monthly
            summary.to_excel(writer, sheet_name='Summary', index=True)
        return alt_path

def row_contains_valid_numeric(row, exclude_col):
    for col in row.index:
        if col == exclude_col:
            continue
        val = row[col]
        try:
            num = float(val)
        except Exception:
            continue
        if np.isfinite(num) and (num not in INVALID_SENTINELS):
            return True
    return False

def main():
    raw = pd.read_excel(INPUT_PATH, sheet_name=0, header=0, dtype=object)
    first_col = raw.columns[0]
    if first_col != MONTH_COL_NAME:
        raw = raw.rename(columns={first_col: MONTH_COL_NAME})
    raw[MONTH_COL_NAME] = raw[MONTH_COL_NAME].replace(r'^\s*$', np.nan, regex=True)
    raw[MONTH_COL_NAME] = raw[MONTH_COL_NAME].ffill()
    raw = raw.dropna(how='all')
    keep_flags = []
    for _, row in raw.iterrows():
        month_cell = row.get(MONTH_COL_NAME, None)
        if looks_like_month(month_cell):
            keep_flags.append(True)
            continue
        if row_contains_valid_numeric(row, MONTH_COL_NAME):
            keep_flags.append(True)
            continue
        keep_flags.append(False)
    kept = raw[pd.Series(keep_flags, index=raw.index)].copy()
    if kept.empty:
        raise RuntimeError("No candidate month rows found after filtering. Inspect the input file.")
    kept[MONTH_COL_NAME] = kept[MONTH_COL_NAME].apply(normalize_month_label)
    kept = kept.set_index(MONTH_COL_NAME)
    numeric = kept.apply(pd.to_numeric, errors='coerce')
    for s in INVALID_SENTINELS:
        numeric = numeric.replace(s, np.nan)
    numeric = numeric.where(numeric >= 0, np.nan)
    numeric = numeric.mask(numeric.abs() < NOISE_THRESHOLD, 0.0)
    numeric = numeric.fillna(0.0)
    new_cols = []
    for i, col in enumerate(numeric.columns, start=1):
        cs = str(col).strip()
        if (cs == '') or cs.lower().startswith('unnamed') or (not re.search(r'\d', cs) and not cs.lower().startswith('day')):
            new_cols.append(f'Day {i}')
        else:
            new_cols.append(cs)
    numeric.columns = new_cols
    numeric_agg = numeric.groupby(numeric.index).sum()
    numeric_full = numeric_agg.reindex(MONTHS_FULL, fill_value=0.0)
    monthly_totals = numeric_full.sum(axis=1)
    yearly_total = monthly_totals.sum()
    average_yearly = monthly_totals.mean()
    if numeric_full.values.size == 0 or numeric_full.values.max() == 0:
        max_precip = 0.0
        max_positions = []
    else:
        max_precip = numeric_full.values.max()
        pos = np.where(numeric_full.values == max_precip)
        rows_idx, cols_idx = pos
        max_positions = [(numeric_full.index[r], numeric_full.columns[c]) for r, c in zip(rows_idx, cols_idx)]
    saved_path = safe_save_excel(numeric_full, monthly_totals, yearly_total, average_yearly, OUTPUT_PATH)
    print("\n--- Total precipitation in each month ---")
    print(monthly_totals.to_string())
    print(f"\nTotal precipitation for the year: {yearly_total}")
    if max_positions:
        print(f"\nMaximum single-day precipitation value: {max_precip}")
        print("All month/day occurrences with that maximum:")
        for m, d in max_positions:
            print(f" - {m}, {d}")
    else:
        print("\nMonth/day with maximum precipitation: None (all zeros)")
    print(f"\nAverage yearly precipitation (mean of monthly totals): {average_yearly}")
    print(f"\nCleaned file written to: {saved_path}")

if __name__ == '__main__':
    main()
