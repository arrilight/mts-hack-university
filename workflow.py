# -*- coding: utf-8 -*-
flow = {
    "build_plan": {
        "init": "choose_minutes",
        "title": "Добро пожаловать в констурктор тарифа. Давай создадим тариф специально для тебя. \nСкажи мне, "
                 "сколько минут звонков в месяц ты хочешь? Введи значение от 100 до 700",
        'suggests': [
            {"title": "100 минут", "hide": True},
            {"title": "300 минут", "hide": True},
            {"title": "500 минут", "hide": True},
        ],
        "state": {
            "choose_minutes": {
                "events": {
                    "next": {
                        "newstate": "choose_data",
                        "title": "Теперь давай выберем, сколько гигабайт интернета тебе нужно в месяц? Введи любое значение от 1 до 100",
                        'suggests': [
                            {"title": "1 гигабайт", "hide": True},
                            {"title": "5 гигабайт", "hide": True},
                            {"title": "10 гигабайт", "hide": True},
                        ]
                    }
                }
            },
            "choose_data": {
                "events": {
                    "next": {
                        "newstate": "choose_sms",
                        "title": "Сколько смс ты хочешь отправлять в месяц? Введи любое значение от 100 до 1000",
                        'suggests': [
                            {"title": "100 смс", "hide": True},
                            {"title": "200 смс", "hide": True},
                            {"title": "500 смс", "hide": True},
                        ]
                    }
                }
            },
            "choose_sms": {
                "events": {
                    "next": {
                        "newstate": "choose_tv",
                        "title": "Хочешь ли добавить услугу МТС ТВ?",
                        'suggests': [
                            {"title": "да"},
                            {"title": "нет"},
                        ]
                    }
                }
            },
            "choose_tv": {
                "events": {
                }
            }
        }
    },
    "top_up": {
        "init": "chose_to_who",
        "title": "Хорошо! Кому пополняем?",
        'suggests': [
            {"title": "Мне"},
            {"title": "Другой номер"},
        ],
        "state": {
            "chose_to_who": {
                "events": {
                    "enter_other_number": {
                        "newstate": "other_number",
                        "title": "Какой номер пополнить?",
                    },
                    "next": {
                        "newstate": "choose_amount",
                        "title": "Хорошо! На сколько рублей? Введи любую сумму от 100 до 15000₽",
                        'suggests': [
                            {"title": "100 рублей", "hide": True},
                            {"title": "200 рублей", "hide": True},
                            {"title": "500 рублей", "hide": True},
                            {"title": "1000 рублей", "hide": True},
                        ]
                    }
                }
            },
            "choose_amount": {
                "events": {
                    "next": {
                        "newstate": "choose_source",
                        "title": "Откуда будем пополнять?",
                        'suggests': [
                            {"title": "Моя карта МТС Банка"},
                            {"title": "С мобильного баланса"},
                        ]
                    }
                }
            },
            "choose_source": {
                "events": {

                }
            },
            "other_number": {
                "events": {
                    "next": {
                        "newstate": "choose_amount",
                        "title": "Хорошо! На сколько рублей? Введи любую сумму от 100 до 15000₽",
                        'suggests': [
                            {"title": "100 рублей", "hide": True},
                            {"title": "200 рублей", "hide": True},
                            {"title": "500 рублей", "hide": True},
                            {"title": "1000 рублей", "hide": True},
                        ]
                    }
                }
            },
        }
    },
    "authorization": {
        "init": "number_validation",
        "title": 'Привет! Я твой новый помощник в мире МТС! Чтобы мы могли свободно общаться, '
                 'я должна знать, что ты – это ты. Для этого введи свой номер телефона.',
        'suggests': [],
        "state": {
            "number_validation": {
                "events": {
                    "next": {
                        "newstate": "sms_input",
                        "title": "Тебе пришло смс с несколькими словами. Прочитай их мне, пожалуйста.",
                        'suggests': []
                    }
                }
            },
            "sms_input": {
                "events": {
                    "fail": {
                        "newstate": "number_validation",
                        "title": "Попробуй ввести номер еще раз.",
                        'suggests': []
                    }
                }
            }
        }
    },
    "handle_music": {
        "init": "search_music",
        "title": 'Какую песню найти?',
        "suggests": [

        ],
        "state": {
            "search_music": {
                "events": {
                    "next": {
                        "newstate": "add_music",
                        "title": "Готово!",
                        'suggests': [
                            {"title": "Проиграть", "url": 'https://music.mts.ru/album/6252045/track/45203073?share=1'},
                            {"title": "Добавить"},
                            {"title": "Спасибо"}
                        ]
                    },
                }
            },
            "add_music": {
                "events": {
                    "next": {
                        "newstate": "finish",
                        "title": "Добавила песню в твою медиатеку.",
                        'suggests': []
                    },
                }
            },
            "finish": {
                "events": None,
            }

        }
    }

}
