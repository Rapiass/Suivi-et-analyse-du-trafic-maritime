
TABLES = ['Company','UserHasVessel','UserHasRole','User','Country','Role','Vessel','VesselType','Position','NavigationStatus']


MAPPING = {
    'MMSI' : ['Vessel.MMSI'],
    'BaseDateTime' : ['Position.BaseDateTime'],
    'LAT' : ['Position.LAT'],
    'LON' : ['Position.LON'],
    'SOG' : ['Position.SOG'],
    'COG' : ['Position.COG'],
    'Heading' : ['Position.Heading'],
    'VesselName' : ['Vessel.VesselName'],
    'IMO' : ['Vessel.IMO'],
    'CallSign' : ['Vessel.CallSign'],
    'VesselType' : ['Vessel.IDVesselType','VesselType.IDVesselType'],
    'Status' : ['Position.Status','NavigationStatus.Status'],
    'Length' : ['Vessel.Length'],
    'Width' : ['Vessel.Width'],
    'Draft' : ['Vessel.Draft'],
    'Cargo' : ['Vessel.Cargo'],
    'TransceiverClass' : ['Vessel.TransceiverClass']

}