# ChatSocialService or GabybotTSJ
-----------------------------
## License
This project is licensed under the Apache License 2.0, See the LICENSE file for more details.
-----------------------------
GabybotTSJ is a project simplifies the management of the social service department. 

### 1. **Setting up your environment:**
- complete your own virtual environment and install all libraries.

### 2. **Configuration with .env file**
1. *Create an `.env` file with the following validations:*
 - `TOKEN_BOT` = Your bot token (replace`XXXXXXX`)
 - `PATH_PDF` = /home/your/route/pdf/file.pdf
 - `INFORMATION` = https://your-google-presentation-or-rute
 - `PHOTO_01` = /home/your/example/photo/
 - `PHOTO_02` = /home/your/example/photo/
 - `PHOTO_03` = /home/your/example/photo/
 - `PHOTO_04` = /home/your/example/photo/
 - `MODIFIED_PDF_PATH` = path/where/the/new/pdf/with/added/information/will/be/`Temp`

### 3. **You need create a new `Temp` folder in your `.env`**

### 4. **Project installation and setup**
To install the necessary libraries, a file named, `requirements.txt` was generated, wich includes all dependencies for this project, such as `Telebot`, 
`SQLite`, `hashlib`, `decouple`, `PyPDF2`, `ReportLab`, and other essencial ones. This small text file should be generated before installing any library or dependency.
***It is recommended to do this from a new virtual environment specifically for the project to avoid interference with the system.***
  
**Steps to Set up**
1. Create a new folder with the project name and work within it:  
 - `mkdir project_name`  
 - `cd project_name`  
2. Create a virtual environment for the project:  
 - `python -m venv project1`  
3. Activate the virtual environment:  
    * On Linux or macOS:  
 - `source project1/bin/activate`  
    * On Windows:  
 - `project1\Scripts\activate.bat`  
4. Create the `requirements.txt` file  
    * On Linux or macOS:  
 - `touch requirements.txt`  
    * On Windows:  
 - `notepad requirements.txt`  
5. Start installing dependencies:  
 - `pip install dependency_name`  
  
Every time if a pip library is installed, the file `requirements.txt` should be updated and frozen to ensure the libraries remain intact when deleting or creating a new project.
This is very useful for transferring data to other projects that require the same dependencies.
  
6. freeze `requirements.txt`:  
 - `pip freeze > requirements.txt`  
7. To view the dependencies in the file:  
 - `pip list`  
8. To install dependencies in another project:  
 - `pip install -r requirements.txt`  
9. To delete a project along with its files and folder:  
    * On Linux or macOS:  
 - `rm -r project1`  
    * On Windows:  
 - `delete it manually through the graphical interface`  
  
**Project Structure**  
The structure of this project is organized as follows:  
 - The `src` folder contains the source codes of the chatbot, incluiding modules for direct interaction with the Telegram API.  
 - The `db` directory serves to store the databases created in SQLite.  
 - The `Temp` folder is a temporary directory used for generating the PDF file requested by the user on Telegram. This prevents local storage of generated formats on the server.  
 - The `venv` folder contains the locally installed libraries in an encapsulated form.  
 - The `requirements.txt` file contains the dependencies used in the project.  
  
**Testing**  
The chatbot in Telegram was tested to observe its functionality when generating PDF formats corresponding to the social service area. The tests included:  
 - Response time for each requested event
 - Handling of automated responses
 - Generation of PDF formats
 - Exporting user data in a recognizable format in a CSV extension  
  
Tests also included sending images in PNG and JPG formats to provide filling examples through the chatbot questionnaire on Telegram. It was ensured that the X and Y 
coordinates where the data is plotted, are accurate and readable for users when downloading the generated file through the Telegram chatbot.  
We hope that the project can be useful for other Tecnológicos and it can be complemented. We send greetings.





Special thanks:
We thank to the developers of ReportLab for providing this PDF generation library.
https://github.com/Distrotech/reportlab

