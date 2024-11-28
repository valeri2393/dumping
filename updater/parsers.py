BS_RESOURCES = [
    {
        "resource": 'AURA',
        "path": "//div[contains(@class, 'product-page__price price')]",
        "attr": 'data-price'
    },

    {
        "resource": 'Energy',
        "path": "//div[contains(@class, 'price-site')]"
    },

    {
        "resource": 'Grandeks',
        "path": "//span[contains(@class, 'price_value')]"
    },

    {
        "resource": 'SEDOS',
        "path": "//span[contains(@itemprop, 'price')]"
    },

    {
        "resource": 'Гольфстрим',
        "path": "//span[contains(@class, 'price_value')]"
    },
    {
        "resource": 'СДС',
        "path": "//div[contains(@class, 'price')]"
    },
    {
        "resource": 'Абсолютное тепло',
        "path": "//span[@class='priceVal']"
    },
    {
        "resource": 'Газовик-М',
        "path": "//span[@class='price_value']"
    },
    {
        "resource": 'Обогрев Люкс',
        "path": "//p[@id='price']"
    },
    {
        "resource": 'Теплоком',
        "path": "//span[contains(@class,'autocalc-product-')]",
        "attr": "data-value"
    },
    {
        "resource": 'Техномаркет',
        "path": ".//b[contains(text(),'Цена:')]",
    },
    {
        "resource": 'Техэтаж',
        "path": ".//strong[contains(text(),' р.')]",
    },
    {
        "resource": 'Хотлидер',
        "path": ".//meta[@itemprop='price']",
        "attr": "content"
    },
    {
        "resource": 'Технологии тепла',
        "path": ".//div[@data-price]",
        "attr": "data-price"
    },
]

SELENIUM_RESOURCES = [
    {
        "resource": 'Caleo',
        "path": "//span[contains(@class, 'price_value')]",
        "sleep_time": 2
    },

    {
        "resource": 'Devi',
        "path": "//span[contains(@class, 'value price')]",
        "sleep_time": 2
    },

    {
        "resource": 'Eastec',
        "path": "//div[contains(@id, 'main-product-price')]",
        "sleep_time": 2
    },

    {
        "resource": 'Spyheat',
        "path": "//span[contains(@class, 'price-wrapper')]",
        "sleep_time": 2
    },
    {
        "resource": 'Thermo',
        "path": "//div[contains(@class, 'js_price_wrapper')]",
        "sleep_time": 2
    },
    {
        "resource": 'Русское тепло',
        "path": "//div[contains(@class, 'regprice-block')]",
        "sleep_time": 2
    },
    {
        "resource": 'Теплолюкс',
        "path": "//div[@class='price']",
        "sleep_time": 2
    },
    {
        "resource": 'ЧТК',
        "path": "//div[@class='card_page__price']"
    },
    {
        "resource": 'ВсеИнструменты',
        "path": "//p[contains(@data-behavior, 'price-now')]",
        "sleep_time": 2
    },
    {
        "resource": 'Миллиметр',
        "path": "//div[@class='priceBig']"
    },
    {
        "resource": 'Петрович',
        "path": "//p[@data-test='product-gold-price']",
        "sleep_time": 3
    },
    {
        "resource": 'Теплоплюс39',
        "path": "//div[contains(@class,'price-current')]",
    },
]

BUTTON_RESOURCES = [
    {
        "resource": "Теплый пол №1",
        "buttons_path": "//li[contains(@class,'button-variable-item')]",
        "price_path": "//p[@class='price variation-price']/ins",
        "del_index": [20],
    },
    {
        "resource": "Золотое Сечение",
        "buttons_path": "//ul[@role='radiogroup']/li",
        "price_path": "//p[@class='price variation-price']/ins",
        "del_index": [0],
    },
]
