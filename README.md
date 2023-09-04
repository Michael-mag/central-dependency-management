# central-dependency-management
Manage some common dependencies that I will need in various projects.

### How to use:
1. Run the command: ```merge-dependencies```, which is a function already existing in my ```.zshprofile```
   - The function is defined as follows, so the first thing would be to copy paste the following code snippet into your ```.zshprofile``` file which is a hidden file found in the home directory:
   - First run the command ```open ~./zshprofile``` to open this hidden file in the mac default text editor and then copy and paste the following code snippet into the file.
      ```bash
      
      # Function to merge Maven dependencies
      merge-dependencies() {
      # Clone the central-dependency-management repository into the current directory
      echo "Downloading private projects central dependencies..."
      git clone git@github.com:Michael-mag/central-dependency-management.git
      
      # Set the destination POM file path to the current directory
      destination_pom_file="$(find "$(pwd)" -name 'pom.xml' -type f -print -quit)"
      echo "Merging central-dependency-management dependencies into: $destination_pom_file"
      
      if [ -z "$destination_pom_file" ]; then
      echo "ERROR: No pom.xml file found in the current directory."
      return 1
      fi
      
      # Set the source POM file path from the cloned repository
      source_pom_file="./central-dependency-management/pom.xml"
      
      # Run the Python script to merge dependencies using the source and destination POM file paths
      python ./central-dependency-management/merge_dependencies.py "$source_pom_file" "$destination_pom_file"
      
      rm -rf central-dependency-management
      echo "FINISHED: Merging central-dependency-management dependencies into: $destination_pom_file"
      }```

2. Now execute the command mentioned in one by going to the root directory of your java maven project and run the following command ```merge-dependencies```