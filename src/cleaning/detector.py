import pandas as pd
import numpy as np
from typing import Dict, Any

def analyze_issues(df: pd.DataFrame) -> Dict[str, Any]:
    issues = {}
    # Missing values
    missing = df.isnull().sum()
    issues['missing_values'] = missing[missing > 0].to_dict()
    # Duplicates
    issues['duplicate_rows'] = int(df.duplicated().sum())
    # Data type inconsistencies
    type_issues = {}
    for col in df.columns:
        types = df[col].map(type).value_counts()
        if len(types) > 1:
            type_issues[col] = {str(k): int(v) for k, v in types.items()}
    issues['type_inconsistencies'] = type_issues
    # Outliers (using IQR for numeric columns)
    outliers = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
        if outlier_count > 0:
            outliers[col] = int(outlier_count)
    issues['outliers'] = outliers

    # Constant columns (zero variance)
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) == 1]
    issues['constant_columns'] = constant_cols

    # High cardinality columns (arbitrary threshold: >50 unique values or >20% of rows)
    high_cardinality = [col for col in df.columns if df[col].nunique() > max(50, 0.2*len(df))]
    issues['high_cardinality_columns'] = high_cardinality

    # Columns with a single unique value
    single_unique = [col for col in df.columns if df[col].nunique() == 1]
    issues['single_unique_columns'] = single_unique

    # Columns with mixed data types (object columns)
    mixed_types = {}
    for col in df.select_dtypes(include=['object']).columns:
        types = df[col].map(type).value_counts()
        if len(types) > 1:
            mixed_types[col] = {str(k): int(v) for k, v in types.items()}
    issues['mixed_type_object_columns'] = mixed_types

    # Columns with high percentage of missing values (>50%)
    high_missing = [col for col in df.columns if (df[col].isnull().mean() > 0.5)]
    issues['high_missing_pct_columns'] = high_missing

    # Highly imbalanced categorical columns (top value >95% of non-null values)
    imbalanced = {}
    for col in df.select_dtypes(include=['object', 'category']).columns:
        top_freq = df[col].value_counts(normalize=True, dropna=True).max() if not df[col].dropna().empty else 0
        if top_freq > 0.95:
            imbalanced[col] = float(top_freq)
    issues['highly_imbalanced_categoricals'] = imbalanced

    # Columns with all zeros
    all_zeros = [col for col in df.columns if (df[col] == 0).all()]
    issues['all_zero_columns'] = all_zeros

    # Columns with all same string
    all_same_str = [col for col in df.select_dtypes(include=['object']).columns if df[col].nunique() == 1]
    issues['all_same_string_columns'] = all_same_str

    # Columns with potential date/time parsing issues
    date_parse_issues = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col], errors='raise')
            except Exception:
                date_parse_issues.append(col)
    issues['potential_datetime_parse_issues'] = date_parse_issues

    return issues
