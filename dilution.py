from opentrons import labware, instruments

metadata = {
    'protocolName': 'Customizable Serial Dilution',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

tube_rack = labware.load('tube-rack_E1415-1500', '2')

liquid_trash = tube_rack.wells('A3')

plate = labware.load('corning_96_wellplate_360ul_flat', '1')

tiprack_10 = [labware.load("tiprack-10ul", '3')]

tiprack_300 = [labware.load("tiprack-200ul", '6')]




def run_custom_protocol(
    total_mixing_volume: float=10.0,
    final_conc: float=1000,):


    pipette_10 = instruments.P10_Single(
        mount='left',
        tip_racks=tiprack_10)

    pipette_300 = instruments.P300_Single(
        mount='right',
        tip_racks=tiprack_300)

    final_conc = final_conc/2
    no_dilutions = 6

    dilution_factor = 1/((final_conc)**(1/no_dilutions))

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # Reverse pipette diluent from wells B12 to H12
    pipette_300.pick_up_tip()
    pipette_300.aspirate(100, tube_rack['A2'])
    pipette_300.dispense(90, plate.cols('12').wells()[0])
    pipette_300.aspirate(diluent_volume+10, tube_rack['A2'])
    pipette_300.dispense(diluent_volume, plate.cols('12').wells()[1])
    for well in plate.cols('12').wells()[2:-1]:
        pipette_300.aspirate(diluent_volume, tube_rack['A2'])
        pipette_300.dispense(diluent_volume, well)
    pipette_300.blow_out(tube_rack['A2'])
    pipette_300.aspirate(total_mixing_volume, tube_rack['A2'])
    pipette_300.dispense(total_mixing_volume, plate.cols('12').wells()[-1])

    pipette_300.drop_tip()

    #Add sample to well A12 for dilution
    pipette_10.pick_up_tip()
    pipette_10.aspirate(10, tube_rack['A1'])
    pipette_10.dispense(10, plate.cols('12').wells('A'))

    if transfer_volume>30:
        pipette_10.drop_tip()
        pipette_300.pick_up_tip()
        for row in range(0,6):
            pipette_300.transfer(
                transfer_volume,
                plate.cols('12').wells(row),
                plate.cols('12').wells(row+1),
                mix_after=(3, total_mixing_volume / 2),
                new_tip='never')

        pipette_300.drop_tip()

    else:
        for row in range(0,6):
            pipette_10.transfer(
                transfer_volume,
                plate.cols('12').wells(row),
                plate.cols('12').wells(row+1),
                mix_after=(3, total_mixing_volume / 2),
                new_tip='never')

        pipette_10.drop_tip()


run_custom_protocol(**{'total_mixing_volume': 100.0, "final_conc": 0.03})
