import hydra
import pandas as pd
from hydra.utils import to_absolute_path as abspath
from omegaconf import DictConfig
from patsy import dmatrices
from sklearn.model_selection import train_test_split


def get_data(raw_path: str):
    data = pd.read_csv(raw_path)
    print(f"Data loaded from {raw_path}")
    return data


def get_features(target: str, features: list, data: pd.DataFrame):
    feature_str = " + ".join(features)
    y, X = dmatrices(
        f"{target} ~ {feature_str} - 1", data=data, return_type="dataframe"
    )
    print(f"Features and target extracted: {feature_str}")
    return y, X


def rename_columns(X):
    # Correctly escape the square brackets to ensure they're treated as literal characters in the regex
    X.columns = X.columns.str.replace(r"\[", "_", regex=True).str.replace(
        r"\]", "", regex=True
    )
    print(f"Columns renamed: {X.columns}")
    return X


@hydra.main(config_path="../../config", config_name="main")
def process_data(config: DictConfig):
    """Function to process the data"""

    print("Starting data processing...")
    data = get_data(abspath(config.raw.path))

    y, X = get_features(config.process.target, config.process.features, data)

    X = rename_columns(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7
    )

    # Save data
    X_train.to_csv(abspath(config.processed.X_train.path), index=False)
    X_test.to_csv(abspath(config.processed.X_test.path), index=False)
    y_train.to_csv(abspath(config.processed.y_train.path), index=False)
    y_test.to_csv(abspath(config.processed.y_test.path), index=False)
    print("Data processing completed and saved.")


if __name__ == "__main__":
    process_data()
