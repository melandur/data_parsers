import os


def checked_dir(dims):
    """Set dir name according to requested dims"""
    if '2d' in dims and '3d' in dims:
        dir_name = 'complete'
    elif '2d' in dims:
        dir_name = 'complete_2d'
    elif '3d' in dims:
        dir_name = 'complete_3d'
    
    return dir_name
