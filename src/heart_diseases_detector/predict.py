import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, Response
from werkzeug.security import check_password_hash, generate_password_hash
from heart_diseases_detector.db import get_db

bp = Blueprint('predict', __name__, url_prefix='/')

PARAMS_DICT = {
    'sex': [
        'Пол',
        ['Мужской', 'Женский']
    ],

    'age': [
        'Возраст',
        0,
        100
    ],

    'cp': [
        'Боль в груди',
        ['Отсутствуют', 'Типичная стенокардия', 'Атипичная стенокардия', 'Боли, не связанные с стенокардией']
    ],

    'trestbps': [
        'Давление в покое (мм рт. ст.)',
        50,
        200
    ],

    'chol': [
        'Уровень сывороточного холестерина (в мг/дл)',
        100,
        700
    ],

    'fbs': [
        'Уровень сахара в крови натощак (в мг/дл)',
        0,
        300
    ],

    'restecg': [
        'Результаты ЭКГ в покое',
        ['В норме', 'Аномалия зубца ST-T', 'Гипертрофия левого желудочка', 'Другое']
    ],

    'thalach': [
        'Максимальный пульс (уд/мин)',
        0,
        220
    ],

    'exang': [
        'Выявляется ли стенокардия при нагрузке',
        ['Нет', 'Да']
    ],

    'oldpeak': [
        'Уровень депрессии ST-сегмента после физической нагрузки',
        0,
        10
    ],

    'slope': [
        'Наклон ST-сегмента при максимальной физической нагрузке',
        ['Ровный', 'Наклон вверх', 'Наклон вниз']
    ],

    'ca': [
        'Количество крупных сосудов, выявленных при рентгеноскопии',
        ['0', '1', '2', '3']
    ],

    'thal': [
        'Тип талассемии',
        ['Нормальный', 'Исправленный дефект', 'Обратимый дефект']
    ]
}

MODEL_COLUMNS = [
    'age',
    'sex',
    'cp',
    'trestbps',
    'chol',
    'fbs',
    'restecg',
    'thalach',
    'exang',
    'oldpeak',
    'slope',
    'ca',
    'thal'
]

SEX_POSSIBLE = ['Мужской', 'Женский']
CP_POSSIBLE = ['Отсутствуют', 'Типичная стенокардия', 'Атипичная стенокардия', 'Боли, не связанные с стенокардией']

@bp.route('/predict', methods=['POST'])
def predict():
    request_data = request.get_json()
    print(request_data)

    is_input_correct, resp = _validate_input(request_data)
    if not is_input_correct:
        return resp
    
    return render_template('heart/result.html')

def _validate_input(req: dict) -> [bool, Response]:
    is_all_columns_in_request = _check_all_params_are_presented_in_req(req)

    if not is_all_columns_in_request:
        return False, Response(
            "В запросе отправлены не все колонки",
            status=400,
        )
    
    is_all_fields_correct, err_msg = _validate_all_params(req)
    if not is_all_fields_correct:
        return False, Response(
            err_msg,
            status=400
        )

    return True, None 

def _check_all_params_are_presented_in_req(params: dict) -> bool:
    for col in MODEL_COLUMNS:
        if col not in params:
            return False
    
    return True

def _validate_all_params(params: dict) -> (bool, str):
    is_age_valid, err_msg = _validate_integer_vars(params['age'], 'age')
    if not is_age_valid:
        return False, err_msg
    
    is_sex_valid, err_msg = _validate_listed_vars(params['sex'], 'sex')
    if not is_sex_valid:
        return False, err_msg

    is_cp_valid, err_msg = _validate_listed_vars(params['cp'], 'cp')
    if not is_cp_valid:
        return False, err_msg
    
    is_trestbps_valid, err_msg = _validate_integer_vars(params['trestbps'], 'trestbps')
    if not is_trestbps_valid:
        return False, err_msg

    is_chol_valid, err_msg = _validate_integer_vars(params['chol'], 'chol')
    if not is_chol_valid:
        return False, err_msg
    
    is_trestbps_valid, err_msg = _validate_integer_vars(params['fbs'], 'fbs')
    if not is_trestbps_valid:
        return False, err_msg

    is_restecg_valid, err_msg = _validate_listed_vars(params['restecg'], 'restecg')
    if not is_restecg_valid:
        return False, err_msg
    
    is_thalach_valid, err_msg = _validate_integer_vars(params['thalach'], 'thalach')
    if not is_thalach_valid:
        return False, err_msg

    is_exang_valid, err_msg = _validate_listed_vars(params['exang'], 'exang')
    if not is_exang_valid:
        return False, err_msg
    
    is_oldpeak_valid, err_msg = _validate_float_vars(params['oldpeak'], 'oldpeak')
    if not is_oldpeak_valid:
        return False, err_msg

    is_slope_valid, err_msg = _validate_listed_vars(params['slope'], 'slope')
    if not is_slope_valid:
        return False, err_msg
    
    is_ca_valid, err_msg = _validate_listed_vars(params['ca'], 'ca')
    if not is_ca_valid:
        return False, err_msg

    is_thal_valid, err_msg = _validate_listed_vars(params['thal'], 'thal')
    if not is_thal_valid:
        return False, err_msg
    
    return True, ''

def _validate_listed_vars(var: str, dict_header: str) -> (bool, str):
    data = PARAMS_DICT[dict_header]

    if len(data) != 2:
        return False, 'Проблемы на стороне сервера'

    var_str = data[0]
    list_of_possible_values = data[1]

    if var not in list_of_possible_values:
        return False, f'{var_str} может быть только следующих значений: {list_of_possible_values}'
    
    return True, ''

def _validate_integer_vars(var: str, dict_header: str) -> (bool, str):
    data = PARAMS_DICT[dict_header]
    
    if len(data) != 3:
        return False, 'Проблемы на стороне сервера'

    var_str = data[0]
    min_value = data[1]
    max_value = data[2]

    try:
        int_var = int(var)
        if int_var < min_value:
            return False, f'Параметр {var_str} не должен быть меньше чем {min_value}'
        
        if int_var > max_value:
            return False, f'Параметр {var_str} не должен быть больше чем {max_value}'
        
        return True, ''
    
    except:
        return False, f'Параметр {var_str} должен быть целым числом'

def _validate_float_vars(var: str, dict_header: str) -> (bool, str):
    data = PARAMS_DICT[dict_header]
    
    if len(data) != 3:
        return False, 'Проблемы на стороне сервера'

    var_str = data[0]
    min_value = data[1]
    max_value = data[2]

    try:
        int_var = float(var)
        if int_var < min_value:
            return False, f'Параметр {var_str} не должен быть меньше чем {min_value}'
        
        if int_var > max_value:
            return False, f'Параметр {var_str} не должен быть больше чем {max_value}'
        
        return True, ''
    
    except:
        return False, f'Параметр {var_str} должен быть дробным числом'

