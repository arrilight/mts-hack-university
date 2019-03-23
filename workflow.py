# -*- coding: utf-8 -*-
flow = {
    "build_plan": {
        "init": "choose_minutes",
        "title": "Добро пожаловать в констурктор тарифа! Давайте создадим тариф специально для вас! Скажите мне, "
                 "сколько минут звонков в месяц вы хотите?",
        'suggests': [
            "100 минут",
            "200 минут",
            "1000 минут",
        ],
        "state": {
            "choose_minutes": {
                "events": {
                    "next": {
                        "newstate": "choose_data",
                        "title": "Теперь давайте выберем, сколько гигабайт интернета вам нужно в месяц?",
                        'suggests': [
                            "2 гигабайта",
                            "5 гигабайта",
                            "10 гигабайт",
                        ]
                    }
                }
            },
            "choose_data": {
                "events": {
                    "next": {
                        "newstate": "choose_sms",
                        "title": "Сколько смс вы хотите отправлять в месяц?",
                        'suggests': [
                            "100 смс",
                            "200 смс",
                            "1000 смс",
                        ]
                    }
                }
            },
            "choose_sms": {
                "events": {
                    "next": {
                        "newstate": "choose_tv",
                        "title": "Хотите ли вы добавть услугу тв",
                        'suggests': [
                            "да",
                            "нет"
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
        "title": "Хорошо! Кому пополняем? ",
        'suggests': [
            "Мне",
            "Другой номер",
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
                        "title": "Хорошо! На сколько рублей?",
                        'suggests': [
                            "50 рублей",
                            "100 рублей",
                            "500 рублей",
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
                            "Моя карта МТС",
                            "Мой мобильный баланс",
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
                        "title": "Хорошо! На сколько рублей?",
                        'suggests': [
                            "50 рублей",
                            "100 рублей",
                            "500 рублей",
                        ]
                    }
                }
            },
        }
    },
    "authorization": {
        "init": "number_validation",
        "title": 'Привет! Я твой новый помощник в мире МТС! Чтобы мы могли свободно общаться, '
                 'я должна знать, что ты –– это ты. Для этого введи свой номер телефона.',
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
    }

}
