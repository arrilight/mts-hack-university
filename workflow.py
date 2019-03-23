flow = {
    "build_plan": {
        "init": "chose_minutes",
        "title": "Добро пожаловать в констурктор тарифа! Давайте создадим тариф специиально для вас! Скажите мне, "
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
            "chose_data": {
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
            "chose_sms": {
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
            "chose_tv": {
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
                            "Другая карта",
                        ]
                    }
                }
            },
            "choose_source": {
                "events": {
                }
            }

        }
    },
    "authorization": {
        "init": "sms_input",
        "title": 'Привет! Я твой новый помощник в мире МТС! Чтобы мы могли свободно общаться, '
                 'я должен знать что ты это ты. Для этого введи свой номер телефона)',
        'suggests': [],
        "state": {
            "sms_input": {
                "events": {
                    "next": {
                        "newstate": "sms_check_success",
                        "title": "Тебе пришло смс с несколькими словами. Прочитай их и я буду уверен, что это ты)",
                        'suggests': []
                    }
                }
            },
            "sms_check_success": {
                "events": {
                    "fail": {
                        "newstate": "sms_check_fail",
                        "title": "Неправильный ввод(",
                        'suggests': [
                            "Попробовать снова",
                            "Новый смс"
                        ]
                    },
                    "next": {
                        "newstate": "end",
                        "title": "Отлично, теперь я могу тебе доверять! Что бы ты хотел?",
                        'suggests': [
                            "Собрать тариф",
                            "Пополнить счет",
                            "Все что вы хотите!",
                        ]
                    }
                }
            },
            "sms_check_fail": {
                "events": {
                    "success": {
                        "newstate": "end",
                        "title": "Отлично, теперь я могу тебе доверять! Что бы ты хотел?",
                        'suggests': [
                            "Собрать тариф",
                            "Пополнить счет",
                            "Все что вы хотите!",
                        ]
                    },
                    "next": {
                        "newstate": "sms_check_fail",
                        "title": "Неправильный ввод(",
                        'suggests': [
                            "Попробовать снова",
                            "Новый смс"
                        ]
                    },
                }
            },
            "end": {
                "events": {
                }
            }

        }
    }

}
