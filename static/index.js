let http_methods = document.querySelectorAll('.http_method')
let method_blocks = document.querySelectorAll('.method_block')

let http_statuses = document.querySelectorAll('.http_status')
let statuses_blocks = document.querySelectorAll('.status_block')
let response_datas = document.querySelectorAll('.status_response_data_block')

let expected_request_datas = document.querySelectorAll('.expected_request_data')
let expected_request_data_datas = document.querySelectorAll('.expected_request_data_data_block')

const zip = (...arr) => {
    const zipped = [];
    arr.forEach((element, ind) => {
       element.forEach((el, index) => {
          if(!zipped[index]){
             zipped[index] = [];
          };
          if(!zipped[index][ind]){
             zipped[index][ind] = [];
          }
          zipped[index][ind] = el || '';
       })
    });
    return zipped;
 };


function set_bg_color_by_http_method_value(el, http_method_value) {
    // меняем цвет квадрам с методом запроса по его значению
    method_to_color = {
        'GET': 'rgba(44,177,254,255)',
        'POST': 'rgba(0,207,149,255)',
        'PUT': 'rgba(255,156,30,255)',
        'PATCH': 'rgba(255,156,30,255)',
        'DELETE': 'rgba(255,34,35,255)',
    }
    let bg_color = method_to_color[http_method_value]
    el.style.backgroundColor = bg_color;
}

function set_bg_color_of_method_block_by_http_method_value(el, http_method_value) {
    // меняем цвет bd внутри method_block
    method_to_color = {
        'GET': 'rgba(233,243,251,255)',
        'POST': 'rgba(228,247,241,255)',
        'PUT': 'rgba(254,241,230,255)',
        'PATCH': 'rgba(254,241,230,255)',
        'DELETE': 'rgba(255,230,230,255)',
    }
    let bg_color = method_to_color[http_method_value];
    el.style.backgroundColor = bg_color;
}

function set_border_color_by_http_method_value(el, http_method_value) {
    // меняем цвет обводки
    method_to_color = {
        'GET': 'rgba(44,177,254,255)',
        'POST': 'rgba(0,207,149,255)',
        'PUT': 'rgba(255,156,30,255)',
        'PATCH': 'rgba(255,156,30,255)',
        'DELETE': 'rgba(255,34,35,255)',
    }
    let border_color = method_to_color[http_method_value]
    el.style.borderColor = border_color;
}

function set_bg_color_by_status_value(el, http_status_value) {
    ok_statuses = ['200', '201']
    if (ok_statuses.includes(http_status_value)) {
      bg_color = 'rgba(44,177,254,255)'
    }
    else {
      bg_color = 'rgba(255,34,35,255)'
    }
    el.style.backgroundColor = bg_color;
}

function set_bg_color_of_status_block_by_status_value(el, http_status_value) {
    ok_statuses = ['200', '201']
    if (ok_statuses.includes(http_status_value)) {
      bg_color = 'rgba(233,243,251,255)'
    }
    else {
      bg_color = 'rgba(255,230,230,255)'
    }
    el.style.backgroundColor = bg_color;
}

function set_border_color_by_status_value(el, http_status_value) {
    ok_statuses = ['200', '201']
    if (ok_statuses.includes(http_status_value)) {
      border_color = 'rgba(44,177,254,255)'
    }
    else {
      border_color = 'rgba(255,34,35,255)'
    }
    el.style.borderColor = border_color;
}

function colorize_response_data(el, http_status_value) {
    ok_statuses = ['200', '201']
    if (ok_statuses.includes(http_status_value)) {
      bg_color = 'rgba(233,243,251,255)'
      border_color = 'rgba(44,177,254,255)'
    }
    else {
      bg_color = 'rgba(255,230,230,255)'
      border_color = 'rgba(255,34,35,255)'
    }
    el.style.backgroundColor = bg_color;
    el.style.borderColor = border_color;
}

function colorize_request_data(el, http_method_value) {
    method_to_bg_color = {
        'GET': 'rgba(233,243,251,255)',
        'POST': 'rgba(228,247,241,255)',
        'PUT': 'rgba(254,241,230,255)',
        'PATCH': 'rgba(254,241,230,255)',
        'DELETE': 'rgba(255,230,230,255)',
    }
    method_to_border_color = {
        'GET': 'rgba(44,177,254,255)',
        'POST': 'rgba(0,207,149,255)',
        'PUT': 'rgba(255,156,30,255)',
        'PATCH': 'rgba(255,156,30,255)',
        'DELETE': 'rgba(255,34,35,255)',
    }
    bg_color = method_to_bg_color[http_method_value];
    border_color = method_to_border_color[http_method_value];
    el.style.backgroundColor = bg_color;
    el.style.borderColor = border_color;
}

// красим http методы
for (let [http_method_el, method_block_el] of zip(http_methods, method_blocks)) {
    let http_method = http_method_el.innerText;
    set_bg_color_by_http_method_value(el=http_method_el, http_method_value=http_method);
    set_bg_color_of_method_block_by_http_method_value(el=method_block_el, http_method_value=http_method);
    set_border_color_by_http_method_value(el=method_block_el, http_method_value=http_method);
}

// красим http статусы
for (let [http_status_el, status_block_el, response_data_el] of zip(http_statuses, statuses_blocks, response_datas)) {
  let status_code = http_status_el.innerText;
  set_bg_color_by_status_value(el=http_status_el, http_status_value=status_code)
  set_bg_color_of_status_block_by_status_value(el=status_block_el, http_status_value=status_code)
  set_border_color_by_status_value(el=status_block_el, http_status_value=status_code)
  colorize_response_data(el=response_data_el, http_method_value=status_code)
}

// красим request data
for (let [http_method_el, expected_request_data_el, expected_request_data_data_el] of zip(http_methods, expected_request_datas, expected_request_data_datas)) {
    let http_method = http_method_el.innerText;
    set_bg_color_by_http_method_value(el=expected_request_data_el, http_method_value=http_method);
    colorize_request_data(el=expected_request_data_data_el, http_method)
}


// навешиваем собитые onClick по нажатию на статус
for (let [status_block_el, response_data_el] of zip(statuses_blocks, response_datas)) {
  status_block_el.addEventListener('click', () => {
    response_data_el.classList.toggle('hide');
    status_block_el.classList.toggle('hide_request_data');
  })
}

for (let [expected_request_data_el, expected_request_data_data_el] of zip(expected_request_datas, expected_request_data_datas)) {
  expected_request_data_el.addEventListener('click', () => {
    expected_request_data_data_el.classList.toggle('hide');
  })
}
