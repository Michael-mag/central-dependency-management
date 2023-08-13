# central-dependency-management
Manage some common dependencies that I will need in various projects.

### How to use:
1. For myself, i just need to run the comand:``` private-mvn-settings``` which is a shell script function that I 
  defined in my ```.zshrc``` file on my mac. This function 
  does the following (& a few other things for myself)
- Download & install this repo. You can use
  the commands below while in the root of your project that you want to 
  include this:

    ```zshr
      git clone git@github.com:Michael-mag/central-dependency-management.git
      cd central-dependency-management
      mvn clean install
    ```
- Now you should see a new folder appear in the root of your project named 
  ```central-dependency-management```
2. #### PARENT CONFIGURATION:
   - If you already have a parent in your project, cut and paste it into the 
     ```central-dependency-management``` pom file.
     - I have already moved my parent, and that is the one that you see in the ```central-dependency-management``` pom file.

   - Now add ```central-dependency-management``` as parent. You can copy and 
     paste the snippet below into your project root pom, or wherever you 
     need it:
     ```xml
        <parent>
            <groupId>com.michael.magaisa.central-dependencies</groupId>
            <artifactId>central-dependencies</artifactId>
            <version>1.0</version>
        </parent>
   
3. Now install your project: e.g run ```mvn clean install```  
4. Additionally, you can add : ```central-dependency-management``` to your .
   gitignore file if you do not want to check in this with your project code.