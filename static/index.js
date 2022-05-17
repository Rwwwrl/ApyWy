let http_methods = document.querySelectorAll('.http_method')
let method_blocks = document.querySelectorAll('.method_block')


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


for (let [http_method_el, method_block] of zip(http_methods, method_blocks)) {
    let http_method = http_method_el.innerText;
    set_bg_color_by_http_method_value(el=http_method_el, http_method_value=http_method);
    set_bg_color_of_method_block_by_http_method_value(el=method_block, http_method_value=http_method);
    set_border_color_by_http_method_value(el=method_block, http_method_value=http_method);
}

