from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'IT_projects'
app.config['MYSQL_PORT'] = 3306
app.config['SECRET_KEY'] = '0ur_$uper^puper_$ecret_key!'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')    
def getWorkers():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM workers''')
    out_rows = cur.fetchall()
    cur.close()
    return out_rows

@app.route('/Workers')
def workersList():
    workers = getWorkers()
    return render_template('Workers/list.html', Workers = workers)

@app.route('/')
def getProjects():
    cur = mysql.connection.cursor()
    cur.execute("call getProjectsWithNames();")
    projects = cur.fetchall()
    cur.close()
    return projects

@app.route('/')
def getEmployerNames():
    cur = mysql.connection.cursor()
    cur.execute("call employerNames();")
    names = cur.fetchall()
    cur.close()
    return names

@app.route('/')
def getAllEmployerNames():
    cur = mysql.connection.cursor()
    cur.execute("call allEmployerNames();")
    names = cur.fetchall()
    cur.close()
    return names

@app.route('/')
def getAllWorkerNames():
    cur = mysql.connection.cursor()
    cur.execute("call allWorkerNames();")
    names = cur.fetchall()
    cur.close()
    return names

@app.route('/Projects')
def projectsList():
    projects = getProjects()
    return render_template('Projects/list.html', Projects = projects)

@app.route('/')
def getAllProjects():
    cur = mysql.connection.cursor()
    cur.execute("call allProjects();")
    projects = cur.fetchall()
    cur.close()
    return projects

@app.route('/')
def getStages(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM project_stages WHERE project_ID = {0}".format(id)
    cur.execute(query)
    stages = cur.fetchall()
    cur.close()
    return stages

@app.route('/Projects/<int:id>')
def stagesList(id):
    stages = getStages(id)
    return render_template('Stages/list.html', Stages = stages, project_id = id)

@app.route('/')
def getDocuments(id):
    cur = mysql.connection.cursor()
    query = "call getDocumentsWithNames({0});".format(id)
    cur.execute(query)
    documents = cur.fetchall()
    cur.close()
    return documents

@app.route('/Documents/<int:id>')
def documentsList(id):
    documents = getDocuments(id)
    return render_template('Documents/list.html', Documents = documents, project_id = id)

@app.route('/')
def getStageParticipants(id):
    cur = mysql.connection.cursor()
    query = "call getStageParticipantsWithNames({0});".format(id)
    cur.execute(query)
    participants = cur.fetchall()
    cur.close()
    return participants

@app.route('/Stage_participants/<int:id>')
def stageParticipantsList(id):
    participants = getStageParticipants(id)
    return render_template('Stage_participants/list.html', Participants = participants, stage_id = id)

@app.route('/')
def getStageTasks(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM stage_tasks WHERE stage_ID = {0}".format(id)
    cur.execute(query)
    tasks = cur.fetchall()
    cur.close()
    return tasks

@app.route('/Stage_tasks/<int:id>')
def stageTasksList(id):
    tasks = getStageTasks(id)
    return render_template('Stage_tasks/list.html', Tasks=tasks, stage_id = id)

@app.route('/')
def getEmployers():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM employers"
    cur.execute(query)
    employers = cur.fetchall()
    cur.close()
    return employers

@app.route('/Employers')
def employersList():
    employers = getEmployers()
    return render_template('Employers/list.html', Employers = employers)

@app.route('/')
def getMeetings():
    cur = mysql.connection.cursor()
    query = "SELECT meeting_key, meeting_date, project_name FROM projects AS p INNER JOIN meetings AS m ON p.project_key = m.project_ID"
    cur.execute(query)
    meetings = cur.fetchall()
    cur.close()
    return meetings

@app.route('/Meetings')
def meetingsList():
    meetings = getMeetings()
    return render_template('Meetings/list.html', Meetings = meetings)

@app.route('/')
def getAgendas(id):
    cur = mysql.connection.cursor()
    query = "call getAgendasWithNames({0});".format(id)
    cur.execute(query)
    agendas = cur.fetchall()
    cur.close()
    return agendas

@app.route('/Agendas/<int:id>')
def agendasList(id):
    agendas = getAgendas(id)
    return render_template('Agendas/list.html', Agendas = agendas, meeting_id = id)

@app.route('/')
def getMeetingParticipants(id):
    cur = mysql.connection.cursor()
    query = "call getMeetingParticipantsWithID({0});".format(id)
    cur.execute(query)
    participants = cur.fetchall()
    cur.close()
    return participants

@app.route('/Meeting_participants/<int:id>')
def meetingParticipantsList(id):
    participants = getMeetingParticipants(id)
    return render_template('Meeting_participants/list.html', Participants = participants, meeting_id = id)

#--------------------Протокол----------------------------
@app.route('/')
def getProtocol(id):
    cur = mysql.connection.cursor()
    query = "SELECT meeting_date FROM meetings WHERE meeting_key = {0}".format(id)
    cur.execute(query)
    date = cur.fetchone()
    query = "call getAgendasWithNames({0});".format(id)
    cur.execute(query)
    agendas = cur.fetchall()
    query = "call getMeetingParticipants({0});".format(id)
    cur.execute(query)
    participants = cur.fetchall()
    cur.close()
    return date, agendas, participants

@app.route('/Protocol/<int:id>')
def protocolList(id):
    date, agendas, participants = getProtocol(id)
    return render_template('Protocol/list.html', Number = id, Date = date, Agendas = agendas, Participants = participants)
#--------------------------------------------------------------

#--------------------Редактирование----------------------------
@app.route('/')
def getTask(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM stage_tasks WHERE stage_task_key = {0}".format(id)
    cur.execute(query)
    task = cur.fetchone()
    cur.close()
    return task

@app.route('/Stage_tasks/<int:id>/edit', methods=('GET', 'POST'))
def editTask(id):
    """Функция-представление для редактирования задания этапа"""
    task = getTask(id)
    if request.method == 'POST':
        task_name = request.form['title']
        task_description = request.form['content']
        if not task_name:
            flash('Вы не добавили название задачи!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE stage_tasks SET task_name = '{0}', task_description = '{1}' WHERE stage_task_key = {2}".format(task_name, task_description, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('stageTasksList', id=task[3]))
    return render_template('Stage_tasks/edit.html', task = task)

@app.route('/Stage_tasks/<int:id>/delete', methods=('POST',))
def deleteTask(id):
    """Функция-представление для удаления задачи"""
    task = getTask(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM stage_tasks WHERE stage_task_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash("Задача '{0}' успешно удалена!".format(task[1]))
    return redirect(url_for('stageTasksList', id=task[3]))

@app.route('/')
def getStageParticipant(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM stage_participants WHERE stage_participant_key = {0}".format(id)
    cur.execute(query)
    participant = cur.fetchone()
    cur.close()
    return participant

@app.route('/Stage_participants/<int:id>/edit', methods=('GET', 'POST'))
def editStageParticipant(id):
    """Функция-представление для редактирования участника этапа"""
    names = getAllWorkerNames()
    participant = getStageParticipant(id)
    worker = getWorker(participant[3])
    if request.method == 'POST':
        role = request.form['role']
        worker_ID = request.form['worker_ID']
        if not role:
            flash('Вы не указали роль участника!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE stage_participants SET role = '{0}', worker_ID = '{1}' WHERE stage_participant_key = {2}".format(role, worker_ID, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('stageParticipantsList', id=participant[2]))
    return render_template('Stage_participants/edit.html', worker=worker, Names = names, participant=participant)

@app.route('/Stage_participants/<int:id>/delete', methods=('POST',))
def deleteStageParticipant(id):
    """Функция-представление для удаления участника этапа"""
    participant = getStageParticipant(id)
    worker = getWorker(participant[3]) # достаем фамилию участника по id
    cur = mysql.connection.cursor()
    query = "DELETE FROM stage_participants WHERE stage_participant_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Участник "{0}" успешно удален(а)!'.format(worker[1]))
    return redirect(url_for('stageParticipantsList', id=participant[2]))

@app.route('/')
def getMeetingParticipant(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM meeting_participants WHERE meeting_participant_key = {0}".format(id)
    cur.execute(query)
    participant = cur.fetchone()
    cur.close()
    return participant

@app.route('/')
def getWorker(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM workers WHERE worker_key = {0}".format(id)
    cur.execute(query)
    worker = cur.fetchone()
    cur.close()
    return worker

@app.route('/Meeting_participants/<int:id>/edit', methods=('GET', 'POST'))
def editMeetingParticipant(id):
    """Функция-представление для редактирования участника совещания"""
    names = getAllWorkerNames()
    participant = getMeetingParticipant(id)
    worker = getWorker(participant[2])
    if request.method == 'POST':
        worker_ID = request.form['worker_ID']
        cur = mysql.connection.cursor()
        query = "UPDATE meeting_participants SET worker_ID = '{0}' WHERE meeting_participant_key = {1}".format(worker_ID, id)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('meetingParticipantsList', id=participant[1]))
    return render_template('Meeting_participants/edit.html', worker=worker, Names = names)

@app.route('/Meeting_participants/<int:id>/delete', methods=('POST',))
def deleteMeetingParticipant(id):
    """Функция-представление для удаления участника совещания"""
    participant = getMeetingParticipant(id)
    worker = getWorker(participant[2]) # достаем фамилию участника по id
    cur = mysql.connection.cursor()
    query = "DELETE FROM meeting_participants WHERE meeting_participant_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Участник "{0}" успешно удален(а)!'.format(worker[1]))
    return redirect(url_for('meetingParticipantsList', id=participant[1]))

@app.route('/Workers/<int:id>/edit', methods=('GET', 'POST'))
def editWorker(id):
    """Функция-представление для редактирования задания этапа"""
    worker = getWorker(id)
    if request.method == 'POST':
        second_name = request.form['second_name']
        first_name = request.form['first_name']
        father_name = request.form['father_name']
        if not second_name:
            flash('Вы не добавили фамилию!')
        if not first_name:
            flash('Вы не добавили имя!')
        if not father_name:
            flash('Вы не добавили имя!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE workers SET second_name = '{0}', first_name = '{1}', father_name = '{2}' WHERE worker_key = {3}".format(second_name, first_name, father_name, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('workersList'))
    return render_template('Workers/edit.html', worker = worker)

@app.route('/Workers/<int:id>/delete', methods=('POST',))
def deleteWorker(id):
    """Функция-представление для удаления задачи"""
    worker = getWorker(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM workers WHERE worker_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash("Работник '{0}' удален!".format(worker[1]))
    return redirect(url_for('workersList'))

@app.route('/')
def getEmployer(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM employers WHERE employer_key = {0}".format(id)
    cur.execute(query)
    employer = cur.fetchone()
    cur.close()
    return employer

@app.route('/Employers/<int:id>/edit', methods=('GET', 'POST'))
def editEmployer(id):
    """Функция-представление для редактирования заказчика"""
    employer = getEmployer(id)
    if request.method == 'POST':
        employer_name = request.form['employer_name']
        employer_type = request.form['employer_type']
        if not employer_name:
            flash('Вы не добавили наименование заказчика!')
        if not employer_type:
            flash('Вы не добавили тип заказчика!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE employers SET employer_name = '{0}', employer_type = '{1}' WHERE employer_key = {2}".format(employer_name, employer_type, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('employersList'))
    return render_template('Employers/edit.html', employer = employer)

@app.route('/Employers/<int:id>/delete', methods=('POST',))
def deleteEmployer(id):
    """Функция-представление для удаления заказчика"""
    employer = getEmployer(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM employers WHERE employer_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash("Заказчик '{0}' удален!".format(employer[1]))
    return redirect(url_for('employersList'))

@app.route('/')
def getProject(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM projects WHERE project_key = {0}".format(id)
    cur.execute(query)
    project = cur.fetchone()
    cur.close()
    return project

@app.route('/Projects/<int:id>/edit', methods=('GET', 'POST'))
def editProject(id):
    """Функция-представление для редактирования проекта"""
    project = getProject(id)
    names = getAllEmployerNames()
    if request.method == 'POST':
        project_name = request.form['project_name']
        soft_type = request.form['soft_type']
        employer_ID = request.form['employer_ID']
        project_start = request.form['project_start']
        project_end = request.form['project_end']
        project_real_end = request.form['project_real_end']
        if not project_name:
            flash('Вы не добавили название проекта!')
        if not soft_type:
            flash('Вы не добавили тип ПО!')
        if not employer_ID:
            flash('Вы не выбрали заказчика!')
        if not project_start:
            flash('Вы не добавили дату начала проекта!')
        if not project_end:
            flash('Вы не добавили дату окончания проекта!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE projects \
                SET project_name = '{0}', soft_type = '{1}', employer_ID = {2}, project_start = '{3}', project_end = '{4}', project_real_end = '{5}' \
                WHERE project_key = {6}".format(project_name, soft_type, employer_ID, project_start, project_end, project_real_end, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('projectsList'))
    return render_template('Projects/edit.html', project = project, Names = names)

@app.route('/Projects/<int:id>/delete', methods=('POST',))
def deleteProject(id):
    """Функция-представление для удаления заказчика"""
    project = getProject(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM projects WHERE project_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash("Проект '{0}' удален!".format(project[1]))
    return redirect(url_for('projectsList'))

@app.route('/')
def getStage(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM project_stages WHERE project_stage_key = {0}".format(id)
    cur.execute(query)
    stage = cur.fetchone()
    cur.close()
    return stage

@app.route('/Stages/<int:id>/edit', methods=('GET', 'POST'))
def editStage(id):
    """Функция-представление для редактирования этапа"""
    stage = getStage(id)
    if request.method == 'POST':
        stage_name = request.form['stage_name']
        stage_cost = request.form['stage_cost']
        stage_start = request.form['stage_start']
        stage_end = request.form['stage_end']
        finish_form = request.form['finish_form']
        if not stage_name:
            flash('Вы не добавили название этапа!')
        if not stage_cost:
            flash('Вы не указали стоимость этапа!')
        if not stage_start:
            flash('Вы не добавили дату начала этапа!')
        if not stage_end:
            flash('Вы не добавили дату окончания этапа!')
        if not finish_form:
            flash('Вы не указали форму сдачи этапа!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE project_stages \
                SET stage_name = '{0}', stage_cost = {1}, stage_start = '{2}', stage_end = '{3}', finish_form = '{4}' \
                WHERE project_stage_key = {5}".format(stage_name, stage_cost, stage_start, stage_end, finish_form, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('stagesList', id=stage[6]))
    return render_template('Stages/edit.html', stage = stage)

@app.route('/Stages/<int:id>/delete', methods=('POST',))
def deleteStage(id):
    """Функция-представление для удаления заказчика"""
    stage = getStage(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM project_stages WHERE project_stage_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Этап "{0}" удален!'.format(stage[1]))
    return redirect(url_for('stagesList', id=stage[6]))

@app.route('/')
def getDocument(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM project_documents WHERE project_document_key = {0}".format(id)
    cur.execute(query)
    document = cur.fetchone()
    cur.close()
    return document

@app.route('/Documents/<int:id>/edit', methods=('GET', 'POST'))
def editDocument(id):
    """Функция-представление для редактирования документа"""
    document = getDocument(id)
    names = getAllWorkerNames()
    if request.method == 'POST':
        document_name = request.form['document_name']
        document_status = request.form['document_status']
        change_status_date = request.form['change_status_date']
        document_developer = request.form['document_developer']			
        if not document_name:
            flash('Вы не добавили название документа!')
        if not document_developer:
            flash('Вы не указали разработчика документа!')
        if not document_status:
            flash('Вы не указали статус документа!')
        else:
            cur = mysql.connection.cursor()
            query = "UPDATE project_documents \
                SET document_name = '{0}', document_status = '{1}', change_status_date = '{2}', document_developer = {3} \
                WHERE project_document_key = {4}".format(document_name, document_status, change_status_date, document_developer, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('documentsList', id=document[2]))
    return render_template('Documents/edit.html', document=document, Names = names)

@app.route('/Documents/<int:id>/delete', methods=('POST',))
def deleteDocument(id):
    """Функция-представление для удаления заказчика"""
    document = getDocument(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM project_documents WHERE project_document_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Документ "{0}" удален!'.format(document[1]))
    return redirect(url_for('documentsList', id=document[2]))

@app.route('/')
def getMeeting(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM meetings WHERE meeting_key = {0}".format(id)
    cur.execute(query)
    meeting = cur.fetchone()
    cur.close()
    return meeting

@app.route('/Meeetings/<int:id>/edit', methods=('GET', 'POST'))
def editMeeting(id):
    """Функция-представление для редактирования совещания"""
    meeting = getMeeting(id)
    projects = getAllProjects()
    if request.method == 'POST':
        meeting_date = request.form['meeting_date']
        project_ID = request.form['project_ID']		
        cur = mysql.connection.cursor()
        query = "UPDATE meetings \
            SET meeting_date = '{0}', project_ID = {1} \
            WHERE meeting_key = {2}".format(meeting_date, project_ID, id)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('meetingsList'))
    return render_template('Meetings/edit.html', meeting=meeting, Projects=projects)

@app.route('/Meetings/<int:id>/delete', methods=('POST',))
def deleteMeeting(id):
    """Функция-представление для удаления совещания"""
    meeting = getMeeting(id)
    project = getProject(meeting[2])
    cur = mysql.connection.cursor()
    query = "DELETE FROM meetings WHERE meeting_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Совещание по проекту "{0}" от {1} удалено!'.format(project[1], meeting[1]))
    return redirect(url_for('meetingsList'))

@app.route('/')
def getAgenda(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM agendas WHERE agenda_key = {0}".format(id)
    cur.execute(query)
    agenda = cur.fetchone()
    cur.close()
    return agenda

@app.route('/Agendas/<int:id>/edit', methods=('GET', 'POST'))
def editAgenda(id):
    """Функция-представление для редактирования документа"""
    agenda = getAgenda(id)
    names = getAllWorkerNames()
    if request.method == 'POST':
        agenda_item = request.form['agenda_item']
        agenda_decision = request.form['agenda_decision']
        execution_date = request.form['execution_date']
        completion_date = request.form['completion_date']
        responsible = request.form['responsible']
        if completion_date == "0000-00-00":
            completion_date = "None"
        cur = mysql.connection.cursor()
        query = "UPDATE agendas \
            SET agenda_item = '{0}', agenda_decision = '{1}', execution_date = '{2}', completion_date = '{3}', responsible = {4} \
            WHERE agenda_key = {5}".format(agenda_item, agenda_decision, execution_date, completion_date, responsible, id)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('agendasList', id=agenda[5]))
    return render_template('Agendas/edit.html', agenda=agenda, Names=names)

@app.route('/Agendas/<int:id>/delete', methods=('POST',))
def deleteAgenda(id):
    """Функция-представление для удаления вопроса повестки дня"""
    agenda = getAgenda(id)
    cur = mysql.connection.cursor()
    query = "DELETE FROM agendas WHERE agenda_key = {0}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('Вопрос "{0}" удален!'.format(agenda[1]))
    return redirect(url_for('agendasList', id=agenda[5]))

#--------------------Создание----------------------------
@app.route('/Projects/create', methods=('GET', 'POST'))
def createProject():
    """Функция-представление для создания проекта"""
    names = getAllEmployerNames()
    if request.method == 'POST':
        project_name = request.form['project_name']
        soft_type = request.form['soft_type']
        employer_ID = request.form['employer_ID']
        project_start = request.form['project_start']
        project_end = request.form['project_end']
        if not project_name:
            flash('Вы не добавили название проекта!')
        if not soft_type:
            flash('Вы не добавили тип ПО!')
        if not employer_ID:
            flash('Вы не выбрали заказчика!')
        if not project_start:
            flash('Вы не добавили дату начала проекта!')
        if not project_end:
            flash('Вы не добавили дату окончания проекта!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO projects (project_name, soft_type, employer_ID, project_start, project_end) VALUES ('{0}', '{1}', {2}, '{3}', '{4}')"\
                .format(project_name, soft_type, employer_ID, project_start, project_end)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Проект "{0}" создан!'.format(project_name))
            return redirect(url_for('projectsList'))
    return render_template('Projects/create.html', Names = names)

@app.route('/Documents/<int:id>/create', methods=('GET', 'POST'))
def createDocument(id):
    """Функция-представление для создания документа по проекту"""
    names = getAllWorkerNames()
    if request.method == 'POST':
        document_name = request.form['document_name']
        document_status = request.form['document_status']
        change_status_date = request.form['change_status_date']
        document_developer = request.form['document_developer']			
        if not document_name:
            flash('Вы не добавили название документа!')
        if not document_developer:
            flash('Вы не указали разработчика документа!')
        if not document_status:
            flash('Вы не указали статус документа!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO project_documents (document_name, document_status, change_status_date, document_developer, project_ID) \
                VALUES ('{0}', '{1}', '{2}', {3}, {4})"\
                .format(document_name, document_status, change_status_date, document_developer, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Документ "{0}" создан!'.format(document_name))
            return redirect(url_for('documentsList', id=id))
    return render_template('Documents/create.html', Names = names)

@app.route('/Stages/<int:id>/create', methods=('GET', 'POST'))
def createStage(id):
    """Функция-представление для создания этапа проекта"""
    if request.method == 'POST':
        stage_name = request.form['stage_name']
        stage_cost = request.form['stage_cost']
        stage_start = request.form['stage_start']
        stage_end = request.form['stage_end']
        finish_form = request.form['finish_form']
        if not stage_name:
            flash('Вы не добавили название этапа!')
        if not stage_cost:
            flash('Вы не указали стоимость этапа!')
        if not stage_start:
            flash('Вы не добавили дату начала этапа!')
        if not stage_end:
            flash('Вы не добавили дату окончания этапа!')
        if not stage_end:
            flash('Вы не добавили дату окончания этапа!')
        if not finish_form:
            flash('Вы не указали форму сдачи этапа!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO project_stages (stage_name, stage_cost, stage_start, stage_end, finish_form, project_ID) VALUES ('{0}', {1}, '{2}', '{3}', '{4}', {5})"\
                .format(stage_name, stage_cost, stage_start, stage_end, finish_form, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Этап "{0}" создан!'.format(stage_name))
            return redirect(url_for('stagesList', id = id))
    return render_template('Stages/create.html')

@app.route('/Stage_tasks/<int:id>/create', methods=('GET', 'POST'))
def createTask(id):
    """Функция-представление для создания задачи """
    if request.method == 'POST':
        task_name = request.form['title']
        task_description = request.form['content']
        if not task_name:
            flash('Вы не добавили заголовок!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO stage_tasks (task_name, task_description, stage_ID) VALUES ('{0}', '{1}', {2})".format(task_name, task_description, id)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Задание "{0}" создано!'.format(task_name))
            return redirect(url_for('stageTasksList', id=id))
    return render_template('Stage_tasks/create.html')

@app.route('/Stage_participants/<int:id>/create', methods=('GET', 'POST'))
def addStageParticipant(id):
    """Функция-представление для добавления участника этапа"""
    names = getAllWorkerNames()
    if request.method == 'POST':
        role = request.form['role']
        worker_ID = request.form['worker_ID']
        if not role:
            flash('Вы не указали роль участника!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO stage_participants (role, stage_ID, worker_ID) VALUES ('{0}', {1}, {2})"\
                .format(role, id, worker_ID)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            worker = getWorker(worker_ID) 
            flash('Участник "{0}" добавлен(а)!'.format(worker[1]))
            return redirect(url_for('stageParticipantsList', id=id))
    return render_template('Stage_participants/create.html', Names = names)

@app.route('/Meeting_participants/<int:id>/create', methods=('GET', 'POST'))
def addMeetingParticipant(id):
    """Функция-представление для добавления участника совещания"""
    names = getAllWorkerNames()
    if request.method == 'POST':
        worker_ID = request.form['worker_ID']
        cur = mysql.connection.cursor()
        query = "INSERT INTO meeting_participants (meetings_ID, worker_ID) VALUES ({0}, {1})"\
            .format(id, worker_ID)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        worker = getWorker(worker_ID) 
        flash('Участник "{0}" добавлен(а)!'.format(worker[1]))
        return redirect(url_for('meetingParticipantsList', id=id))
    return render_template('Meeting_participants/create.html', Names = names)

@app.route('/Workers/create', methods=('GET', 'POST'))
def addWorker():
    """Функция-представление для добавления работника"""
    if request.method == 'POST':
        second_name = request.form['second_name']
        first_name = request.form['first_name']
        father_name = request.form['father_name']
        if not second_name:
            flash('Вы не добавили фамилию!')
        if not first_name:
            flash('Вы не добавили имя!')
        if not father_name:
            flash('Вы не добавили отчество!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO workers (second_name, first_name, father_name) VALUES ('{0}', '{1}', '{2}')".format(second_name, first_name, father_name)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Работник "{0}" добавлен(а)!'.format(second_name))
            return redirect(url_for('workersList'))
    return render_template('Workers/create.html')

@app.route('/Employers/create', methods=('GET', 'POST'))
def addEmployer():
    """Функция-представление для добавления заказчика"""
    if request.method == 'POST':
        employer_name = request.form['employer_name']
        employer_type = request.form['employer_type']
        if not employer_name:
            flash('Вы не добавили наименование заказчика!')
        if not employer_type:
            flash('Вы не добавили тип заказчика!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO employers (employer_name, employer_type) VALUES ('{0}', '{1}')".format(employer_name, employer_type)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Заказчик "{0}" добавлен!'.format(employer_name))
            return redirect(url_for('employersList'))
    return render_template('Employers/create.html')

@app.route('/Meetings/create', methods=('GET', 'POST'))
def createMeeting():
    """Функция-представление для добавления участника этапа"""
    projects = getAllProjects()
    if request.method == 'POST':
        meeting_date = request.form['meeting_date']
        project_ID = request.form['project_ID']
        cur = mysql.connection.cursor()
        query = "INSERT INTO meetings (meeting_date, project_ID) VALUES ('{0}', {1})"\
            .format(meeting_date, project_ID)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        project = getProject(project_ID)
        flash('Собрание по проекту "{0}" запланировано на {1}!'.format(project[1], meeting_date))
        return redirect(url_for('meetingsList'))
    return render_template('Meetings/create.html', Projects = projects)

@app.route('/Agendas/<int:id>/create', methods=('GET', 'POST'))
def createAgenda(id):
    """Функция-представление для создания этапа вопроса к повестке дня"""	
    names = getAllWorkerNames()
    if request.method == 'POST':
        agenda_item = request.form['agenda_item']
        agenda_decision = request.form['agenda_decision']
        execution_date = request.form['execution_date']
        responsible = request.form['responsible']
        if not agenda_item:
            flash('Вы не добавили вопрос!')
        if not agenda_decision:
            flash('Вы не указали решение по вопросу!')
        if not responsible:
            flash('Вы не добавили ответственного за исполнение!')
        else:
            cur = mysql.connection.cursor()
            query = "INSERT INTO agendas (agenda_item, agenda_decision, execution_date, meeting_ID, responsible) \
                VALUES ('{0}', '{1}', '{2}', {3}, {4})"\
                    .format(agenda_item, agenda_decision, execution_date, id, responsible)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flash('Вопрос "{0}" создан!'.format(agenda_item))
            return redirect(url_for('agendasList', id=id))
    return render_template('Agendas/create.html', Names = names)

app.run(debug=True)