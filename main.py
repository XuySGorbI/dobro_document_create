import asyncio
from linc_pars import Lincs_parser
from datetime import datetime


start = datetime(2023, 11, 17)
end = datetime(2024, 9, 12)

class_pars_l = Lincs_parser(10045181, start, end)


asyncio.run(class_pars_l.pars_linc())

print(class_pars_l.lincs)