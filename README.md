# hello-world-real

### Project Description

# A messaging platform simililar in functionality to instagram

3 pages
Homepage/FYP
Messaging
Profile

| Functional Requirements                                          | Non Functional Requirements               |
| ---------------------------------------------------------------- | ----------------------------------------- |
| Navigate between pages using links/buttons                       | Acceptable load times (1 second)          |
| Login functionality                                              | Visually aesthetic                        |
| Send and save messages to a database which can then be retrieved | Streamlined ui for smooth user experience |
| Share images                                                     | Intuitive interface                       |

# Design decisions

- Minimalistic aesthetics (White,light colours)
- Rounded corners to give site polish
- legible, unadorned font,
- 1-2 font families

# Sketches/Wireframes

![Sketch 1](working_documents/1000022271-1.jpg)
![Sketch 2](working_documents/1000022270.jpg)

# Algorithms

Flow chart for Login Functionality
![flowchart](<working_documents/Screenshot 2025-08-14 111442.png>)

Test Case 1:

Test Case ID: 1
Test Case Name: User login functionality
Preconditions: User is registered on website, users data is recorded on database,
Test Steps:

- Open website
- Input details into relevant fields
- Press login button
  Expected Result: Succesfully logs in and unlocks website

Test Case 2:

Test Case ID: 2
Test Case Name: Message functionality
Preconditions: User is registered on website, users data is recorded on database, user is logged in
Test Steps:

- Log into website
- Open messages and select chat
- Input message
- Send message
- Log out

Expected result: Message is saved to chat and appears when recipitent logs in

Test Case 3:

Test Case ID: TC 003
Test Case Name: Change Bio
Preconditions: User is registered on website, users data is recorded on database, user is logged in
Test Steps:

- Log into website and navigate to profile page
- Click on edit bio button
- Input new bio
- Press save

Expected result: New bio is saved to backend and will remain upon logging out

## Database
