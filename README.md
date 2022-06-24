# ApyWy - аналог Swagger

Основную проблему, которую решает _ApyWy_ - большое количество времени разработчика для написания схемы (_schema_) для класса _View_. В моей версии мы можем использовать обычные питоновские словари для обозначения ожидаемых данные и ожидаемого ответа.

## Пример не настроенной версии apywy:

![alt](static_images/default_apywy.png)

## Пример настроенной версии apywy:

*Тут для примера настроен только *GET* метод.*

![alt](static_images/configured_apywy.gif)

## Установка

1. Добавляем в _settings.INSTALLED_APPS_:

```python
INSTALLED_APPS = [
    ...
    'apywy.api',
    ...
]
```

2. Добавляем в _urls.py_ главного приложения:

```python
path('apywy/', include(('apywy.api.urls', 'apywy.api'), namespace='apywy')),
```

3. **Готово**, на главной странице _ApyWy_ - **_/apywy/_** есть вся возможная информация без дополнительных настроек.

## Настройка

По умолчанию, все что мы можем узнать для джанго-вьюшки:

- Url-путь до _http-метода_.
- Док-стринг для вьюшки, а также для всех ее _http-методов_ (_get_, _post_, ...).

Но мы можем это исправить, построив _ApyWy_ схему для вьюшки.

Наш файл _views.py_:

```python
# views.py
class HomePageView(APIView):
    '''
    HomePageView doc string
    '''

    def get(self, request, some_quary):
        'HomePageView.get doc string'

        if some_quary == 'some value':
            return Response({'ANSWER': 'GET-INVALID-RESULT'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'ANSWER': 'GET-RESULT'}, status=status.HTTP_200_OK)

    def post(self, request):
        'HomePageView.post doc string'
        return Response({'ANSWER': 'POST-RESULT'}, status=status.HTTP_201_CREATED)
```

- Создаем файл _apywy_schemas.py_ (имя не важно)

```python
# apywy_schemas.py
from apywy.fields import StatusField, MethodField, RequestDataField
from apywy.schema import Schema

from apywy.constants.const import Constant


class HomePageSchema(Schema):
    class GET(MethodField):

        HTTP_200 = StatusField(expected_response_data=Constant({'ANSWER': 'GET-RESULT'}))

        HTTP_500 = StatusField(expected_response_data=Constant({'ANSWER': 'GET-INVALID-RESULT'}))

```

- Навешиваем эту схему на view:

```python
# views.py
...
from apywy.decorators import set_apywy_schema

from .apywy_schemas import HomePageSchema


@set_apywy_schema(HomePageSchema)
class HomePageView(APIView):
    ...
```

Итог, для метода **get** мы получили расширенную информацию.

- Добавим информацию про **post**

```python
# apywy_schemas.py
...

class HomePageSchema(Schema):
    ...

    class POST(MethodField):

        HTTP_201 = StatusField(expected_response_data=Constant({'ANSWER': 'POST-RESULT'}))

        class META:
            expected_request_data = RequestDataField(Constant({'data': 'some data here'}))
```

По итогу, конечный вариант нашей схемы:

```python
# apywy_schemas.py
from apywy.fields import StatusField, MethodField, RequestDataField
from apywy.schema import Schema

from apywy.constants.const import Constant


class HomePageSchema(Schema):
    class GET(MethodField):

        HTTP_200 = StatusField(expected_response_data=Constant({'ANSWER': 'GET-RESULT'}))

        HTTP_500 = StatusField(expected_response_data=Constant({'ANSWER': 'GET-INVALID-RESULT'}))

    class POST(MethodField):

        HTTP_201 = StatusField(expected_response_data=Constant({'ANSWER': 'POST-RESULT'}))

        class META:
            expected_request_data = RequestDataField(Constant({'data': 'some data here'}))
```

<!-- TODO добавить тут итоговую картинку  -->

---

По умолчанию на главной странице мы видим вьюшки до всех путей, кроме тех, которые относятся к неймспейсам:

```python
('apywy', 'admin')
```

Если вы хотите игнорировать дополнительные неймспейсы, то укажите это в _settings.NAMESPACES_TO_IGNORE_:

```python
NAMESPACES_TO_IGNORE = ()  # значение по умолчанию

NAMESPACES_TO_IGNORE = ('app', )  # игнорировать namespace с именем "app"

NAMESPACES_TO_IGNORE = ('*', )  # игнорировать все неймспейсы
```

### FAQ:

1. Можно ли указать _query_ параметр для запроса в схеме?
2. Можно ли указать сразу несколько ожидаемых результатов от фронта/бекенда в схеме для одного http статуса?

**(1)** и **(2)**, да можно, ниже представлены различные варианты, которые поддерживает _apywy_:

```python
# apywy_schemas.py
from apywy.fields import StatusField, MethodField, RequestDataField
from apywy.schema import Schema

from apywy.constants.const import ListOfConstants, Constant


class HomePageSchema(Schema):
    class GET(MethodField):

        # пример, когда для метода есть единственные данные, независящие от аргумента
        HTTP_200 = StatusField(expected_response_data=Constant({'ANSWER': 'GET-RESULT'}))

        # пример, что и выше, но только с комментарием
        HTTP_300 = StatusField(
            expected_response_data=Constant({'ANSWER': 'GET-RESULT FROM 300'}, comment='some comment')
        )

        # пример, когда для метода есть единственные данные, но мы также хотим задокументировать query паметр
        HTTP_400 = StatusField(
            expected_response_data=Constant({'ANSWER': 'GET-RESULT FROM 400'}, query_arg={'some query': 1})
        )

        # пример, когда для одного статуса может соответствовать множество данных
        HTTP_500 = StatusField(
            expected_response_data=ListOfConstants(
                Constant(
                    expected_data={'ANSWER': 'GET-RESULT FROM 500'},
                    comment='some another comment with list of constants'
                ),
                Constant(
                    expected_data={'ANSWER': 'GET-RESULT FROM 500'},
                    query_arg={
                        'some query 1': '1',
                        'some another query 2': 'blabla',
                    },
                    comment='some comment here'
                ),
            )
        )

        class META:
            # все что относится к работе со статусами распространяется и на request данные
            expected_request_data = RequestDataField(
                ListOfConstants(
                    Constant(expected_data={'some data 1': 'data1'}),
                    Constant(expected_data={'some another data 2': 'data2'}, query_arg={
                        'title': 'some title',
                        'book_id': '10'
                    }),
                )
            )
```

### TODO:

- Рефакторить index.js
