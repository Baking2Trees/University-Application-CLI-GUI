# University-Application-CLI-GUI Project

A local university system developed using both CLI and GUI interfaces. The application provides separate subsystems for students and administrators.

---

## Project Intro
- MVC Architecture (a simplified layered MVC structure rather than a strict MVC implementation, as the CLI and GUI classes act as both the View and Controller. They handle displaying interfaces as well as processing user actions.)

---

## How to Run? 

1. Make sure Python 3 is installed.

2. Clone this repository and run the program accordingly:

```bash
git clone https://github.com/Baking2Trees/University-Application-CLI-GUI.git
cd University-Application-CLI-GUI
python3 uni.py
```
3. Choose an option from the menu:

- (1) CLI version → follow the menu prompts  
- (2) GUI version → interact using buttons and input fields  

*Optional: Use test data if needed for demonstration.*

---

## Project Architecture
### i) Model
- **Student**
  - 6-digit unique id: `000001 ~ 999999`
  - max 4 subjects

- **Subject**
  - 3-digit unique id: `001 ~ 999`

- **Database**
  - checks if data exists in `students.data` before using/creating it  
  - reads/writes objects from/to `students.data`  
  - clears all objects from `students.data`  
  - includes helper functions in the *utilities* section to interact with the database  

### ii) View
- CLI menus/prints inside `CLIUniApp`  
- GUI screens inside `GUIUniApp` using Tkinter  

### iii) Controller
- `CLIUniApp`  
- `GUIUniApp`  

---

## Sample I/O
- Created menu for all required option pages  
- Added `(b) Back to Main Menu` for easier navigation during demo  
- Grade formatting is right-aligned for neat output:

---

## CLI Features

### University System Menu
- (A) Admin  
- (S) Student  
- (X) Exit  

### Student System Menu
- (l) login  
- (r) register  
- (x) exit  
- add-on: (b) back to main menu  

### Student Subject Enrolment Menu
- (c) change  
- (e) enrol  
- (r) remove  
- (s) show  
- (x) exit  
- add-on: (b) back to main menu  

### Admin System Menu
- (c) clear database  
- (g) group students  
- (p) partition students  
- (r) remove student  
- (s) show  
- (x) exit  
- add-on: (b) back to main menu  

---

## GUI Features
- Login for students (without admin options)  
  *(PS: login button is also bound to the Enter key)*  
- Max four subject enrolments for logged-in students  
- GUI exception handling for:
  - Empty login fields  
  - Incorrect student credentials  
  - Incorrect email format  
- Uses `Student` objects stored in `students.data` as registered students to log into `GUIUniApp`  
- Includes at least 4 windows/screens after login

---

## Code Quality
- The project was refined using pylint checks and achieved a final pylint score of `10.00 / 10`.

---

## Key Highlights
- Dual interface: CLI + GUI
- Persistent storage using file-based database (`pickle`)
- User-friendly navigation with back functionality
- Input validation and error handling
- Additional handling for:
  - invalid menu input
  - invalid subject ID when removing subjects
  - invalid password confirmation
  - maximum 4 subject enrolments in CLI and GUI
  - missing or unreadable `students.data` fallback
- Clean formatted output for readability

---

## Team
Somesh Shanbhag, Kelly Jia Yi Beh, Madhava Kumar Ravi & Sahil Uppal
