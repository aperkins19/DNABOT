from opentrons import labware, instruments
from math import log

metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

tube_rack = labware.load('tube-rack_E1415-1500', '2')

liquid_trash = tube_rack.wells('A3')

plate = labware.load('4ti-0960_FrameStar', '1')

tiprack_10 = [labware.load("tiprack-10ul", '3')]

tiprack_300 = [labware.load("tiprack-200ul", '6')]


def run_custom_protocol(
    pipette_type: 'StringSelection...'='p10-Single',
    total_mixing_volume: float=10.0,
    tip_use_strategy: 'StringSelection...'='use one tip'):


    pipette_10 = instruments.P10_Single(
        mount='left',
        tip_racks=tiprack_10)

    pipette_300 = instruments.P300_Single(
        mount='right',
        tip_racks=tiprack_300)

    new_tip = 'never' if tip_use_strategy == 'use one tip' else 'always'

    initial_conc = 10
    final_conc = 0.345

    dilution_factor = log((initial_conc/(final_conc/10)),3.981071705534972507702523050877520434876770372973804468652)

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    #add sample to well A12 for dilution
    pipette_10.distribute(total_mixing_volume, tube_rack['A1'], plate.cols('12').wells('A'))

    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column after the number of samples for a blank

    pipette_300.distribute(diluent_volume, tube_rack['A2'], plate.cols('12').wells()[1:], disposal_vol=10)



    for row in range(0,6):
        if new_tip == 'never':
            pipette_10.pick_up_tip()

        pipette_10.transfer(
            transfer_volume,
            plate.cols('12').wells(row),
            plate.cols('12').wells(row+1),
            mix_after=(3, total_mixing_volume / 2),
            new_tip=new_tip)

        if new_tip == 'never':
            pipette_10.drop_tip()


run_custom_protocol(**{'pipette_type': 'p300-Single', 'total_mixing_volume': 10.0, 'tip_use_strategy': 'use one tip'})
