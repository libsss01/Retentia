from pathlib import Path
from Retentia.tools import write_to_file

def file_setup():
    # filename variables
    json_file = "storage.json"
    tools_json = "tools.json"

    # Path object
    storage_file_path = Path(json_file)
    tools_file_path = Path(tools_json)

    # File contents
    storage_file_content = []
    tools_file_content = [{"lastUserId": 1}]

    # list of data
    list_of_paths = [storage_file_path, tools_file_path]
    list_of_contents = [storage_file_content, tools_file_content]
    list_of_filename = [json_file, tools_json]


    for filename, path_obj, content in zip(list_of_filename,list_of_paths, list_of_contents):
        if path_obj.exists():
            pass
        else:
            write_to_file(filename, content)

    