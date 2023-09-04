import xml.etree.ElementTree as ET
import sys
import shutil  # Import shutil for file backup


def rearrange_xml(xml_file):
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the 'dependencyManagement' and 'build' elements
    dependency_management = None
    build = None
    for element in root:
        if element.tag == 'dependencyManagement':
            dependency_management = element
        elif element.tag == 'build':
            build = element

    # Remove 'build' if found
    if build is not None:
        root.remove(build)

    # Append 'build' after 'dependencyManagement' if both are found
    if dependency_management is not None:
        root.append(build)

    # Save the modified XML back to the file
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True)


if len(sys.argv) != 3:
    print("Usage: python merge_dependencies.py source_pom.xml destination_pom.xml")
    sys.exit(1)

source_pom_path = sys.argv[1]
destination_pom_path = sys.argv[2]

# Backup the destination POM file
backup_pom_path = destination_pom_path + '.bak'
shutil.copy(destination_pom_path, backup_pom_path)

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

# Find the <dependencies> and <dependencyManagement> sections in the destination POM
destination_dependencies = destination_root.find('.//ns0:dependencies', namespaces)
destination_dependency_management = destination_root.find('.//ns0:dependencyManagement', namespaces)

# Find the <dependencies> and <dependencyManagement> sections in the source POM
source_dependencies = source_root.find('.//ns0:dependencies', namespaces)
source_dependency_management = source_root.find('.//ns0:dependencyManagement', namespaces)

# Merge <dependencies> from source to destination
if source_dependencies is not None:
    if destination_dependencies is not None:
        destination_dependencies.extend(source_dependencies)
    else:
        # If destination dependencies don't exist, create it and append source dependencies
        destination_root.append(source_dependencies)

# Merge <dependencyManagement> from source to destination
if source_dependency_management is not None:
    if destination_dependency_management is not None:
        destination_dependency_management.extend(source_dependency_management)
    else:
        # If destination dependencyManagement doesn't exist, create it and append source dependencyManagement
        destination_root.append(source_dependency_management)

# Merge <build> from source to destination
source_build = source_root.find('.//ns0:build', namespaces)
if source_build is not None:
    destination_build = destination_root.find('.//ns0:build', namespaces)
    if destination_build is not None:
        # Find the <plugins> section in both source and destination
        source_plugins = source_build.find('.//ns0:plugins', namespaces)
        destination_plugins = destination_build.find('.//ns0:plugins', namespaces)

        if source_plugins is not None:
            if destination_plugins is not None:
                # Append individual <plugin> elements from source to destination
                for source_plugin in source_plugins:
                    destination_plugins.append(source_plugin)
            else:
                # If destination <plugins> doesn't exist, create it and append source <plugins>
                destination_build.append(source_plugins)


# Remove the 'ns0:' namespace prefix from all elements and attributes in the merged XML
for elem in destination_root.iter():
    elem.tag = elem.tag.replace('{http://maven.apache.org/POM/4.0.0}', '')

    for key in list(elem.attrib.keys()):
        if key.startswith('{http://maven.apache.org/POM/4.0.0}'):
            new_key = key[len('{http://maven.apache.org/POM/4.0.0}'):]
            elem.attrib[new_key] = elem.attrib.pop(key)

# Save the updated destination POM file as "pom.xml"
destination_tree.write(destination_pom_path, encoding='UTF-8', xml_declaration=True)

# Rearrange the XML elements and save as "output_pom.xml"
rearrange_xml(destination_pom_path)

print("Merging and cleanup completed. Updated POM saved as 'pom.xml'")
