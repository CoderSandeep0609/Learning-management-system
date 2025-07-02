# Learning-management-system
Modular Learning Management System (LMS) – Python Project
🔧 Project Overview
This project implements a Modular Learning Management System (LMS) in Python using Object-Oriented Programming (OOP) principles. The LMS handles:

Student registration

Evaluation (Quiz or Assignment)

Notification (SMS or Email)

Config-driven plugin system for extensibility

Full error handling with custom exceptions

🚀 Key Features
✅ Plugin-based system using abstract classes
✅ Dynamic plugin selection using from_config()
✅ Auto evaluation + notification pipeline
✅ Duplicate student check via phone number
✅ Exception-safe execution with meaningful error messages
✅ Easy to extend: just add a new plugin or notifier

🧱 Class Structure
1. Exceptions
Custom exceptions for each responsibility (e.g., QuizEvaluationError, StudentError, etc.)

2. Abstract Base Classes
EvaluationPlugin: For different types of evaluation (e.g., quiz, assignment)

Notifier: For different notification modes (e.g., SMS, email)

3. Concrete Plugins
QuizEvaluation, AssignmentEvaluation implement evaluation logic

SMSNotifier, EmailNotifier implement notification methods

4. Student
Holds all relevant student data including exam type, notification mode, contact info, etc.

5. LMS
Core controller:

Evaluates student

Sends notification

Registers if passed

Prevents duplicate registrations

⚙️ Technologies Used
Python 3.x

No external libraries required (fully standard Python)
