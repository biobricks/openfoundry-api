from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text, inspect, DateTime, func, \
    Numeric, Boolean
from sqlalchemy import Enum as EnumType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy_imageattach.entity import Image, image_attachment
from enum import Enum

from sqlalchemy_fsm import FSMField, transition

Base = declarative_base()

# Basics
class EnumString(Enum):
    def __str__(self):
        return str(self.value)

class Id():
    id = Column(Integer, primary_key=True)

class Physical(Id):
    well_id = Column(Integer, ForeignKey('well.id'))
    well = relationship("Well")

class Virtual(Id):
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    genbank_file = Column(String) # TODO this is a file, so let's dump to str for now
    name = Column(String) # Human readable name. Different than human readable id.

### Virutals
part_conditions = Table('part_conditions', Base.metadata,
    Column('left_id', Integer, ForeignKey('conditions.id')),
    Column('right_id', Integer, ForeignKey('parts.id'))
)

organism_conditions = Table('organism_conditions', Base.metadata,
    Column('condition_id', Integer, ForeignKey('conditions.id')),
    Column('organism_id', Integer, ForeignKey('organisms.id'))
)

class ConditionStates(EnumString):
    temp_37 = 'Grow at 37c'
    temp_30 = 'Grow at 30c'
    media_2yt = 'Grow liquid cultures in 2YT'
    agar_lb = 'Grow solid cultures on LB'
    amp = 'Ampicillin or Carbenicillin resistant'
    kan = 'Kanamycin resistant'
    cam = 'Chloramphenicol resistant'
    tet = 'Tetracycline resistant'
    spc = 'Spectinomycin resistant'

class Condition(Base, Id):
    __tablename__ = "conditions"
    condition = Column(EnumType(ConditionStates))
    part = relationship("Part",
            secondary=part_conditions,
            backref="conditions")
    organism = relationship("Organism",
            secondary=organism_conditions,
            backref="conditions")

class PartState(EnumString):
    unordered = 'unordered'
    ordered = 'ordered'
    synthesis_abandoned = 'synthesis_abandoned'
    uncloned = 'uncloned'
    building = 'building'
    sequence_verified = 'sequence_verified'

class PartType(EnumString):
    full_promoter = 'fg-full_promoter'
    promoter = 'fg-promoter'
    utr5 = 'fg-5utr'
    cds = 'fg-cds'
    tag = 'fg-tag'
    terminator = 'fg-3utr'
    operon = 'fg-operon'
    vector = 'vector'

class ProvenanceType(EnumString):
    synthetic = 'synthetic'
    composite = 'composite'
    precloned = 'precloned'

#  Parts <-> Parts
parts_parts = Table('parts_parts', Base.metadata,
    Column('part', ForeignKey('parts.id'), primary_key=True),
    Column('provenance_part', ForeignKey('parts.id'), primary_key=True)
)

class Part(Base, Virtual):
    __tablename__ = "parts"
    hrid = Column(String)
    seq = Column(String)
    part_type = Column(EnumType(PartType))
    part_status = Column(EnumType(PartType)) # TODO transitions here

    # A part can have many parts
    provenance_parts = relationship('Part',
                            secondary=parts_parts,
                            backref='progeny_parts')

    provenance_type = Column(EnumType(ProvenanceType))

    dna_samples = relationship('dna_samples', backref='parts')
    wells = relationship("Well", back_populates="parts")

class Organism(Base, Virtual):
    __tablename__ = "organisms"
    name = Column(String)
    wells = relationship("Well", back_populates="parts")
    
# Physicals
class SequenceState(EnumString):
    not_sequenced = 'not_sequenced'
    sequencing_requested = 'sequencing_requested'
    sequence_confirmed = 'sequence_confirmed'
    sequence_failed = 'sequence_failed'
    mutation = 'mutation'

class DnaType(EnumString):
    plasmid = 'plasmid'
    fragment = 'fragment'


## Wells
class ResidentState(EnumString):
    dna = 'dna'
    organism = 'organism'

class GeneralState(EnumString):
    stocked = "stocked"
    terminated = "terminated"
    shipped = "shipped"

class WellState(EnumString):
    dried = "dried"
    liquid = "liquid"
    solid = "solid"

class WellSolvent(EnumString):
    water = 'water'
    te = 'te'
    two_yt = '2yt'

#  Wells <-> Wells
wells_wells = Table('wells_wells', Base.metadata,
    Column('well', ForeignKey('wells.id'), primary_key=True),
    Column('provenance_well', ForeignKey('wells.id'), primary_key=True)
)

class Well(Base, Id):
    __tablename__ = "wells"
    id = Column(Integer, primary_key=True)
    volume = Column(Numeric)
    address = Column(String)
    plate_id = Column(Integer, ForeignKey('plates.id'))
    solvent = Column(EnumType(WellSolvent), nullable=True)

    logs = relationship("Log", backref="wells")

    general_state = Column(EnumType(GeneralState), nullable=False)
    @transition(source='stocked', target='terminated')
    def terminate(self):
        """This function terminates a well"""
        pass

    well_state = Column(EnumType(WellState), nullable=False)
    @transition(source='dried', target='liquid')
    def resuspend(self):
        """This function resuspends a well"""
        pass
    
    resident_type = Column(EnumType(ResidentState))
    
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=True)
    part = relationship("Part", back_populates="wells")
    
    vector_id = Column(Integer, ForeignKey('parts.id'), nullable=True)
    vector = relationship("Part", back_populates="wells")

    organism_id = Column(Integer, ForeignKey('organisms.id'), nullable=True)
    organism = relationship("Organism", back_populates="wells")
    # TODO all cannot be false

    # DNA data
    ng_quantity = Column(Numeric)
    quality = Column(Numeric)
    def fmol_quantity(self):
        """This function calculates fmol per ul from volume and ng_quantity"""
        pass

    sequence_state = Column(EnumType(SequenceState), nullable=False)
    @transition(source='not_sequenced', target='sequence_confirmed')
    def sequence_dna(self):
        """This function analyzes sequence data. Or something."""
        pass

    # A well can come from many wells
    provenance_wells = relationship('Well',
                            secondary=wells_wells,
                            backref='progeny_wells')

## Plates
class PlateTypes(EnumString):
    deepwell = 'deepwell'
    standard_plate = 'standard_plate'
    pcr_plate = 'pcr_plate'
    agar_plate = 'agar_plate'

class Plate(Base, Id):
    __tablename__ = "plates"
    plate_type = Column(EnumType(PlateTypes))
    plate_location = Column(String) # Human readable sentence of where to find the plate
    wells = relationship("Well", backref="plates")

## Logs

class Log(Base, Id):
    """A log of transitions that occured to wells"""
    __tablename__ = "logs"
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    well_id = Column(Integer, ForeignKey('wells.id'))
    transition_written = Column(String)

