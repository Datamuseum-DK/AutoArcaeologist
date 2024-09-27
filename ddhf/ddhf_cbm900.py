#!/usr/bin/env python3
#
# SPDX-License-Identifier: BSD-2-Clause
#
# See LICENSE file for full text of license text

'''
Commodore CBM-900 Artifacts from Datamuseum.dk's BitStore
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from autoarchaeologist import ddhf
from autoarchaeologist.base import type_case

from autoarchaeologist.unix import guess_unix_fs
from autoarchaeologist.vendor.commodore import cbm900
from autoarchaeologist.generic import textfiles
from autoarchaeologist.generic import samesame

class CBM900(ddhf.DDHF_Excavation):

    '''
    Two CBM900 hard-disk images, one also contains the four distribution
    floppy images.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # The demo programs for Hanovermesse 1985 are in german.
        self.type_case = type_case.WellKnown("iso8859-1")

        self.add_examiner(*cbm900.examiners)
        self.add_examiner(guess_unix_fs.GuessUnixFs)
        self.add_examiner(textfiles.TextFile)
        self.add_examiner(samesame.SameSame)

        self.from_bitstore(
            "30001199",
            "30001972",
        )

if __name__ == "__main__":
    ddhf.main(
        CBM900,
        html_subdir="cbm900",
        ddhf_topic = "Commodore CBM-900",
        ddhf_topic_link = 'https://datamuseum.dk/wiki/Commodore/CBM900',
    )
