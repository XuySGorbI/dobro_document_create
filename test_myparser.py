import pytest
from bs4 import BeautifulSoup
from myparser import extract_data, pars_dob

# Для мока
import builtins
import myparser as pdm
from unittest.mock import patch

# 1. Тестируем extract_data на простом HTML
def test_extract_data_simple():
    html = """
    <div class="class1">Текст 1</div>
    <div class="class1">Текст 2</div>
    <div class="class2">Другой текст</div>
    """
    result = extract_data(html, ["class1", "class2"])
    assert result == {
        "class1": ["Текст 1", "Текст 2"],
        "class2": ["Другой текст"]
    }

# 2. Тестируем pars_dob с замоканным fetch_html
def test_pars_dob_mocked():
    fake_html = """
    <div class="EventInfo_event-title__k6Fsy d-none d-md-block">Событие A</div>
    <div class="CardTypes_card-location__title__uqLH2">Moscow</div>
    """
    fake_url = "http://example.com/event"

    with patch.object(pdm, 'fetch_html', return_value=fake_html):
        result = pars_dob(fake_url)
        assert result["EventInfo_event-title__k6Fsy d-none d-md-block"].startswith("Событие A")
        assert result["CardTypes_card-location__title__uqLH2"] == "Moscow"
        assert result["url"] == fake_url
