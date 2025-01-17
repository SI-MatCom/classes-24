
import json
import random

import subprocess
import os

################################################################
### Funciones para seleccionar las preguntas del examen
################################################################

def _read_json(filename='./DB-questions.json'):
    """
    Load in JSON file

    Arg:
        filename: str 
             Path of the JSON file to read. By default, './DB-questions.json' is assumed.

    Return:
        dict 

    Exceptions:
        FileNotFoundError: Thrown if the specified file cannot be found.
        json.JSONDecodeError: Thrown if there is an error decoding the JSON.
        IOError: Thrown if there is an error opening or reading the file.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error al decodificar el JSON en el archivo: {filename}", e.doc, e.pos)
    except IOError as e:
        raise IOError(f"Error al abrir o leer el archivo: {filename}", e.errno)

def _filter_by_topic(data, topics_id, key):
    """
    Select a set such that the key belongs to a defined group

    Args:
        data: list<dict>
            List of dictionaries to filter.
        topics_id: list<str>
            List of topic id considered valid.
        key: str
            Name of the field by which it will be filtered.

    Return:
        list<dict>
     
    """
    return [item for item in data if item[key] in topics_id]

def _generate_exam(data, n_questions, topics, number_of_questions_per_topic):
    """
    Randomly selects a set of elements and rearranges some elements internal to the selected elements
    
    Args:
        data: list<dict>
            List of questions in the form of dictionaries.
        n_questions: int
            Number of itmes to select.
        topics: list<int>
            List of topic identifiers that will be used to filter questions.
        number_of_questions_per_topic: int
            Minimum number of questions per topic
    
    Return: 
        list<dict>
    
    """
    # selected_data = []
    # while not _validate_exam(selected_data, topics, number_of_questions_per_topic):
    #     selected_data = random.sample(data, n_questions)
    
    # # desordenar las opciones
    # for item in selected_data:
    #     len_ = len(item['options'])
    #     permutation = random.sample(range(len_), len_)
    #     item['options'] = [item['options'][i] for i in permutation]
    #     item['answers'] = [item['answers'][i] for i in permutation]
    
    # return selected_data
    
    selected_data = []
    
    # Ensure all topics are included with at least the minimum number of questions
    for topic in topics:
        topic_questions = [q for q in data if q['topic_id'] == topic]
        if len(topic_questions) < number_of_questions_per_topic:
            # Handle case where there aren't enough questions for a topic
            raise ValueError(f"Not enough questions for topic {topic}")
        
        selected_data.extend(random.sample(topic_questions, k=number_of_questions_per_topic))

    # Fill remaining questions with random selections from any topic
    remaining_questions = n_questions - len(selected_data)
    available_questions = [q for q in data if q not in selected_data]
    selected_data.extend(random.sample(available_questions, k=remaining_questions))

    return _shuffle_options_and_answers(selected_data)
    
def _shuffle_options_and_answers(selected_data):
    """Shuffle options and answers within each question

    Args:
        selected_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    for item in selected_data:
        len_ = len(item['options'])
        permutation = random.sample(range(len_), len_)
        item['options'] = [item['options'][i] for i in permutation]
        item['answers'] = [item['answers'][i] for i in permutation]

    random.shuffle(selected_data)
    return selected_data


 
def generates_exams(data, amount_of_question_per_test, amount_of_tests, topics_id, number_of_questions_per_topic):
    """
    Generate tests from a data set

    Parámetros:
        data: list<dict>
            List of questions.
        amount_of_question_per_test: int
            Number of questions per exam.
        amount_of_tests: int
            Total number of exams to generate.
        topics_id: list
            List of topic identifiers that will be used to filter questions.
        number_of_questions_per_topic: int
            Minimum number of questions per topic

    Return:
        list<dict>

    """
    valid_questions = _filter_by_topic(data, topics, 'topic_id')
    tests = []
    
    for _ in range(amount_of_tests):
        tests.append(_generate_exam(data, amount_of_question_per_test, topics, number_of_questions_per_topic))
    
    return tests
    
################################################################


################################################################
### Funciones para generar el fichero .tex
################################################################

preamble_code = """
\\documentclass[10pt]{exam}

\\usepackage[top=0.5in, bottom=1in, left=0.7in, right=0.7in]{geometry}

\\usepackage{multicol}
\\usepackage{graphicx}
\\usepackage{enumitem}

%\\usepackage{xcolor}

\\pagestyle{empty}

\\setlength{\\columnsep}{20pt}
\\renewcommand{\choicelabel}{\\alph{choice})}
%\\raggedright

\\usepackage{tikz}
\\usepackage{qrcode}

\\makeatletter
\\renewenvironment{choices}
{\\list{\\choicelabel}
    {\\usecounter{choice}\\def\\makelabel##1{\\hss\\llap{##1}}%
        \\setlength{\\leftmargin}{15pt}
        \\def\\choice{
            \\if@correctchoice
            \\color@endgroup
            \\endgroup
            \\fi
            \\item
            \\do@choice@pageinfo
        } 
        \\def\\CorrectChoice{
            \\if@correctchoice
            \\color@endgroup
            \\endgroup
            \\fi
            \\ifprintanswers
            \\ifhmode \\unskip\\unskip\\unvbox\\voidb@x \\fi
            \\begingroup \\color@begingroup \\@correctchoicetrue
            \\CorrectChoice@Emphasis
            \\fi
            \\item
            \\do@choice@pageinfo
        } 
        \\let\\correctchoice\\CorrectChoice
        \\labelwidth\\leftmargin\\advance\\labelwidth-\\labelsep
        \\topsep=0pt
        \\partopsep=0pt
        \\choiceshook
    }
}
{\\if@correctchoice \\color@endgroup \\endgroup \\fi \\endlist}
\\makeatother


\\newcommand{\\encabezado}[3]{
    
    \\begin{minipage}[c]{0.55\\textwidth}
        \\begin{centering}
            Trabajo de Control \\\\
            Sistemas de Recuperación de Información \\\\
            %Facultad de Matemática y Computación. UH \\\\
            Fecha: #1 \\\\
            Temario \\##3
            
        \\end{centering}
 
    \\end{minipage}%
    \\begin{minipage}[c]{0.35\\textwidth}
        \\begin{centering}
            \\begin{tikzpicture}
                \\node[anchor=north east, inner sep=0pt] at (current page.north east) {\\qrcode{#2}};
            \\end{tikzpicture}
            
        \\end{centering}
    \\end{minipage}
    
    \\vspace{1\\baselineskip}
  
    Nombre: \\underline{\\hspace{10cm}}  
    Grupo: \\underline{\\hspace{2cm}} 
        
    \\vspace{1\\baselineskip}
    Seleccione en cada caso la(s) respuesta(s) correcta(s). Considere también no marcar ninguna opción.
}

\\begin{document}
    
    %\\color{blue}
     
    my_questions
    
\\end{document}
 
"""

def _change_format_question(question):
    """
   Change the question to latex format and get the correct answers

    Arg:
        question: dict
             A dictionary containing the question statement and options.
     
    Return:
        (str, str)

    """
    code = "\\question " + question['statement'] + '\n'
    code += "\\begin{choices}" + '\n'
    
    code += '\n'.join("\\choice " + option for option in question['options'])
    # for o, a in zip(question['options'], question['answers']):
    #     if a:
    #         code += '\n \\choice \\textbf{' + o + '}'
    #     else:
    #         code += '\n \\choice ' + o
    
    code += '\n' + "\\end{choices}"
    return code, str(question['answers'])
    
def _change_format_exam(questions, date, num):
    """
    Create a test in LaTeX format from a list of questions.

    Parámetros:
        questions: list<dict>
            List of questions.
        date: str
			Day of exam.
        num: int
            Exam number generated

    Retorna:
        str
        
    """
    code_questions = ''
    answers = ''
    for (i, question) in enumerate(questions):
        qlatex, answer = _change_format_question(question)
        code_questions += qlatex + '\n'
        answers += str(i + 1) + ': ' + answer + '\\\\'
        
    code = '\\encabezado{' + date +'}{' + answers + '}{' + str(num) + '}\n'
    code += '\\begin{questions}' + '\n'
    code += '\\begin{multicols}{2}' + '\n'
    code += '\n' + code_questions + '\n'
    code += '\\end{multicols}' + '\n'
    code += '\\end{questions}' + '\n' + '\\newpage'
    return code

def _delete_files_extensions(dir='./'):
    """
    Delete files generated when compiling Latex

    Args:
        dir (str, optional): 
              Path folder where the file will be compiled. Defaults to './'.
    
    """
    
    files = os.listdir(dir)
    extensions_to_remove = ['.aux', '.log', '.synctex.gz']
    
    for file in files:
        name, ext = os.path.splitext(file)
        if ext in extensions_to_remove:
            ruta_completa = os.path.join(dir, file)
            os.remove(ruta_completa)
            print(f"Archivo eliminado: {ruta_completa}")


def _change_format_document(tests, date):
    """
    Create a LaTeX document

    Args:
        tests: list<list<dict>>
            Exam list.
        date: str
            Date to include in the document

    Return:
        str
    
    """
    
    global preamble_code
    
    tests_latex = '\n'.join([_change_format_exam(test, date, i + 1) for i, test in enumerate(tests)])
    tests_latex = tests_latex[:-9]
    
    return preamble_code.replace('my_date', date).replace('my_questions', tests_latex)
    
def create_pdf(tests, date, doc_name, dir='.'):
    """
    Create a PDF document with a set of exams

    Args:
        tests (list<dict>): 
        	List of exams. Each dictionary will have:
				'topic_id': int,
				'subtopic_id': int,
				'statement': str,
				'options': list<str>,
				"answers": list<str>
        date (str): 
        	Date of each exam.
        doc_name (str): 
        	Output file name without the extension.
        dir (str, optional): 
        	Output directory of the PDF file. By default it is the current directory.

    """
    
    doc = os.path.join(dir, doc_name + '.tex')
    latex_code = _change_format_document(tests, date)
    
    with open(doc, 'w') as file_text:
        file_text.write(latex_code)

    try:
        subprocess.run(['pdflatex', doc])
        _delete_files_extensions(dir)
    except Exception as e:
        print('Error al compilar el documento LaTeX:', e)


################################################################

data = _read_json('./DB-questions.json')
amount_of_question_per_test = 20
amount_of_tests = 29 + 33 + 10
topics = [6, 7, 8, 9, 10]
number_of_questions_per_topic = 2

tests = generates_exams(data['questions'], amount_of_question_per_test, amount_of_tests, topics, number_of_questions_per_topic)
create_pdf(tests, '15 de julio de 2024', 'SRI-Parcial', '.')