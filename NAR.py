'''
Apache 2.0 License. This source code builds on souce code from the NILMTK project.

Christoph Klemenjak 2019. Please cite our paper (and the NILMTK paper) in case you use this code: http://makonin.com/doc/ISGT-NA_2020b.pdf

https://github.com/klemenjak/comparability

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import numpy as np

from nilmtk.elecmeter import ElecMeterID
from warnings import warn


def noise_aggregate_ratio(elec_meter, power_type='active', meterkeys=None, good_sections_only=True):
    '''
    Computes the noise-to-aggregate ratio (NAR) of an elec metergroup. For more information, see our paper: http://makonin.com/doc/ISGT-NA_2020b.pdf
    :param elec_meter: elec of a dataset (see https://raw.githubusercontent.com/nilmtk/writing/master/figures/NILMTK_UML.png)
    :param meterkeys: either None or array that contains meter IDs
    :param power_type: AC power type, either active or apparent
    :param good_sections_only: option to use good sections only (see http://nilmtk.github.io/nilmtk/master/nilmtk.stats.html)
    :return: NAR ratio (float), power_type (string), good_sections (Boolean)
    '''

    mains = elec_meter.mains()

    if not meterkeys:
        submeters = elec_meter.meters_directly_downstream_of_mains()
    else:
        submeters = elec_meter.from_list(
           [ElecMeterID(elec_meter[m].instance(), elec_meter.building(), elec_meter.dataset()) for m in meterkeys])

    if good_sections_only:
        good_mains_sections = mains.good_sections()
        loader_kwargs = {'sections': good_mains_sections}
    else:
        loader_kwargs = {}

    mains_total_energy = mains.total_energy(**loader_kwargs)
    mains_ac_types = mains_total_energy.keys()

    proportion = np.float64(0.0)

    for meter in submeters.meters:
        try:
            meter_total_energy = meter.total_energy(**loader_kwargs)
        except KeyError:
            warn('KeyError at '+str(meter))
            return [-1, 'power type: '+ power_type, 'good sections only: ' +str(good_sections_only)]
        meter_ac_types = meter_total_energy.keys()
        shared_ac_types = set(mains_ac_types).intersection(meter_ac_types)

        if len(shared_ac_types) > 1:
            proportion += meter_total_energy[power_type] / mains_total_energy[power_type]
            continue

        elif len(shared_ac_types) == 1 and shared_ac_types.__contains__(power_type):
            ac_type = list(shared_ac_types)[0]
            proportion += meter_total_energy[ac_type] / mains_total_energy[ac_type]
            continue

        elif len(shared_ac_types) == 1 and not shared_ac_types.__contains__(power_type):
            warn('No matching power types found!')
            continue

        elif len(shared_ac_types) == 0:
            warn('No matching power types found!')
            continue

    return round(1 - proportion, 2)
