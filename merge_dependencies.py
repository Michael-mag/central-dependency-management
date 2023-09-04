import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 3:
    print("Usage: python merge_dependencies.py source_pom.xml destination_pom.xml")
    sys.exit(1)

source_pom_path = sys.argv[1]
destination_pom_path = sys.argv[2]

# Load the destination POM file
destination_tree = ET.parse(destination_pom_path)
destination_root = destination_tree.getroot()

# Load the source POM file
source_tree = ET.parse(source_pom_path)
source_root = source_tree.getroot()

# Define XML namespaces
namespaces = {
    'ns0': 'http://maven.apache.org/POM/4.0.0',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Merge <dependencies> from source to destination
source_dependencies = source_root.find('.//ns0:dependencies', namespaces)
if source_dependencies is not None:
    destination_dependency_management = destination_root.find('.//ns0:dependencyManagement', namespaces)
    if destination_dependency_management is not None:
        # Append source dependencies to the existing destination dependencies if it exists
        destination_dependencies = destination_dependency_management.find('.//ns0:dependencies', namespaces)
        if destination_dependencies is not None:
            destination_dependencies.extend(source_dependencies)
        else:
            # If destination dependencies don't exist, create it and append source dependencies
            destination_dependency_management.append(source_dependencies)

# Merge <dependencyManagement> from source to destination
source_dependency_management = source_root.find('.//ns0:dependencyManagement', namespaces)
if source_dependency_management is not None:
    destination_dependency_management = destination_root.find('.//ns0:dependencyManagement', namespaces)
    if destination_dependency_management is not None:
        # Append source dependencyManagement to the existing destination dependencyManagement if it exists
        destination_dependency_management.extend(source_dependency_management)
    else:
        # If destination dependencyManagement doesn't exist, create it and append source dependencyManagement
        destination_root.append(source_dependency_management)

# Merge <build> from source to destination
source_build = source_root.find('.//ns0:build', namespaces)
if source_build is not None:
    destination_build = destination_root.find('.//ns0:build', namespaces)
    if destination_build is not None:
        destination_build.extend(source_build)

# Remove the 'ns0:' namespace prefix from all elements and attributes in the merged XML
for elem in destination_root.iter():
    elem.tag = elem.tag.replace('{http://maven.apache.org/POM/4.0.0}', '')

    for key in list(elem.attrib.keys()):
        if key.startswith('{http://maven.apache.org/POM/4.0.0}'):
            new_key = key[len('{http://maven.apache.org/POM/4.0.0}'):]
            elem.attrib[new_key] = elem.attrib.pop(key)

# Save the updated destination POM file
destination_tree.write('updated_destination_pom.xml', encoding='UTF-8', xml_declaration=True)

print("Merging and cleanup completed. Updated POM saved as 'updated_destination_pom.xml'")
