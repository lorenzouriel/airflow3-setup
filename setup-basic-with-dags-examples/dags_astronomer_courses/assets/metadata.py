from airflow.sdk import Asset, Metadata, task

my_asset = Asset("my_asset")

@task(outlets=[my_asset])
def attach_extra_using_metadata():
    num = 42
    yield Metadata(my_asset, {"answer": num})

    return "Hello, World!"

attach_extra_using_metadata() 