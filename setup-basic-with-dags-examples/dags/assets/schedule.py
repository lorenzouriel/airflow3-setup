from airflow.sdk import Asset, dag

@dag(
    schedule=(
        Asset("asset1") | Asset("asset2") | Asset("asset3") | Asset("asset4")
    ),

    # schedule=(
    #     (Asset("asset1") | Asset("asset2")) & (Asset("asset3") | Asset("asset4"))
    # ),
)
def downstream_dag():
    pass

downstream_dag()