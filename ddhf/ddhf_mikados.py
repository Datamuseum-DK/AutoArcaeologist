#!/usr/bin/env python3
#
# SPDX-License-Identifier: BSD-2-Clause
#
# See LICENSE file for full text of license

'''
   DDE MIKADOS artifacts from DDHF's bitstore
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from autoarchaeologist.base import type_case
from autoarchaeologist.generic import samesame
from autoarchaeologist.generic import textfiles
from autoarchaeologist.vendor.dansk_data_elektronik import mikados

import ddhf

class Mikados(ddhf.DDHFExcavation):
    ''' All MIKADOS artifacts '''

    BITSTORE = (
        "OS/MIKADOS",
        "DDE/SPC-1",
        #"-30003595", 	# Only one side preserved?
        #"-30003618", 	# Only one side preserved?
        #"-30003620", 	# Only one side preserved?
        #"-30005676", 	# Only one side preserved?
        #"-30004642", 	# missing sectors in IMD
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_case = type_case.DS2089()

        self.add_examiner(*mikados.examiners)
        self.add_examiner(samesame.SameSame)
        self.add_examiner(textfiles.TextFile)


if __name__ == "__main__":
    ddhf.main(
        Mikados,
        html_subdir="mikados",
        ddhf_topic = "MIKADOS",
        ddhf_topic_link = 'https://datamuseum.dk/wiki/MIKADOS',
    )
