# imports
from opentrons import robot, labware, instruments, modules

# modules
temp_controller = modules.load('tempdeck', '10')
temp_controller.set_temperature(4)

# labware
tiprack_type = 'tiprack-200ul-VWR'
tiprack_p50s = [labware.load(tiprack_type, slot_p50s)
               for slot_p50s in ['1','2','3','6']]
tiprack_p300s = [labware.load(tiprack_type, slot_p300s)
               for slot_p300s in ['9']]
rxn_plate = labware.load('384-corning-3702BC','8')
nitrilase_samples = labware.load(
    'opentrons-aluminum-block-2ml-eppendorf','10', share=True)
reagent_rack = labware.load('opentrons-tuberack-15_50ml','11')
substrate_rack = labware.load('opentrons-tuberack-2ml-eppendorf','7')
ammonium_chloride = labware.load('opentrons-tuberack-15ml','4')
liquid_trash = reagent_rack.wells('C1')
liquid_trash_2 = reagent_rack.wells('C2')

# instruments
p50s = instruments.P50_Single(
    mount="right",
    tip_racks=tiprack_p50s)
if tiprack_type == 'tiprack-200ul-VWR':
    p300s = instruments.P300_Single(
        mount="left",
        tip_racks=tiprack_p300s,
        min_volume=10,
        max_volume=200)
elif tiprack_type == 'opentrons-tiprack-300ul':
    p300s = instruments.P300_Single(
        mount="left",
        tip_racks=tiprack_p300s,
        min_volume=30,
        max_volume=300)

# protocol
def run_custom_protocol(
	phosphate_buffer_volume: float=100,
	water_volume: float=100,
    transfer_volume_nitrilase: float=100,
    transfer_volume_substrate: float=100):

    transfer_dilution_volume = transfer_volume_nitrilase
    final_rxn_volume = transfer_volume_nitrilase + transfer_volume_substrate

    p300s.pick_up_tip()
    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.rows('A',to='D'),
        disposal_vol=20,
        new_tip='never')
    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.wells('E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12',
            'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12'),
        disposal_vol=20,
        new_tip='never')
    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.rows('G',to='J'),
        disposal_vol=20,
        new_tip='never')
    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.wells('K1','K2','K3','K4','K5','K6','K7','K8','K9','K10','K11','K12',
            'L1','L2','L3','L4','L5','L6','L7','L8','L9','L10','L11','L12'),
        disposal_vol=20,
        new_tip='never')
    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.rows('M'),
        disposal_vol=20,
        new_tip='never')

    p300s.distribute(
        phosphate_buffer_volume,
        reagent_rack.wells('A3'),
        rxn_plate.wells('O1','O2','O3','O4','O5','O6','O7','O8','O9',
            'P1','P2','P3','P4','P5','P6','P7','P8','P9'),
        disposal_vol=20,
        new_tip='never')
    p300s.drop_tip()

    p50s.pick_up_tip()
    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A1'),
        rxn_plate.rows('A','C'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')
    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A1'),
        rxn_plate.wells('E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')

    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A1'),
        rxn_plate.wells('O1','O2','O3'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')
    p50s.drop_tip()

    p50s.pick_up_tip()
    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A2'),
        rxn_plate.rows('G','I'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')
    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A2'),
        rxn_plate.wells('K1','K2','K3','K4','K5','K6','K7','K8','K9','K10','K11','K12'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')

    p50s.transfer(
        transfer_volume_nitrilase,
        nitrilase_samples.wells('A2'),
        rxn_plate.wells('P1','P2','P3'),
        mix_after=(2,(transfer_volume_nitrilase+phosphate_buffer_volume)*0.50),
        blow_out=False,
        new_tip='never')
    p50s.drop_tip()

    p50s.pick_up_tip()
    for i in range(3):
    	p50s.transfer(
    		transfer_dilution_volume,
    		rxn_plate[i*2:i*2+370:16],
    		rxn_plate[i*2+1:i*2+371:16],
    		mix_after=(2, (transfer_dilution_volume+phosphate_buffer_volume)*0.50),
    		touch_tip=True,
    		new_tip='always')
    p50s.drop_tip()

    p50s.pick_up_tip()
    p50s.transfer(
        transfer_dilution_volume,
        rxn_plate.wells('O1','O2','O3'),
        rxn_plate.wells('O4','O5','O6'),
        mix_after=(2, (transfer_dilution_volume+phosphate_buffer_volume)*0.50),
        touch_tip=True,
        new_tip='always')

    p50s.pick_up_tip()
    for i in [3,4,5]:
        p50s.transfer(
            transfer_dilution_volume,
            rxn_plate[i*2:i*2+370:16],
            rxn_plate[i*2+1:i*2+371:16],
            mix_after=(2, (transfer_dilution_volume+phosphate_buffer_volume)*0.50),
            touch_tip=True,
            new_tip='always')
    p50s.drop_tip()

    p50s.pick_up_tip()
    p50s.transfer(
        transfer_dilution_volume,
        rxn_plate.wells('P1','P2','P3'),
        rxn_plate.wells('P4','P5','P6'),
        mix_after=(2, (transfer_dilution_volume+phosphate_buffer_volume)*0.50),
        touch_tip=True,
        new_tip='always')

    p300s.pick_up_tip()
    for i in range(3):
        p300s.consolidate(
            transfer_dilution_volume,
            rxn_plate[i*2+1:i*2+371:16],
            liquid_trash,
            blow_out=True,
            new_tip='always')
    p300s.drop_tip()

    p50s.pick_up_tip()
    p50s.consolidate(
        transfer_dilution_volume,
        rxn_plate.wells('O4','O5','O6'),
        liquid_trash,
        blow_out=True,
        new_tip='never')
    p50s.drop_tip()

    p300s.pick_up_tip()
    for i in [3,4,5]:
        p300s.consolidate(
            transfer_dilution_volume,
            rxn_plate[i*2+1:i*2+371:16],
            liquid_trash_2,
            blow_out=True,
            new_tip='always')
    p300s.drop_tip()

    p50s.pick_up_tip()
    p50s.consolidate(
        transfer_dilution_volume,
        rxn_plate.wells('P4','P5','P6'),
        liquid_trash_2,
        blow_out=True,
        new_tip='never')
    p50s.drop_tip()

    for j in range(6):
        if j in [0,1]:
            k=0
        elif j in [2,3]:
            k=8
        elif j in [4,5]:
            k=16
        for i in range(8):
            p50s.pick_up_tip()
            p50s.distribute(
                transfer_volume_substrate,
                substrate_rack.wells(i+k),
                rxn_plate[i*48+j:i*47+i+33+j:16],
                disposal_vol=5,
                touch_tip=True,
                new_tip='never')
            p50s.drop_tip()
            p50s.pick_up_tip()
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*48+j])
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*47+i+16+j])
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*47+i+32+j])
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.drop_tip()
    
    for j in [6,7,8,9,10,11]:
        if j in [6,7]:
            k=0
        elif j in [8,9]:
            k=8
        elif j in [10,11]:
            k=16
        for i in range(8):
            p50s.pick_up_tip()
            p50s.distribute(
                transfer_volume_substrate,
                substrate_rack.wells(i+k),
                rxn_plate[i*48+j:i*47+i+33+j:16],
                disposal_vol=5,
                touch_tip=True,
                new_tip='never')
            p50s.drop_tip()
            p50s.pick_up_tip()
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*48+j])
            p50s.blow_out()
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*47+i+16+j])
            p50s.blow_out()
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.mix(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50,
                rxn_plate[i*47+i+32+j])
            p50s.blow_out()
            p50s.touch_tip(v_offset=-1.5, speed=40.0)
            p50s.drop_tip()
    
    p50s.pick_up_tip()
    p50s.transfer(
        transfer_volume_substrate,
        substrate_rack.wells('A1',to='D6'),
        rxn_plate.wells('M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12',
            'M13','M14','M15','M16','M17','M18','M19','M20','M21','M22','M23','M24'),
        mix_after=(1,(transfer_dilution_volume+phosphate_buffer_volume)*0.50),
        touch_tip=True,
        new_tip='always')

    p50s.pick_up_tip()
    p50s.distribute(
        transfer_volume_substrate,
        reagent_rack.wells('A3'),
        rxn_plate.wells('O9','O8','O7','O6','O5','O4','O3','O2','O1'),
        disposal_vol=5,
        new_tip='never')
    p50s.drop_tip()

    p50s.pick_up_tip()
    p50s.distribute(
        transfer_volume_substrate,
        reagent_rack.wells('A3'),
        rxn_plate.wells('P9','P8','P7','P6','P5','P4','P3','P2','P1'),
        disposal_vol=5,
        new_tip='never')
    p50s.drop_tip()

    # Reagent rack switch
    print("You have 3 mintues to switch out reagents.")
    p50s.delay(minutes=3)

    p50s.pick_up_tip()
    p50s.transfer(
        final_rxn_volume,
        ammonium_chloride.wells(
            'A1','A1','A1',
            'B1','B1','B1',
            'C1','C1','C1',
            'A2','A2','A2',
            'B2','B2','B2',
            'C2','C2','C2',
            'A3','A3','A3',
            'B3','B3','B3',
            'C3','C3','C3',
            'A4','A4','A4',
            'B4','B4','B4',
            'C4','C4','C4',
            'A5','A5','A5',
            'B5','B5','B5'),
        rxn_plate.wells(
            'N11','O11','P11',
            'N12','O12','P12',
            'N13','O13','P13',
            'N14','O14','P14',
            'N15','O15','P15',
            'N16','O16','P16',
            'N17','O17','P17',
            'N18','O18','P18',
            'N19','O19','P19',
            'N20','O20','P20',
            'N21','O21','P21',
            'N22','O22','P22',
            'N23','O23','P23',
            'N24','O24','P24'),
        new_tip='never')
    p50s.drop_tip()

run_custom_protocol(**{
    'phosphate_buffer_volume': 10.0,
    'water_volume': 10.0,
    'transfer_volume_nitrilase': 10.0,
    'transfer_volume_substrate': 1.0})