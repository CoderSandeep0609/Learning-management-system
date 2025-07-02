'''
All Exception listed here
'''

class QuizEvaluationError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class AssignmentEvaluationError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class SMSNotifierError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class EmailNotifierError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class StudentError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class LMSError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
class DuplicateDataError(Exception):
    def __init__(self,message):
        self.message=message
    def __str__(self):
        return self.message
    

'''Abstract class'''
from abc import ABC,abstractmethod

class EvaluationPlugin(ABC):
    @property
    @abstractmethod
    def plugin_name(self):
        pass

    @abstractmethod
    def validate(self):
        pass
    @abstractmethod
    def evaluate(self,score):
        pass
    @classmethod
    def from_config(cls,config_dict):
        pass


class QuizEvaluation(EvaluationPlugin):
    def __init__(self,subject=None,max_score=None,pass_marks=None):
        if not subject or not max_score or not pass_marks:
            raise QuizEvaluationError('Value missing in Quiz Evaluation')
        else:
            self.subject=subject
            self.max_score=max_score
            self.pass_marks=pass_marks
            self.scored=0
            self.validate()
    @property
    def plugin_name(self):
        return 'Quiz'
    def validate(self):
        if self.max_score<0:
            raise QuizEvaluationError('Max-marks should not be in negative')
        if self.pass_marks<0:
            raise QuizEvaluationError('Pass marks should not be in negative')
    
    def evaluate(self,student):
        self.scored=50
        student.marks=self.scored
        if self.scored<self.pass_marks:
            student.remarks='FAIL'
            return f'{student.name} scored {self.scored} and >>>>>>>> failed'
        student.remarks='PASS'
        return f'{student.name} scored {self.scored} and >>>>>>> Pass'
    @classmethod
    def from_config(cls,config):
        try:
            obj_quiz=cls(config['subject'],config['max-score'],config['pass-marks'])
            obj_quiz.student=config['student']
        except KeyError as e:
            print('Invalid data for Quiz')
        else:
            return obj_quiz.evaluate(obj_quiz.student)

class AssignmentEvaluation(EvaluationPlugin):
    def __init__(self,subject=None,max_score=None,pass_marks=None):
        if not subject or not max_score or not pass_marks:
            raise AssignmentEvaluationError('Value missing in Assignment Evaluation')
        else:
            self.subject=subject
            self.max_score=max_score
            self.pass_marks=pass_marks
            self.scored=0
            self.validate()
    def validate(self):
        if self.max_score<0:
            raise AssignmentEvaluation('Max-marks should not be in negative')
        if self.pass_marks<0:
            raise AssignmentEvaluation('Pass marks should not be in negative')
    def evaluate(self,student):
        self.scored=50
        student.marks=self.scored
        if self.scored<self.pass_marks:
            student.remarks='FAIL'
            return f'{student.name} scored {self.scored} and >>>>>>>> failed'
        student.remarks='PASS'
        return f'{student.name} scored {self.scored} and >>>>>>> Pass'
    @classmethod
    def from_config(cls,config):
        try:
            obj_assignment=cls(
                config['subject'],
                config['max_score'],
                config['pass_marks']
            )
            student=config['student']
            if not student:
                raise AssignmentEvaluationError('Student data not provided')
        except AssignmentEvaluationError as e:
            print(e)
        except KeyError as e:
            raise AssignmentEvaluationError('Key missing in Assignmnt fron config')
        else:
            return obj_assignment.evaluate(student)
    @property
    def plugin_name(self):
        return 'Assignment'

'''
Abstract class for notification
'''

class Notifier(ABC):
    @abstractmethod
    def notify(self,message):
        pass
    @classmethod
    def from_config(self,config):
        pass

class SMSNotifier(Notifier):
    def notify(self,message=None,no=None):
        if not message or not no:
            raise SMSNotifierError('Data is missing in SMS notifier')
        return f'{message} has been sent to {no}'
    @classmethod
    def from_config(cls,config):
        try:
            msgs=config['message']
            number=config['no']
        except KeyError as e:
            raise SMSNotifierError('You have missed to provide value for SMS from config')
        else:
            sms_obj=cls()
            return sms_obj.notify(msgs,number)

class EmailNotifier(Notifier):
    def notify(self,message=None,email=None):
        if not message or not email:
            raise EmailNotifierError('Value missing in Email notifire')
        else:
            return f'{message} has been sent to {email}'
    
    @classmethod
    def from_config(cls,config):
        try:
            msgs=config['message']
            email=config['email']
        except KeyError as e:
            raise EmailNotifierError('You have missed to provide value for EMAIL from config')
        else:
            obj_email=cls()
            return obj_email.notify(msgs,email)

class Student:
    def __init__(self,name=None,age=None,subject=None,email=None,phone=None,notifier_mode=None,exam_mode=None):
        if not name or not age or not email or not phone or not notifier_mode or not exam_mode:
            raise StudentError('Value nissing for student,,, check again')
        elif isinstance(age,int)==False:
            raise ValueError('Age would be in integer')
        else:
            self.name=name
            self.age=age
            self.subject=subject
            self.email=email
            self.phone=phone
            self.notifier_mode=notifier_mode
            self.exam_mode=exam_mode
            self.marks=None
            self.remarks=None

class LMS:
    student_lists=[]
    def __init__(self):
        print('LMS into system')
    def evaluate_student(self,student):
        if student.exam_mode=='Quiz':
            obj_quiz=QuizEvaluation.from_config({'subject':student.subject,'max-score':100,'pass-marks':40,'student':student})
            return obj_quiz
        elif student.exam_mode=='Assignment':
            obj_assignment=AssignmentEvaluation.from_config({'subject':student.subject,'max-score':100,'pass-marks':40,'student':student})
            return obj_assignment
    def make_nofity(self,message,student):
        if student.notifier_mode=='SMS':
            obj_sms=SMSNotifier.from_config({'message':message,'no':student.phone})
            print(obj_sms,'message has been sent successfully')
        elif student.notifier_mode=='email':
            obj_email=EmailNotifier.from_config({'message':message,'email':student.email})
            print(obj_email,'message has been sent successfully')
    def register_student(self,student=None):
        if not student:
            raise LMSError('Error while regestring student')
        else:
            if student.remarks=='PASS':
                LMS.student_lists.append({
                    student.phone:{
                        'name':student.name,
                        'age':student.age,
                        'email':student.email,
                        'subject':student.subject,
                        'exam_mode':student.exam_mode,
                        'marks':student.marks,
                        'remarks':student.remarks
                    }
                })
                print(f'{student.name} has been registered successfully')
    @classmethod
    def from_config(cls,config):
        student=None
        for data in LMS.student_lists:
            if config['student']['phone'] in data.keys():
                raise DuplicateDataError('Student already exist in the LMS,, choose another phone number')
        else:
            stu=Student(
                config['student']['name'],
                config['student']['age'],
                config['student']['subject'],
                config['student']['email'],
                config['student']['phone'],
                config['student']['notifier_mode'],
                config['student']['exam_mode'],
            )
            student=stu

        obj_lms=cls()
        record=obj_lms.evaluate_student(student)
        if student.notifier_mode=='SMS':
            obj_lms.make_nofity(record,student)
        else:
            obj_lms.make_nofity(record,student)
        obj_lms.register_student(student)
        return obj_lms

config = {
    "student": {
        "name": "Rahul",
        "age": 18,
        'subject':'Python',
        "email": "abc@example.com",
        "phone": "9896253434",
        'exam_mode':'Quiz',
        'notifier_mode':'email'
    }
}
try:
    obj=LMS.from_config(config)
except KeyError as e:
    print(e)
except ValueError as e:
    print(e)
except DuplicateDataError as e:
    print(e)
except QuizEvaluationError as e:
    print(e)
except AssignmentEvaluationError as e:
    print(e)
except SMSNotifierError as e:
    print(e)
except EmailNotifierError as e:
    print(e)
except LMSError as e:
    print(e)
except StudentError as e:
    print(e)
except Exception as e:
    print(e)
else:
    print(obj.student_lists)
finally:
    print('Admission Done')
    

