# imports
from opentrons import labware, instruments

# labware
tiprack_type = 'tiprack-200ul-VWR'
rxn_plate = labware.load('384-corning-3702BC', '8')
tiprack_p300m = [labware.load(tiprack_type, slot_p300m)
               for slot_p300m in ['9']]
tiprack_p50m = [labware.load(tiprack_type, slot_p50m)
               for slot_p50m in ['10','7','4','1']]
reagent_trough = labware.load('trough-12row','11')

# instruments
p50m = instruments.P50_Multi(
    mount="right",
    tip_racks=tiprack_p50m)
if tiprack_type == 'tiprack-200ul-VWR':
    p300m = instruments.P300_Multi(
        mount="left",
        tip_racks=tiprack_p300m,
        min_volume=10,
        max_volume=200)
elif tiprack_type == 'opentrons-tiprack-300ul':
    p300m = instruments.P300_Multi(
        mount="left",
        tip_racks=tiprack_p300m,
        min_volume=30,
        max_volume=300)

def run_custom_protocol(
        transfer_volume_nitrilase: float=10,
        transfer_volume_substrate: float=1,
        transfer_volume_OPA_DMSO: float=36,
        transfer_volume_TCA: float=7.5,
        transfer_volume_DMSO: float=35.5):
    
    final_rxn_volume = transfer_volume_nitrilase + transfer_volume_substrate
    final_assay_volume = final_rxn_volume + transfer_volume_OPA_DMSO
     + transfer_volume_TCA + transfer_volume_DMSO

    alternating_wells = []
    for column in rxn_plate.cols():
        alternating_wells.append(column.wells('A'))
        alternating_wells.append(column.wells('B'))

    p50m.pick_up_tip()
    p50m.transfer(
        transfer_volume_OPA_DMSO,
        reagent_trough.wells('A1'),
        alternating_wells,
        mix_after=(2,final_assay_volume*0.25),
        new_tip='always')

    p50m.reset()

    p50m.pick_up_tip()
    p50m.transfer(
        transfer_volume_TCA,
        reagent_trough.wells('A6'),
        alternating_wells,
        mix_after=(3, final_assay_volume*0.30),
        new_tip='always')

    p50m.reset()

    p50m.pick_up_tip()
    p50m.set_flow_rate(aspirate=60,dispense=80)
    p50m.transfer(
        transfer_volume_DMSO,
        reagent_trough.wells('A12'),
        alternating_wells,
        mix_after=(8, final_assay_volume*0.50),
        new_tip='always')
    p50m.set_flow_rate(aspirate=25,dispense=50)

run_custom_protocol(**{
    'transfer_volume_nitrilase': 10,
    'transfer_volume_substrate': 1.0,
    'transfer_volume_OPA_DMSO': 36.0,
    'transfer_volume_TCA': 7.5,
    'transfer_volume_DMSO': 40.5})