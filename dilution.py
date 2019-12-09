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
    total_mixing_volume: float=10.0,
    final_conc: float=1000,):


    pipette_10 = instruments.P10_Single(
        mount='left',
        tip_racks=tiprack_10)

    initial_conc = 10**6
    no_dilutions = 6

    dilution_factor = 1/((final_conc/initial_conc)**(1/no_dilutions))

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # Reverse pipette diluent from wells B12 to H12
    pipette_10.pick_up_tip()
    pipette_10.aspirate(diluent_volume+1, tube_rack['A2'])
    pipette_10.dispense(diluent_volume, plate.cols('12').wells()[1])
    for well in plate.cols('12').wells()[2:-1]:
        pipette_10.aspirate(diluent_volume, tube_rack['A2'])
        pipette_10.dispense(diluent_volume, well)
    pipette_10.blow_out(tube_rack['A2'])
    pipette_10.aspirate(total_mixing_volume, tube_rack['A2'])
    pipette_10.dispense(total_mixing_volume, plate.cols('12').wells()[-1])

    pipette_10.drop_tip()

    #Add sample to well A12 for dilution
    pipette_10.pick_up_tip()
    pipette_10.aspirate(10, tube_rack['A1'])
    pipette_10.dispense(10, plate.cols('12').wells('A'))

    for row in range(0,6):

        pipette_10.transfer(
            transfer_volume,
            plate.cols('12').wells(row),
            plate.cols('12').wells(row+1),
            mix_after=(3, total_mixing_volume / 2),
            new_tip='never')

    pipette_10.drop_tip()


run_custom_protocol(**{'total_mixing_volume': 10.0, "final_conc": 1000})
