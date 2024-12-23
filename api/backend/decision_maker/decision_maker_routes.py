from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

#------------------------------------------------------------
# decision maker blueprint
# Contains routes for decision maker functionalities
decision_maker = Blueprint('decision_maker', __name__)

#------------------------------------------------------------
# decision maker routes

# Route: Insights on student engagement with modules
@decision_maker.route('/engagement', methods=['GET'])
def get_student_engagement():
    query = '''
        SELECT lp.module_name, COUNT(p.id) AS engaged_students
        FROM learning_path lp
        LEFT JOIN progress p ON lp.id = p.path_id
        GROUP BY lp.module_name
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Route: Visualization of student progress over time
@decision_maker.route('/progress/<int:mentee_id>', methods=['GET'])
def get_student_progress(mentee_id):
    query = '''
        SELECT mentee_id, status, completion_date
        FROM progress
        WHERE mentee_id = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (mentee_id,))
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Route: Review and organize student feedback
@decision_maker.route('/feedback', methods=['GET'])
def get_student_feedback():
    query = '''
        SELECT f.description AS feedback, f.session_id, s.purpose, s.date
        FROM feedback f
        JOIN session s ON f.session_id = s.id
        WHERE s.date > CURRENT_DATE - INTERVAL 30 DAY
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Route: Automated reports on cultural competence trends
@decision_maker.route('/trends', methods=['GET'])
def get_cultural_competence_trends():
    query = '''
        SELECT lp.module_name, COUNT(p.id) AS completions, 
               AVG(DATEDIFF(p.completion_date, lp.last_updated)) AS avg_completion_time
        FROM learning_path lp
        JOIN progress p ON lp.id = p.path_id
        GROUP BY lp.module_name
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Route: Track completion rates by student demographics
@decision_maker.route('/completion-rates', methods=['GET'])
def get_completion_rates():
    query = '''
        SELECT mentee_id, COUNT(p.id) AS total_completions
        FROM progress p
        WHERE p.status = 'Completed'
        GROUP BY mentee_id
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# Route: Correlations between module performance and success
@decision_maker.route('/correlations', methods=['GET'])
def get_module_performance_correlations():
    query = '''
        SELECT lp.module_name, p.status, s.purpose
        FROM learning_path lp
        JOIN progress p ON lp.id = p.path_id
        JOIN session s ON p.mentee_id = s.mentee_id
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
