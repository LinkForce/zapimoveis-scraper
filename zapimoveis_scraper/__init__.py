#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2016, Geovany Rodrigues
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from zapimoveis_scraper.enums import ZapAcao, ZapTipo
from zapimoveis_scraper.item import ZapItem

__all__ = [
    # Main search function.
    'search',
]


# URL templates to make urls searches.
url_home = "https://www.zapimoveis.com.br/%(acao)s/%(tipo)s/%(localization)s/#{\"pagina\":\"%(page)s\",\"formato\":\"Lista\"}"

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    return response


def __get_text(element, content=False):
    if element is not None:
        if content is False:
            return element.getText()
        else:
            return element.get("content")

    return ''


def search(localization='go+goiania++setor-marista', num_pages=1, acao=ZapAcao.aluguel.value, tipo=ZapTipo.casas.value):
    page = 1
    items = []

    while page <= num_pages:
        html = get_page(url_home % vars())
        soup = BeautifulSoup(html, 'html.parser')

        houses_cards = soup.find_all(attrs={"class": "minificha"})
        for house_card in houses_cards:
            specifications = house_card.find(attrs={"class": "caracteristicas"})

            item = ZapItem()
            item.price = __get_text(specifications.find(attrs={"class": "preco"}))
            item.bedrooms = __get_text(specifications.find(attrs={"class": "icone-quartos"}))
            item.suites = __get_text(specifications.find(attrs={"class": "icone-suites"}))
            item.vacancies = __get_text(specifications.find(attrs={"class": "icone-vagas"}))
            item.total_area_m2 = __get_text(specifications.find(attrs={"class": "icone-area"}))

            address = house_card.find(attrs={"class": "endereco"})
            item.district = __get_text(address.find("strong"))
            item.country = __get_text(address.find(attrs={"itemprop": "addressCountry"}), True)
            item.postal_code = __get_text(address.find(attrs={"itemprop": "postalCode"}), True)
            item.street = __get_text(address.find(attrs={"itemprop": "streetAddress"}))
            item.city = __get_text(address.find(attrs={"itemprop": "addressLocality"}))
            item.state = __get_text(address.find(attrs={"itemprop": "addressRegion"}))

            item.description = __get_text(house_card.find(attrs={"itemprop": "description"}))
            item.url = address.find("a").get("href")

            items.append(item)
        page += 1

    return items
