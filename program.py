from adh_sample_library_preview import ADHClient, AuthorizationTag, Asset, EnumerationState, EventGraphEventType, EventGraphEnumeration, EventGraphReferenceDataType, TypeProperty, PropertyTypeCode, PropertyTypeFlags, EventGraphReferenceDataCategory
from datetime import datetime, timedelta
import json
import random
import traceback

authorization_tag_id = 'SampleAuthorizationTagPython'
enumeration_id = 'SampleEnumerationPython'
reference_data_type_id = 'SampleReferenceDataTypePython'
asset_id = 'SampleReferenceAssetPython'
reference_data_id = 'SampleReferenceDataPython'
event_type_id = 'SampleEventTypePython'
event_id = 'SampleEventPython'

def get_appsettings():
    """Open and parse the appsettings.json file"""

    # Try to open the configuration file
    try:
        with open(
            'appsettings.json',
            'r',
        ) as f:
            appsettings = json.load(f)
    except Exception as error:
        print(f'Error: {str(error)}')
        print(f'Could not open/read appsettings.json')
        exit()

    return appsettings


def suppress_error(func):
    """Suppress an error thrown by func"""
    try:
        func()
    except Exception as error:
        print(f'Encountered Error: {error}')


def main(test=False):
    """This function is the main body of the Event Store sample script"""
    exception = None
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

        appsettings = get_appsettings()

        # Step 1
        # Create an AVEVA Data Hub client
        resource = appsettings.get('Resource')
        api_version = appsettings.get('ApiVersion')
        tenant_id = appsettings.get('TenantId')
        namespace_id = appsettings.get('NamespaceId')
        client_id = appsettings.get('ClientId')
        client_secret = appsettings.get('ClientSecret')

        client = ADHClient(api_version, tenant_id, resource,
                           client_id, client_secret)

        # Step 2
        # Get or create authorization tag
        print('Creating an authorization tag')
        authorization_tag = AuthorizationTag(authorization_tag_id)
        authorization_tag = client.AuthorizationTags.getOrCreateAuthorizationTag(
            namespace_id, authorization_tag.Id, authorization_tag)
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 3
        # Get or create enumeration
        print('Creating an enumeration')
        members = [EnumerationState(name='on', code=1),
                   EnumerationState(name='off', code=2)]
        enumeration = EventGraphEnumeration(
            members, enumeration_id, enumeration_id, id=enumeration_id)
        enumeration = client.Enumerations.getOrCreateEnumeration(
            namespace_id, enumeration.Id, enumeration)
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 4
        # Get or create reference data type
        print('Creating a reference data type')
        reference_data_type_properties = [
            TypeProperty(PropertyTypeCode.ASSET, 'ReferenceAssets', 'ReferenceAssets', 'ReferenceAssets',
                         PropertyTypeFlags.ReverseLookup | PropertyTypeFlags.IsCollection, property_type_id='none', remote_reference_name=reference_data_type_id),
            TypeProperty(PropertyTypeCode.DOUBLE, 'SomeValue')]
        reference_data_type = EventGraphReferenceDataType(
            EventGraphReferenceDataCategory.REFERENCE_DATA, reference_data_type_properties, authorization_tag.Id, reference_data_type_id, id=reference_data_type_id)
        reference_data_type = client.ReferenceDataTypes.getOrCreateReferenceDataType(
            namespace_id, reference_data_type.Id, reference_data_type)
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 5
        # Get or create an Asset to reference
        print('Creating a reference asset')
        asset = Asset(asset_id, asset_id)
        asset = client.Assets.getOrCreateAsset(namespace_id, asset)

        # Step 6
        # Upsert reference data
        print('Upserting reference data')
        reference_data = [
            {
                'referenceAssets': [
                    {'id': asset_id}
                ],
                'someValue': int(100*random.random()),
                'id': reference_data_id,
                'authorizationTags': [authorization_tag.Id]
            }
        ]
        reference_data = client.ReferenceData.getOrCreateReferenceData(
            namespace_id, reference_data_type.Id, json.dumps(reference_data))

        # Step 7
        # Get or Create event type
        print('Creating an event type')
        event_type_properties = [
            TypeProperty(PropertyTypeCode.ASSET, 'ReferenceAssets', 'ReferenceAssets', 'ReferenceAssets',
                         PropertyTypeFlags.IsCollection, property_type_id='none', remote_reference_name=event_type_id),
            TypeProperty(PropertyTypeCode.DOUBLE, 'SomeValue')]
        event_type = EventGraphEventType(
            event_type_properties, authorization_tag.Id, event_type_id, id=event_type_id, version=1)
        event_type = client.EventTypes.getOrCreateEventType(
            namespace_id, event_type_id, event_type)
        client.GraphQL.checkForSchemaChanges(namespace_id)

        # Step 8
        # Upsert events
        print('Upserting events')
        events = [
            {
                'eventStartTime': (datetime.utcnow() - timedelta(minutes=5)).isoformat() + 'Z',
                'eventEndTime': datetime.utcnow().isoformat() + 'Z',
                'referenceAssets': [
                    {'id': asset_id}
                ],
                'someValue': int(100*random.random()),
                'id': event_id,
                'authorizationTags': [authorization_tag.Id]
            }
        ]
        events = client.Events.getOrCreateEvents(
            namespace_id, event_type.Id, json.dumps(events))

        # Step 9
        # Get authorization tags
        print('Getting authorization tags')
        authorization_tags = client.AuthorizationTags.getAuthorizationTags(
            namespace_id)
        for authorization_tag in authorization_tags:
            print(authorization_tag.Id)
        print()

        # Step 10
        # Get Enumerations
        print('Getting enumerations')
        enumerations = client.Enumerations.getEnumerations(namespace_id)
        for enumeration in enumerations:
            print(enumeration.Name)
        print()

        # Step 11
        # Get reference data types
        print('Getting reference data types')
        reference_data_types = client.ReferenceDataTypes.getReferenceDataTypes(
            namespace_id)
        for reference_data_type in reference_data_types:
            print(reference_data_type.Name)
        print()

        # Step 12
        # Get reference data
        reference_data = client.ReferenceData.getReferenceData(
            namespace_id, reference_data_type_id)
        print(reference_data)
        print()

        # Step 13
        # Get event types
        print('Getting event types')
        event_types = client.EventTypes.getEventTypes(namespace_id)
        for event_type in event_types:
            print(event_type.Name)
        print()

        # Step 14
        # Get events
        print('Getting events')
        events = client.Events.getEvents(namespace_id, event_type_id)
        print(events)
        print()

        # Step 15
        # Use a graphQL query to retrieve events, refernce data, and assets
        print('Executing a graph QL query')
        query = '''
        {
            events {
                query''' + event_type_id + '''{
                id
                referenceAssets {
                    id
                }
                someValue
                }
            }
            referenceData {
                query''' + reference_data_id + '''{
                id
                referenceAssets {
                    id
                }
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
        graph_ql_events = client.GraphQL.executeQuery(
            namespace_id, query=query)
        print()
        print(graph_ql_events)

    except Exception as error:
        print((f'Encountered Error: {error}'))
        print()
        traceback.print_exc()
        print()
        exception = error

    finally:
        # Step 16
        # Clean up the remaining artifacts
        print('Deleting events')
        for event in events:
            suppress_error(lambda: client.Events.deleteEvent(
                namespace_id, event_type.Id, event['id']))

        print('Deleting reference data')
        for reference_datum in reference_data:
            suppress_error(lambda: client.ReferenceData.deleteReferenceData(
                namespace_id, reference_data_type_id, reference_datum['id']))

        print('Deleting assets')
        suppress_error(lambda: client.Assets.deleteAsset(
            namespace_id, asset_id))

        print('Deleting authorization tag')
        suppress_error(lambda: client.AuthorizationTags.deleteAuthorizationTag(
            namespace_id, authorization_tag.Id))

        if test and exception is not None:
            raise exception


if __name__ == '__main__':
    main()
