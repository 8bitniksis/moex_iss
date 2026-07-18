import pandas as pd

from moex_iss.clients.client import ISSClient
from moex_iss.dataframe.query import Query


def merge_marketdata_yields(bonds_df: pd.DataFrame, client: ISSClient) -> pd.DataFrame:
    """
    Fetches marketdata_yields for securities in bonds_df and merges them.

    Args:
        bonds_df: DataFrame from client.services.bond.df()
        client: ISSClient instance

    Returns:
        DataFrame merged with marketdata_yields data.
    """
    if bonds_df.empty:
        return bonds_df

    # Получаем список SECID из текущего DataFrame
    secids = bonds_df['SECID'].dropna().unique().tolist()
    if not secids:
        return bonds_df

    all_yields_data = []
    for secid in secids:
        # Получаем данные по одному инструменту (можно оптимизировать для батчинга, если API позволяет)
        # Используем endpoint.bond, так как yields там обычно
        url = client.endpoint.bond(security=secid)
        raw_data = client.get_json(url)

        # Извлекаем блок marketdata_yields
        yld_block = raw_data.get("marketdata_yields", {})
        yld_data = yld_block.get("data", [])
        yld_columns = yld_block.get("columns", [])

        if yld_data and yld_columns:
            # Создаём DataFrame для данного инструмента
            yld_df = pd.DataFrame(data=yld_data, columns=yld_columns)
            # Оставляем только нужные колонки, чтобы избежать конфликта (например, 'SECID', 'BOARDID')
            # или переименовываем их, если есть пересечение
            # Предположим, нас интересуют EFFECTIVEYIELD, DURATION, ZSPREADBP
            relevant_cols = [col for col in ['SECID', 'EFFECTIVEYIELD', 'DURATION', 'ZSPREADBP'] if col in yld_df.columns]
            yld_df_subset = yld_df[relevant_cols].copy()
            
            # Убираем дубликаты, если таковые имеются (маловероятно для snapshot)
            yld_df_subset.drop_duplicates(subset=['SECID'], keep='first', inplace=True)
            
            all_yields_data.append(yld_df_subset)

    if not all_yields_data:
        # Если не удалось получить ни одного блока yields, возвращаем исходный df
        print("Warning: Could not fetch any marketdata_yields data.")
        return bonds_df

    # Объединяем все yields DataFrame'ы
    combined_yields_df = pd.concat(all_yields_data, ignore_index=True)

    # Объединяем с исходным bonds_df по 'SECID'
    # Используем left join, чтобы сохранить все строки из bonds_df
    merged_df = pd.merge(bonds_df, combined_yields_df, on='SECID', how='left')

    return merged_df

def main():
    client = ISSClient()

    # Return dataFram of all bonds
    # df = client.services.bond.df()
    # print(df.head())
    # print(df.columns)

    # Return individual bond by SECID
    # bond_details = client.services.bond.details("RU000A10AHU1")
    # print(bond_details)

    # bond = client.services.bond.snapshot("RU000A10AHU1")
    # print(bond)

    # print(bond['SHORTNAME'])
    # print(bond['MATDATE'])
    # print(bond['EFFECTIVEYIELD'])
    # print(bond['DURATION'])
    # print(bond['ZSPREADBP'])

    #============================================================#
    # Advanced logic for df
    #============================================================#

    # Get DataFrame of all bonds
    df = client.services.bond.df()
    print("Initial DataFrame shape:", df.shape)
    print("Initial DataFrame columns:", df.columns.tolist())
    print(df.head())

    # Merge with marketdata_yields
    df_with_yields = merge_marketdata_yields(df, client)
    print("\nDataFrame after merging with yields shape:", df_with_yields.shape)
    print("DataFrame after merging with yields columns:", df_with_yields.columns.tolist())
    print(df_with_yields.head())

    # Now apply the Query with the required columns
    # Note: Ensure 'EFFECTIVEYIELD', 'DURATION', 'ZSPREADBP' are now available in df_with_yields
    required_columns = ['SHORTNAME', 'YIELD', 'LAST', 'EFFECTIVEYIELD', 'DURATION', 'STATUS', 'MATDATE', 'NEXTCOUPON', 'ACCRUEDINT']
    
    # Check if all required columns are present
    missing_cols = [col for col in required_columns if col not in df_with_yields.columns]
    if missing_cols:
        print(f"\nWarning: Some required columns are missing in the DataFrame: {missing_cols}")
        # Filter to only existing columns for the query
        existing_cols = [col for col in required_columns if col in df_with_yields.columns]
        print(f"Proceeding with existing columns: {existing_cols}")
        if not existing_cols:
             print("No required columns are available. Cannot proceed with selection.")
             return
        query_cols = existing_cols
    else:
        query_cols = required_columns

    result = (
        Query(df_with_yields)
            .where("LISTLEVEL <= 3") # Применяем фильтр
            .take(30)                 # Ограничиваем количество строк
            .select(*query_cols)      # Выбираем нужные колонки
            .to_df()                  # Возвращаем результат как DataFrame
    )

    print("\nFinal Result:")
    print(result)


if __name__ == "__main__":
    main()