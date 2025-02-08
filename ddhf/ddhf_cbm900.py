#!/usr/bin/env python3
#
# SPDX-License-Identifier: BSD-2-Clause
#
# See LICENSE file for full text of license

'''
   Commodore CBM-900 Artifacts from Datamuseum.dk's BitStore
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from autoarchaeologist.base import type_case

from autoarchaeologist.os.unix import unix_fs
from autoarchaeologist.vendor.commodore import cbm900
from autoarchaeologist.generic import textfiles
from autoarchaeologist.generic import samesame

import ddhf

class CBM900(ddhf.DDHFExcavation):

    '''
    Two CBM900 hard-disk images, one also contains the four distribution
    floppy images.
    '''

    BITSTORE = (
        "30001199",
        "30001972",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # The demo programs for Hanovermesse 1985 are in german.
        self.type_case = type_case.WellKnown("iso8859-1")

        self.add_examiner(*cbm900.examiners)
        self.add_examiner(unix_fs.FindUnixFs)
        self.add_examiner(textfiles.TextFile)
        self.add_examiner(samesame.SameSame)

if __name__ == "__main__":
    ddhf.main(
        CBM900,
        html_subdir="cbm900",
        ddhf_topic = "Commodore CBM-900",
        ddhf_topic_link = 'https://datamuseum.dk/wiki/Commodore/CBM900',
    )
