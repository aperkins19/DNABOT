"""
@author Opentrons
@date April 27th, 2018
@version 1.3
"""
from opentrons import labware, instruments

metadata = {
    'protocolName': 'Opentrons Logo',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


def run_custom_protocol(pipette_type: 'StringSelection...'='p300-Single',
    dye_labware_type: 'StringSelection...'='trough-12row'):
    if pipette_type == 'p300-Single':
        tiprack = labware.load('tiprack-200ul', '1')
        pipette = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Single':
        tiprack = labware.load('tiprack-200ul', '1')
        pipette = instruments.P50_Single(
            mount='right',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Single':
        tiprack = labware.load('tiprack-10ul', '1')
        pipette = instruments.P10_Single(
            mount='right',
            tip_racks=[tiprack])

    if dye_labware_type == 'trough-12row':
        dye_container = labware.load('trough-12row', '2')
    else:
        dye_container = labware.load('tube-rack-2ml', '2')

    output = labware.load('96-flat', '3')
    # Well Location set-up
    dye1_wells = ['C4','B4','A3','A2', 'B1', 'C1', 'D1','D2','E2', 'E1', 'F1', 'G1', 'H2', 'H3',
                  'G4', 'F4']

    dye2_wells = ['C5', 'C6', 'C7', 'C8', 'C9', 'B10', 'C11', 'D12',
                  'E12', 'F11', 'G10','E9', 'F9', 'F8', 'F7', 'F6', 'F5', 'G8']

    dye2 = dye_container.wells('A1')
    dye1 = dye_container.wells('A2')

    pipette.distribute(
        50,
        dye1,
        output.wells(dye1_wells),
        new_tip='once')
    pipette.distribute(
        50,
        dye2,
        output.wells(dye2_wells),
        new_tip='once')


run_custom_protocol(**{'pipette_type': 'p300-Single', 'dye_labware_type': 'trough-12row'})
