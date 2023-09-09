import os

def getPath(app):
    """
    params: app str: app name
    return: home_path, db_file_path
    notice: some app's name may be different with it's package name in app_path
    """
    if app:
        home_path = os.environ['HOME']
        # macos apps path
        app_path = os.path.join(home_path, r'Library/Group Containers')
        app_list = os.listdir(app_path)

        for app_name in app_list:
            if app in app_name:
                # {app}'s absolute path
                app_path = os.path.join(app_path, app_name)
                # get all infos and find sqlite files
                for _dir, _, _file_list in os.walk(app_path):
                    for file in _file_list:
                        if file.endswith('.sqlite'):
                            db_file_path = os.path.join(_dir, file)
                            return home_path, db_file_path
            else:
                continue
        return home_path, f"check if {app} is the same as it's name in the {app_path}"
                
    else:
        return home_path, 'Please tell which app you want to get path'
    
    


def main():
    home_path, db_file_path = getPath('openai')
    print(home_path, db_file_path)


if __name__ == "__main__":
    main()