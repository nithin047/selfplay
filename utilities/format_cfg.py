def format_cfg(cfg_dict):
    """
    Formats elements of config dict and returns them
    :param cfg_dict:
    :return:
    """
    formatted_cfg_dict = cfg_dict.copy()
    traverse_and_format_dict(formatted_cfg_dict)

    return formatted_cfg_dict['settings']


def traverse_and_format_dict(d):
    for key, value in d.items():
        if isinstance(value, dict):
            traverse_and_format_dict(value)
        else:
            d[key] = format_cfg_value(value)


def format_cfg_value(cfg_item):

    if isinstance(cfg_item, str):
        if cfg_item.isdigit():
            return int(cfg_item)
        elif cfg_item.startswith('[') and cfg_item.endswith(']'):
            cfg_item = cfg_item.replace('[', '').replace(']', '').replace(' ', '')
            temp_list = cfg_item.split(',')
            return [float(element) for element in temp_list]

        else:
            return cfg_item
    else:
        return None