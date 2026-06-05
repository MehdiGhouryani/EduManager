erDiagram
Course {
  integer id pk
  varchar title 
  varchar slug 
  text description 
  integer_unsigned capacity 
  text start_date 
  text end_date 
  bool is_active 
  text created_at 
  text updated_at 
  integer instructor_id 
}
Student {
  integer id pk
  integer user_id 
  varchar phone 
  bool is_active 
  text registered_at 
}
Content {
  integer id pk
  integer course_id 
  varchar title 
  varchar content_type 
  varchar file 
  text text_content 
  integer_unsigned order 
  bigint duration 
  text uploaded_at 
}
Quiz {
  integer id pk
  integer course_id 
  varchar title 
  text description 
  integer_unsigned time_limit 
}
Question {
  integer id pk
  integer quiz_id 
  text text 
  varchar option1 
  varchar option2 
  varchar option3 
  varchar option4 
  integer correct_option 
}
QuizAttempt {
  integer id pk
  integer student_id 
  integer quiz_id 
  real score 
  text completed_at 
}
Profile {
  integer id pk
  integer user_id 
  varchar role 
  varchar phone 
  text bio 
}
Announcement {
  integer id pk
  varchar title 
  text content 
  text created_at 
  bool is_active 
  bool show_on_login 
  bool show_on_dashboard 
}
EventType {
  integer id pk
  varchar name 
  text description 
}
Notification {
  integer id pk
  integer user_id 
  integer event_type_id 
  text message 
  varchar link 
  bool is_read 
  text created_at 
}
Assignment {
  integer id pk
  integer course_id 
  varchar title 
  text description 
  text due_date 
  integer_unsigned max_score 
  text created_at 
  text updated_at 
}
Submission {
  integer id pk
  integer assignment_id 
  integer student_id 
  varchar file 
  text submitted_at 
  integer_unsigned score 
  text feedback 
  bool is_late 
}
Assignment }|--|| Course: ""
Content }|--|| Course: ""
Profile ||--|| User: ""
Question }|--|| Quiz: ""
Quiz }|--|| Course: ""
Course }|--|{ Student: ""
Course }|--|| User: ""
Notification }|--|| User: ""
Notification }|--|| EventType: ""
QuizAttempt }|--|| Student: ""
QuizAttempt }|--|| Quiz: ""
Student ||--|| User: ""
Submission }|--|| Assignment: ""
Submission }|--|| User: ""