import json
import random
import traceback
from datetime import datetime, timedelta

from adh_sample_library_preview import (
    ADHClient,
    AuthorizationTag,
    Enumeration,
    EnumerationState,
    EventType,
    PropertyTypeCode,
    PropertyTypeFlags,
    ReferenceDataCategory,
    ReferenceDataType,
    SdsUom,
    TypeProperty,
    UomValueInput,
)
from adh_sample_library_preview.Asset import Asset

from SampleEnumerationPython import SampleEnumerationPython
from SampleEventTypePython import SampleEventTypePython
from SampleReferenceDataTypePython import SampleReferenceDataTypePython

authorization_tag_id = 'SampleAuthorizationTagPython'
enumeration_id = 'SampleEnumerationPython'
reference_data_type_id = 'SampleReferenceDataTypePython'
asset_id = 'SampleReferenceAssetPython'
reference_data_id_0 = 'SampleReferenceDataPython0'
reference_data_id_1 = 'SampleReferenceDataPython1'
event_type_id = 'SampleEventTypePython'
event_id_0 = 'SampleEventPython0'
event_id_1 = 'SampleEventPython1'


def suppress_error(func):
    """Suppress an error thrown by func"""
    try:
        func()
    except Exception as error:
        print(f'Encountered Error: {error}')


def main(test=False):
    """This function is the main body of the Event Store sample script"""
    exception = None
    created_reference_data = []
    created_events = []
    try:
        print(r"---------------------------------------------------------------")
        print(r"    ,---,.                                  ___                ")
        print(r"  ,'  .' |                                ,--.'|_              ")
        print(r",---.'   |                        ,---,   |  | :,'             ")
        print(r"|   |   .'     .---.          ,-+-. /  |  :  : ' :  .--.--.    ")
        print(r":   :  |-,   /.  ./|  ,---.  ,--.'|'   |.;__,'  /  /  /    '   ")
        print(r":   |  ;/| .-' . ' | /     \|   |  ,'' ||  |   |  |  :  /`./   ")
        print(r"|   :   .'/___/ \: |/    /  |   | /  | |:__,'| :  |  :  ;_     ")
        print(r"|   |  |-,.   \  ' .    ' / |   | |  | |  '  : |__ \  \    `.  ")
        print(r"'   :  ;/| \   \   '   ;   /|   | |  |/   |  | '.'| `----.   \ ")
        print(r"|   |    \  \   \  '   |  / |   | |--'    ;  :    ;/  /`--'  / ")
        print(r"|   :   .'   \   \ |   :    |   |/        |  ,   /'--'.     /  ")
        print(r"|   | ,'      '---' \   \  /'---'          ---`-'   `--'---'   ")
        print(r"`----'               `----'                                    ")
        print(r"---------------------------------------------------------------")
        print()

        client, namespace_id = ADHClient.fromAppsettings()

        # Step 1
        # Get or create authorization tag
        print('Creating an authorization tag')
        authorization_tag = AuthorizationTag(authorization_tag_id)
        authorization_tag = client.AuthorizationTags.getOrCreateAuthorizationTag(
            namespace_id, authorization_tag.Id, authorization_tag
        )
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 2
        # Get or create enumeration
        print('Creating an enumeration')
        members = [
            EnumerationState(name='on', code=1),
            EnumerationState(name='off', code=2),
        ]
        enumeration = Enumeration(
            members, enumeration_id, enumeration_id, id=enumeration_id
        )
        enumeration = client.Enumerations.getOrCreateEnumeration(
            namespace_id, enumeration.Id, enumeration
        )
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 3
        # Get or create reference data type
        print('Creating a reference data type')
        reference_data_type_properties = [
            TypeProperty(
                PropertyTypeCode.Double, 'SomeValue', flags=PropertyTypeFlags.NoUom
            ),
        ]
        reference_data_type = ReferenceDataType(
            ReferenceDataCategory.ReferenceData,
            reference_data_type_properties,
            authorization_tag.Id,
            reference_data_type_id,
            id=reference_data_type_id,
        )
        reference_data_type = client.ReferenceDataTypes.getOrCreateReferenceDataType(
            namespace_id, reference_data_type.Id, reference_data_type
        )
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 4
        # Get or create an Asset to reference
        print('Creating a reference asset')
        asset = Asset(asset_id, asset_id)
        asset = client.Assets.getOrCreateAsset(namespace_id, asset)

        # Step 5
        # Upsert reference data
        print('Upserting reference data')
        reference_data = [
            {
                'someValue': int(100 * random.random()),
                'id': reference_data_id_0,
                'authorizationTags': [authorization_tag.Id],
            }
        ]
        created_reference_data += client.ReferenceData.getOrCreateReferenceData(
            namespace_id, reference_data_type.Id, json.dumps(reference_data)
        )

        # Step 6
        # Upsert reference data using reference data class
        print('Upserting reference data using reference data class')
        reference_data = [
            SampleReferenceDataTypePython(
                Id=reference_data_id_1,
                SomeValue=int(100 * random.random()),
                AuthorizationTags=[authorization_tag.Id],
            )
        ]
        created_reference_data += client.ReferenceData.getOrCreateReferenceData(
            namespace_id, reference_data_type.Id, reference_data
        )

        # Step 7
        # Get or Create event type
        print('Creating an event type')
        event_type_properties = [
            TypeProperty(
                PropertyTypeCode.Enumeration,
                'SomeValueEnum',
                property_type_id=enumeration_id,
            ),
            TypeProperty(PropertyTypeCode.Double, 'SomeValueUom', uom='kilowatt'),
            TypeProperty(
                PropertyTypeCode.Double, 'SomeValueUnspecifiedUom', uom='NONE'
            ),
            TypeProperty(
                PropertyTypeCode.Double, 'SomeValueNoUom', flags=PropertyTypeFlags.NoUom
            ),
        ]
        event_type = EventType(
            event_type_properties,
            authorization_tag.Id,
            event_type_id,
            id=event_type_id,
            version=1,
        )
        event_type = client.EventTypes.getOrCreateEventType(
            namespace_id, event_type_id, event_type
        )
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 8
        # Upsert events
        print('Upserting events')
        events = [
            {
                'startTime': (datetime.utcnow() - timedelta(minutes=5)).isoformat()
                + 'Z',
                'endTime': datetime.utcnow().isoformat() + 'Z',
                'asset': {'id': asset_id},
                'someValueEnum': 'on',
                'someValueUom': {
                    'value': int(100 * random.random()),
                    'uom': {'id': 'kilowatt'},
                },
                'someValueUnspecifiedUom': {
                    'value': int(100 * random.random()),
                    'uom': None,
                },
                'someValueNoUom': int(100 * random.random()),
                'id': event_id_0,
                'authorizationTags': [authorization_tag.Id],
            }
        ]
        created_events += client.Events.getOrCreateEvents(
            namespace_id, event_type.Id, json.dumps(events)
        )

        # Step 9
        # Upsert events using event class
        print('Upserting event using reference event class')
        events = [
            SampleEventTypePython(
                Id=event_id_1,
                StartTime=datetime.utcnow() - timedelta(minutes=5),
                EndTime=datetime.utcnow(),
                Asset=Asset(asset_id),
                AuthorizationTags=[authorization_tag.Id],
                SomeValueEnum=SampleEnumerationPython.off,
                SomeValueUom=UomValueInput(
                    Value=int(100 * random.random()), Uom=SdsUom('kilowatt')
                ),
                SomeValueUnspecifiedUom=UomValueInput(Value=int(100 * random.random())),
                SomeValueNoUom=int(100 * random.random()),
            )
        ]
        created_events += client.Events.getOrCreateEvents(
            namespace_id, event_type.Id, events
        )

        # Step 10
        # Get authorization tags
        print('Getting authorization tags')
        authorization_tags = client.AuthorizationTags.getAuthorizationTags(namespace_id)
        for authorization_tag in authorization_tags:
            print(authorization_tag.Id)
        print()

        # Step 11
        # Get Enumerations
        print('Getting enumerations')
        enumerations = client.Enumerations.getEnumerations(namespace_id)
        for enumeration in enumerations:
            print(enumeration.Name)
        print()

        # Step 12
        # Get reference data types
        print('Getting reference data types')
        reference_data_types = client.ReferenceDataTypes.getReferenceDataTypes(
            namespace_id
        )
        for reference_data_type in reference_data_types:
            print(reference_data_type.Name)
        print()

        # Step 13
        # Get reference data
        print('Getting reference data')
        reference_data = client.ReferenceData.getReferenceData(
            namespace_id, reference_data_type_id
        )
        print(reference_data)
        print()

        # Step 14
        # Get reference data with reference data class
        print('Getting reference data with reference data class')
        reference_data = client.ReferenceData.getReferenceData(
            namespace_id,
            reference_data_type_id,
            reference_data_class=SampleReferenceDataTypePython,
        )
        reference_datum: SampleReferenceDataTypePython
        for reference_datum in reference_data:
            print(reference_datum.Id)
        print()

        # Step 15
        # Get event types
        print('Getting event types')
        event_types = client.EventTypes.getEventTypes(namespace_id)
        for event_type in event_types:
            print(event_type.Name)
        print()

        # Step 16
        # Get events
        print('Getting events')
        events = client.Events.getEvents(namespace_id, event_type_id)
        print(events)
        print()

        # Step 17
        # Get events with event class
        print('Getting events with event class')
        events = client.Events.getEvents(
            namespace_id, event_type_id, event_class=SampleEventTypePython
        )
        event: SampleEventTypePython
        for event in events:
            print(event.Id)
        print()

        # Step 18
        # Use a graphQL query to retrieve events, refernce data, and assets
        print('Executing a graph QL query')
        query = (
            '''
        {
            events {
                query'''
            + event_type_id
            + '''{
                    id
                    asset {
                        id
                    }
                    someValueEnum
                    someValueNoUom
                    someValueUnspecifiedUom {
                        value
                    }
                    someValueUom {
                        value
                    }
                }
            }
            referenceData {
                query'''
            + reference_data_type_id
            + '''{
                    id
                    someValue
                }
            }
            assets {
                queryAsset {
                id
                }
            }
        }
        '''
        )
        graph_ql_events = client.GraphQL.executeQuery(namespace_id, query=query)
        print()
        print(graph_ql_events)

    except Exception as error:
        print((f'Encountered Error: {error}'))
        print()
        traceback.print_exc()
        print()
        exception = error

    finally:
        # Step 19
        # Clean up the remaining artifacts
        print('Deleting events')
        for event in created_events:
            suppress_error(
                lambda: client.Events.deleteEvent(
                    namespace_id, event_type.Id, event['id']
                )
            )

        print('Deleting reference data')
        for reference_datum in created_reference_data:
            suppress_error(
                lambda: client.ReferenceData.deleteReferenceData(
                    namespace_id, reference_data_type_id, reference_datum['id']
                )
            )

        print('Deleting assets')
        suppress_error(lambda: client.Assets.deleteAsset(namespace_id, asset_id))

        if test and exception is not None:
            raise exception


if __name__ == '__main__':
    main()
