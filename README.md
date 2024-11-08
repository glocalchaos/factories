# API
1) `factories/get_all` - возвращаются данные `накопительно ко дню`, и за `переработку`
`factories/get_all?period=daily` - возвращаются данные `за день`
`factories/get_all?period=range`
`factories/get_all?from=24.02.2024&to=24.02.2024` 
Если даты не переданы то накопительно ко дню сегодняшнему
Если некорретный заспрос, то данные отдаеются `factories/get_all`.
`factories/get_all?factory_type=переработка` - параметр отвечает за тип завода

```json
[
    {
        "region": "Москва",
        "code": "77",
        "factories": [
            {
                "name": "Московская ГПЗ",
                "value": 55,
                // "percent": 70,
                "oil_type": [
                    {
                        "name": "Светлые н/п",
                        "value": 80
                    },
                    {
                        "name": "Тёмные н/п",
                        "value": 90
                    },
                    {
                        "name": "СУГ",
                        "value": 70
                    },
                    {
                        "name": "Сера жидкая",
                        "value": 60
                    },
                    {
                        "name": "Сера твёрдая",
                        "value": 50
                    }
                ],
                "transport_type": [
                    {
                        "name": "Ж/Д",
                        "value": 80
                    },
                    {
                        "name": "Авто",
                        "value": 90
                    },
                    {
                        "name": "Труба",
                        "value": 70
                    }
                ]
            }
        ]
        
    },
    {
        "region": "Санкт-Петербург",
        "code": "78",
        "factories": [
            {
                "name": "Санкт-Петербургская ГПЗ",
                "value": 80,
                "oil_type": [
                    {
                        "name": "Светлые н/п",
                        "value": 80
                    },
                    {
                        "name": "Тёмные н/п",
                        "value": 90
                    },
                    {
                        "name": "СУГ",
                        "value": 70
                    },
                    {
                        "name": "Сера жидкая",
                        "value": 60
                    },
                    {
                        "name": "Сера твёрдая",
                        "value": 50
                    }
                ],
                "transport_type": [
                    {
                        "name": "Ж/Д",
                        "value": 80
                    },
                    {
                        "name": "Авто",
                        "value": 90
                    },
                    {
                        "name": "Труба",
                        "value": 70
                    }
                ]
            }
        ]
        
    }
]
```


3)  `factories/:factory_name` - factory_name: Астраханская ГПЗ

Если даты не переданы то накопительно ко дню сегодняшнему
`factories/:factory_name?from=24.02.2024&to=24.02.2024` 

```json
{
    "factory_name": "Астраханская ГПЗ",
    "daily": {
        "plan": 21312,
        "fact": 324324
    },
    "sum": {
        "plan": 124124,
        "fact": 1232
    }
}
```

3) `factories/:factory_name/transport` - за все виды транспорта, накопительно к сегодняшнему дню
Если даты не переданы то накопительно ко дню сегодняшнему
`factories/:factory_name/transport?period=daily` - за день
`factories/:factory_name/transport?period=range` - накопительно ко дню

`factories/:factory_name/transport?transport_type=Автомобильный` - тип транспорта 
`factories/:factory_name/transport?product_category=Светлые` - категория продукта 

`factories/:factory_name/transport?from=24.02.2024&to=24.02.2024` 

`factories/:factory_name/transport?to=24.02.2024` - с начала месяца до `to`

```json
{
    "factory_name":  "Астраханская ГПЗ",
    "transports": [
        {
            "transport_type": "Автомобильный",
            "plan": 2433,
            "fact": 23423 
        }
    ]
}
```
4) `factories/:factory_name/product_category`
Если даты не переданы то накопительно ко дню сегодняшнему

`factories/:factory_name/transport?period=daily` - за день (`to` либо сегодня)
`factories/:factory_name/transport?period=range` - накопительно ко дню (дефолт - с начала месяца до сегодня)

`factories/:factory_name/transport?transport_type=Автомобильный` - тип транспорта 
`factories/:factory_name/transport?product_category=Светлые` - категория продукта 

`factories/:factory_name/transport?from=24.02.2024&to=24.02.2024` 

`factories/:factory_name/transport?to=24.02.2024` - с начала месяца до `to`


```json

{
    "factory_name":  "Астраханская ГПЗ",
    "categories": [
        {
            "product_category": "Светлые",
            "plan": 2433,
            "fact": 23423 
        }
    ]
}
```

## Статусы 

`404` - данные не найдены (тип транспорта не используется на заводе, категории сырья нет на заводе) 
если нет данных за эти даты 
если нет такого завода

`400` - неверный запрос

## Parameters

- from
- to
- period
- factory_type
- product_category
