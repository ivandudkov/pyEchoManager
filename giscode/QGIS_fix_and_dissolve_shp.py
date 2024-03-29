import os
import processing


### Importing my script "file_ext_search.py"
# Define a function that searches for files with defined extension
# and returns a list of full paths for these files

# If function doesn't find any file in the parent directory,
# it will search for one directory up

# August 2021
# Author: Ivan Dudkov
# Affiliations:
# P.P Shirshov's Institute of Oceanography, Atlantic Branch, Kaliningrad, Russia. (2018 - ????)
# Center for Coastal and Ocean Mapping, University of New Hampshire. Durham, USA. (2020-2021)

def file_ext_search(extension: str, path=os.getcwd(), recursive=False) -> list:
    """
    extension
    path
    recursive
    """
    
    # Check the top path existence
    if os.path.exists(path):
        print(('Searching *%s files in directory:' + path) % extension)
    else:  # Raise a meaningful error
        raise RuntimeError('Path either not exists or not correct ' + path)

    paths = []
    count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        if recursive is True:
            for filename in filenames:
                fextension = os.path.splitext(filename)[1]
                if fextension == extension:
                    paths.append(os.path.abspath(os.path.join(dirpath, filename)))
                    count += 1
        else:
            if dirpath == path:
                for filename in filenames:
                    fextension = os.path.splitext(filename)[1]
                    if fextension == extension:
                        paths.append(os.path.abspath(os.path.join(dirpath, filename)))

                        count += 1

    count = 0
    if len(paths) == 0:
        os.chdir(os.path.dirname(path))
        path_up = os.getcwd()
        print("Searching was unsuccessful. Trying to search in one directory up:\n%s" % path_up)

        for dirpath, dirnames, filenames in os.walk(path_up):
            for filename in filenames:
                fextension = os.path.splitext(filename)[1]
                if fextension == extension:
                    paths.append(os.path.abspath(os.path.join(dirpath, filename)))
                    count += 1
    return paths
### importing over


path_notfixed = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\Polygonized_shapes'
files_notfixed = file_ext_search('.shp', path_notfixed)
path_fixed = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\Polygonized_shapes_fixed'
path_dissolved = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing\Polygonized_shapes_fixed_dissolved'

for shapefile in files_notfixed:
    filename = os.path.basename(shapefile)

    output_fix = os.path.join(path_fixed, filename)
    output_dissolved = os.path.join(path_dissolved, filename)
    # run fixing
    processing.run("native:fixgeometries", 
    {'INPUT':shapefile,
    'METHOD':1,
    'OUTPUT':output_fix})
    
    processing.run("native:dissolve", 
    {'INPUT':output_fix,
    'FIELD':[],
    'SEPARATE_DISJOINT':False,
    'OUTPUT':output_dissolved})

output_folder = r'D:\aa_yandexcloud\aa_cloudmbesproceessing\aa_abp49_processing'
merged_filename = 'abp49_id001-054_merged.shp'
output_path = os.path.join(output_folder, merged_filename)
files_dissolved = file_ext_search('.shp', path_dissolved)
print(files_dissolved)

processing.run("native:mergevectorlayers", 
{'LAYERS':files_dissolved,
'CRS':QgsCoordinateReferenceSystem('EPSG:32634'),
'OUTPUT':output_path})