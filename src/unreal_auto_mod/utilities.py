import os
import shutil
import subprocess
import time

from unreal_auto_mod import file_io, log, main_logic, unreal_engine
from unreal_auto_mod.data_structures import CompressionType, ExecutionMode, HookStateType, get_enum_from_val


def get_fmodel_path(output_directory: str) -> str:
    return os.path.join(output_directory, 'Fmodel.exe')


def install_fmodel(output_directory: str):
    download_fmodel()
    zip_path = os.path.join(get_working_dir(), 'Fmodel.zip')
    file_io.unzip_zip(zip_path, output_directory)


def install_umodel(output_directory: str):
    download_umodel()
    os.makedirs(output_directory, exist_ok=True)
    zip_path = os.path.join(get_working_dir(), 'umodel_win32.zip')
    file_io.unzip_zip(zip_path, output_directory)


def install_kismet_analyzer(output_directory: str):
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(get_working_dir(), exist_ok=True)
    download_kismet_analyzer(get_working_dir())
    zip_path = f'{get_working_dir()}/kismet-analyzer-3d06645-win-x64.zip'
    file_io.unzip_zip(zip_path, output_directory)
    shutil.move(f'{output_directory}/kismet-analyzer-3d06645-win-x64/kismet-analyzer.exe', f'{output_directory}/kismet-analyzer.exe')


def install_uasset_gui(output_directory: str):
    os.makedirs(output_directory, exist_ok=True)
    download_uasset_gui(output_directory)
    exe_path = f'{output_directory}/UAssetGUI.exe'
    shutil.move(exe_path, f'{output_directory}/UAssetGUI.exe')


def download_stove(output_directory: str):
    latest_version = get_latest_stove_version()
    if latest_version:
        url = f"https://github.com/bananaturtlesandwich/stove/releases/download/{latest_version}/stove.exe"
    else:
        url = "https://github.com/bananaturtlesandwich/stove/releases/download/0.13.1-alpha/stove.exe"

    download_path = f'{output_directory}/stove.exe'
    file_io.download_file(url, download_path)


def install_stove(output_directory: str):
    os.makedirs(output_directory, exist_ok=True)
    download_stove(output_directory)
    exe_path = f'{output_directory}/stove.exe'
    shutil.move(exe_path, f'{output_directory}/stove.exe')


def install_spaghetti(output_directory: str):
    os.makedirs(output_directory, exist_ok=True)
    download_spaghetti(output_directory)
    exe_path = f'{output_directory}/spaghetti.exe'
    shutil.move(exe_path, f'{output_directory}/spaghetti.exe')


def download_fmodel():
    url = 'https://github.com/4sval/FModel/releases/latest/download/FModel.zip'
    download_path = os.path.join(get_working_dir(), 'Fmodel.zip')
    file_io.download_file(url, download_path)


def get_umodel_path(output_directory: str) -> str:
    path = os.path.join(output_directory,'umodel_64.exe')
    return os.path.normpath(path)


def download_umodel():
    url = 'https://github.com/Mythical-Github/UEViewer/releases/download/vStatic/umodel_win32.zip'
    download_path = f'{get_working_dir()}/umodel_win32.zip'

    file_io.download_file(url, download_path)


def get_kismet_analyzer_path(output_directory: str) -> str:
    return f'{output_directory}/kismet-analyzer-3d06645-win-x64/kismet-analyzer.exe'


def download_kismet_analyzer(output_directory: str):
    url = "https://github.com/trumank/kismet-analyzer/releases/download/latest/kismet-analyzer-3d06645-win-x64.zip"
    download_path = f'{output_directory}/kismet-analyzer-3d06645-win-x64.zip'
    file_io.download_file(url, download_path)


def get_ide_path():
    return main_logic.settings_information.settings['optionals']['ide_path']


def get_blender_path():
    return main_logic.settings_information.settings['optionals']['blender_path']


def get_uasset_gui_path(output_directory: str) -> str:
    return f'{output_directory}/UAssetGUI.exe'


def download_uasset_gui(output_directory: str):
    url = "https://github.com/atenfyr/UAssetGUI/releases/latest/download/UAssetGUI.exe"
    download_path = f'{output_directory}/UAssetGUI.exe'
    file_io.download_file(url, download_path)


def does_umodel_exist(output_directory: str) -> bool:
    return os.path.isfile(get_umodel_path(output_directory))


def does_fmodel_exist() -> bool:
    return os.path.isfile(get_fmodel_path())


def does_kismet_analyzer_exist() -> bool:
    return os.path.isfile(get_kismet_analyzer_path())


def does_uasset_gui_exist() -> bool:
    return os.path.isfile(f"{get_uproject_unreal_auto_mod_resources_dir()}/UAssetGUI/UAssetGUI.exe")


def download_spaghetti(output_directory: str):
    url = 'https://github.com/bananaturtlesandwich/spaghetti/releases/latest/download/spaghetti.exe'
    download_path = f"{output_directory}/spaghetti.exe"
    file_io.download_file(url, download_path)


def get_latest_stove_version():
    import requests
    api_url = "https://api.github.com/repos/bananaturtlesandwich/stove/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        latest_release = response.json()
        return latest_release['tag_name']
    return None


def get_latest_stove_version():
    import requests
    from requests.exceptions import HTTPError, RequestException
    try:
        api_url = "https://api.github.com/repos/bananaturtlesandwich/stove/releases/latest"

        # Attempt to fetch the latest release information
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        latest_release = response.json()
        return latest_release.get('tag_name')  # Use .get() to avoid KeyError if 'tag_name' is missing

    except HTTPError as http_err:
        log.log_message(f"HTTP error occurred while accessing {api_url}: {http_err}")
    except RequestException as req_err:
        log.log_message(f"Request error occurred while accessing {api_url}: {req_err}")
    except ValueError as val_err:
        log.log_message(f"JSON parsing error: {val_err}")  # Catches invalid JSON
    except Exception as err:
        log.log_message(f"An unexpected error occurred: {err}")

    return None  # Return None in case of failure


def get_spaghetti_path(output_directory: str) -> str:
    return f"{output_directory}/spaghetti.exe"


def does_spaghetti_exist() -> bool:
    return os.path.isfile(get_spaghetti_path())


def get_stove_path(output_directory: str) -> str:
    return f"{output_directory}/stove.exe"


def does_stove_exist(output_directory: str) -> bool:
    return os.path.isfile(get_stove_path(output_directory))


def is_repak_packing_enum_in_use():
    is_in_use = False
    for entry in get_mods_info_from_json():
        if entry['packing_type'] == "repak":
            is_in_use = True
    return is_in_use


def is_loose_packing_enum_in_use():
    is_in_use = False
    for entry in get_mods_info_from_json():
        if entry['packing_type'] == "loose":
            is_in_use = True
    return is_in_use


def is_engine_packing_enum_in_use():
    is_in_use = False
    for entry in get_mods_info_from_json():
        if entry['packing_type'] == "engine":
            is_in_use = True
    return is_in_use


def is_unreal_pak_packing_enum_in_use():
    is_in_use = False
    for entry in get_mods_info_from_json():
        if entry['packing_type'] == "unreal_pak":
            is_in_use = True
    return is_in_use


def get_is_using_repak_path_override() -> bool:
    return main_logic.settings_information.settings['repak_info']['override_default_repak_path']


def get_repak_path_override() -> str:
    return main_logic.settings_information.settings['repak_info']['repak_path_override']


def get_game_info_launch_type_enum_str_value() -> str:
    return main_logic.settings_information.settings['game_info']['launch_type']


def get_game_id() -> int:
    return main_logic.settings_information.settings['game_info']['game_id']


def get_game_launcher_exe_path() -> str:
    return main_logic.settings_information.settings['game_info']['game_launcher_exe']


def get_game_launch_params() -> list:
    return main_logic.settings_information.settings['game_info']['launch_params']


def get_override_automatic_launcher_exe_finding() -> bool:
    return main_logic.settings_information.settings['game_info']['override_automatic_launcher_exe_finding']


def get_window_management_events():
    return main_logic.settings_information.settings["window_management_events"]


def get_engine_launch_args() -> list:
    return main_logic.settings_information.settings['engine_info']['engine_launch_args']


def get_exec_events() -> list:
    return main_logic.settings_information.settings['exec_events']


def get_mods_info_from_json() -> list:
    return main_logic.settings_information.settings['mods_info']


def get_game_exe_path() -> str:
    game_exe_path = main_logic.settings_information.settings['game_info']['game_exe_path']
    file_io.check_path_exists(game_exe_path)
    return game_exe_path


def get_is_using_alt_dir_name() -> bool:
    return main_logic.settings_information.settings['packaging_uproject_name']['use_override']


def get_alt_packing_dir_name() -> str:
    return main_logic.settings_information.settings['packaging_uproject_name']['name']


def get_game_process_name():
    return unreal_engine.get_game_process_name(get_game_exe_path())


def get_process_kill_events() -> list:
    return main_logic.settings_information.settings['process_kill_events']['processes']


def kill_processes(state: HookStateType):
    current_state = state.value if isinstance(state, HookStateType) else state
    for process_info in get_process_kill_events():
        target_state = process_info.get('hook_state')
        if target_state == current_state:
            if process_info['use_substring_check']:
                proc_name_substring = process_info['process_name']
                for proc_info in file_io.get_processes_by_substring(proc_name_substring):
                    proc_name = proc_info['name']
                    file_io.kill_process(proc_name)
            else:
                proc_name = process_info['process_name']
                file_io.kill_process(proc_name)


def get_override_automatic_version_finding() -> bool:
    return main_logic.settings_information.settings['engine_info']['override_automatic_version_finding']


def custom_get_unreal_engine_version(engine_path: str) -> str:
    if get_override_automatic_version_finding():
        unreal_engine_major_version = main_logic.settings_information.settings['engine_info']['unreal_engine_major_version']
        unreal_engine_minor_version = main_logic.settings_information.settings['engine_info']['unreal_engine_minor_version']
        return f'{unreal_engine_major_version}.{unreal_engine_minor_version}'
    else:
        return unreal_engine.get_unreal_engine_version(engine_path)


def custom_get_game_dir():
    return unreal_engine.get_game_dir(get_game_exe_path())


# def custom_get_game_paks_dir() -> str:
#     alt_game_dir = os.path.dirname(custom_get_game_dir())
#     if get_is_using_alt_dir_name():
#         return os.path.join(alt_game_dir, get_alt_packing_dir_name, 'Content', 'Paks')
#     elif not get_should_skip_uproject_steps():
#         return unreal_dev_utils.get_game_paks_dir(get_uproject_file(), custom_get_game_dir())
#     else:
#         return f'{os.path.dirname(os.path.dirname(os.path.dirname(get_game_exe_path())))}/Content/Paks'


def custom_get_game_paks_dir() -> str:
    alt_game_dir = os.path.dirname(custom_get_game_dir())
    if get_is_using_alt_dir_name():
        return os.path.join(alt_game_dir, get_alt_packing_dir_name, 'Content', 'Paks')
    else:
        return unreal_engine.get_game_paks_dir(get_uproject_file(), custom_get_game_dir())


def get_unreal_engine_dir() -> str:
    ue_dir = main_logic.settings_information.settings['engine_info']['unreal_engine_dir']
    file_io.check_path_exists(ue_dir)
    return ue_dir


def get_uproject_file() -> str:
    uproject_file = main_logic.settings_information.settings['engine_info']['unreal_project_file']
    return uproject_file


def get_uproject_dir():
    return os.path.dirname(get_uproject_file())


def get_uproject_unreal_auto_mod_dir():
    return f'{get_uproject_dir()}/Plugins/UnrealAutoMod'


def get_uproject_unreal_auto_mod_resources_dir():
    return f'{get_uproject_unreal_auto_mod_dir()}/Resources'


def get_persistent_mods_dir() -> str:
    return f'{main_logic.settings_information.settings_json_dir}/mod_packaging/persistent_files'


def get_use_mod_name_dir_name_override(mod_name: str) -> bool:
    return get_mods_info_dict(mod_name)['use_mod_name_dir_name_override']


def get_mod_name_dir_name_override(mod_name: str) -> bool:
    return get_mods_info_dict(mod_name)['mod_name_dir_name_override']


def get_mod_name_dir_name(mod_name: str) -> str:
    if get_use_mod_name_dir_name_override(mod_name):
        return get_mod_name_dir_name_override(mod_name)
    else:
        return mod_name


def get_pak_dir_structure(mod_name: str) -> str:
    for info in get_mods_info_from_json():
        if info['mod_name'] == mod_name:
            return info['pak_dir_structure']
    return None


def get_mod_compression_type(mod_name: str) -> CompressionType:
    for info in get_mods_info_from_json():
        if info['mod_name'] == mod_name:
            compression_str = info['compression_type']
            return get_enum_from_val(CompressionType, compression_str)
    return None


def get_unreal_mod_tree_type_str(mod_name: str) -> str:
    for info in get_mods_info_from_json():
        if info['mod_name'] == mod_name:
            return info['mod_name_dir_type']
    return None


def get_mods_info_dict(mod_name: str) -> dict:
    for info in get_mods_info_from_json():
        if info['mod_name'] == mod_name:
            return dict(info)
    return None


def is_mod_name_in_list(mod_name: str) -> bool:
    for info in get_mods_info_from_json():
        if info['mod_name'] == mod_name:
            return True
    return False


def get_mod_name_dir(mod_name: str) -> dir:
    if is_mod_name_in_list(mod_name):
        return f'{unreal_engine.get_uproject_dir(get_uproject_file())}/Saved/Cooked/{get_unreal_mod_tree_type_str(mod_name)}/{mod_name}'
    return None


def get_mod_name_dir_files(mod_name: str) -> list:
    return file_io.get_files_in_tree(get_mod_name_dir(mod_name))


def get_persistant_mod_dir(mod_name: str) -> str:
    return f'{main_logic.settings_information.settings_json_dir}/mod_packaging/persistent_files/{mod_name}'


def get_persistant_mod_files(mod_name: str) -> list:
    return file_io.get_files_in_tree(get_persistant_mod_dir(mod_name))


def get_is_overriding_default_working_dir() -> bool:
    return main_logic.settings_information.settings['general_info']['override_default_working_dir']


def get_override_working_dir() -> str:
    return main_logic.settings_information.settings['general_info']['working_dir']


# def get_working_dir() -> str:
#     if get_is_overriding_default_working_dir():
#         working_dir = get_override_working_dir()
#     else:
#         working_dir = os.path.join(settings.SCRIPT_DIR, 'working_dir')
#     os.makedirs(working_dir, exist_ok=True)
#     return working_dir


def get_working_dir() -> str:
    working_dir = os.path.join(main_logic.SCRIPT_DIR, 'working_dir')
    os.makedirs(working_dir, exist_ok=True)
    return working_dir


def clean_working_dir():
    working_dir = get_working_dir()
    if os.path.isdir(working_dir):
        try:
            shutil.rmtree(working_dir)
        except Exception as e:
            log.log_message(f"Error: {e}")


def get_window_management_events() -> dict:
    return main_logic.settings_information.settings['window_management_events']


def get_engine_cooking_args() -> list:
    return main_logic.settings_information.settings['engine_info']['engine_cooking_args']


def get_engine_packaging_args() -> list:
    return main_logic.settings_information.settings['engine_info']['engine_packaging_args']


def get_engine_building_args() -> list:
    return main_logic.settings_information.settings['engine_info']['engine_building_args']


def get_is_overriding_automatic_version_finding() -> bool:
    return main_logic.settings_information.settings['repak_info']['override_automatic_version_finding']


def get_override_automatic_window_title_finding() -> bool:
    return main_logic.settings_information.settings['game_info']['override_automatic_window_title_finding']


def get_window_title_override() -> str:
    return main_logic.settings_information.settings['game_info']['window_title_override']


def get_window_title() -> str:
    return main_logic.settings_information.settings['general_info']['window_title']


def filter_file_paths(paths_dict: dict) -> dict:
    filtered_dict = {}
    path_dict_keys = paths_dict.keys()
    for path_dict_key in path_dict_keys:
        if os.path.isfile(path_dict_key):
            filtered_dict[path_dict_key] = paths_dict[path_dict_key]
    return filtered_dict


def get_game_window_title() -> str:
    if get_override_automatic_window_title_finding():
        return get_window_title_override()
    else:
        unreal_engine.get_game_process_name(get_game_exe_path())


def ensure_path_quoted(path: str) -> str:
    return f'"{path}"' if not path.startswith('"') and not path.endswith('"') else path


def run_app(
        exe_path: str,
        exec_mode: ExecutionMode = ExecutionMode.SYNC,
        args: list = [],
        working_dir: str = None
    ):

    exe_path = ensure_path_quoted(exe_path)

    if exec_mode == ExecutionMode.SYNC:
        command = exe_path
        for arg in args:
            command = f'{command} {arg}'
        log.log_message('----------------------------------------------------')
        log.log_message(f'Command: main executable: {exe_path}')
        for arg in args:
            log.log_message(f'Command: arg: {arg}')
        log.log_message('----------------------------------------------------')
        log.log_message(f'Command: {command} running with the {exec_mode} enum')
        if working_dir:
            if os.path.isdir(working_dir):
                os.chdir(working_dir)

        process = subprocess.Popen(command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)

        for line in iter(process.stdout.readline, ''):
            log.log_message(line.strip())

        process.stdout.close()
        process.wait()
        log.log_message(f'Command: {command} finished')

    elif exec_mode == ExecutionMode.ASYNC:
        command = exe_path
        for arg in args:
            command = f'{command} {arg}'
        log.log_message(f'Command: {command} started with the {exec_mode} enum')
        subprocess.Popen(command, cwd=working_dir, start_new_session=True, shell=True)


def get_running_time():
    from unreal_auto_mod import initialization
    return time.time() - initialization.start_time


def get_cleanup_repo_path() -> str:
    return main_logic.settings_information.settings['git_info']['repo_path']


def get_unreal_engine_building_main_command() -> str:
    return main_logic.settings_information.settings['engine_info']['engine_building_command']


def get_unreal_engine_cooking_main_command() -> str:
    return main_logic.settings_information.settings['engine_info']['engine_cooking_command']


def get_unreal_engine_packaging_main_command() -> str:
    return main_logic.settings_information.settings['engine_info']['engine_packaging_command']


def get_git_info_repo_path() -> str:
    return main_logic.settings_information.settings['git_info']['repo_path']
