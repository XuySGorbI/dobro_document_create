import pytest
from linc_pars import Lincs_parser


# 1. Тест функции перевода даты
def test_translate_date():
    parser = Lincs_parser(html=0, start="01/01/23", end="01/01/24")
    result = parser.translate_date("12 сентября 2024")
    assert result == "12 9 2024"

# 2. Тест parse_events с фиктивным HTML
def test_parse_events_within_range():
    html = '''
    <div class="OrganizationEventsPage_events__item__NULCJ col-12 col-sm-6 col-md-4 col-lg-3">
        <span class="CardTypes_card-date__title__zS1Lv">12 сентября 2023</span>
        <a href="/event/123">Событие</a>
    </div>
    <div class="OrganizationEventsPage_events__item__NULCJ col-12 col-sm-6 col-md-4 col-lg-3">
        <span class="CardTypes_card-date__title__zS1Lv">15 октября 2025</span>
        <a href="/event/999">Позднее событие</a>
    </div>
    '''
    parser = Lincs_parser(html=0, start="01/01/23", end="01/01/24")
    parser.parse_events(html)

    assert parser.event_links == ["/event/123"]  # Только первое событие попадает в диапазон
