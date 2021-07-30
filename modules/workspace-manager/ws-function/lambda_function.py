import csv
import logging
import os
import boto3

s3_client = boto3.client('s3')
ws_client = boto3.client('workspaces')
ABC_DIR = os.getenv('ABC_DIR_ID')
DEF_DIR = os.getenv('DEF_DIR_ID')
GHI_DIR = os.getenv('GHI_DIR_ID')
JKL_DIR = os.getenv('JKL_DIR_ID')
WIN_PERF = os.getenv('WIN_PERF_BUNDLE_ID',)
WIN_GPU = os.getenv('WIN_GPU_BUNDLE_ID',)
LINUX_PERF = os.getenv('LINUX_PERF_BUNDLE_ID',)
LINUX_POWERPRO = os.getenv('LINUX_POWERPRO_BUNDLE_ID',)
ENCRYPTION_KEY = os.getenv('WORKSPACE_KMS_KEY',)
RUNNING_MODE = 'AUTO_STOP'
logging.basicConfig(format='%(asctime)s [%(levelname)+8s]%(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))




# --- Main handler ---

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get CSV file from S3 and transform it into JSON
    csv_object = s3_client.get_object(Bucket=bucket, Key=key)
    logger.debug('CSV file: {}'.format(csv_object))
    csv_users = csv.reader(csv_object['Body'].read().decode('utf-8').splitlines())
    ad_users_1 = set()
    ad_users_2 = set()
    ad_users_3 = set()
    ad_users_4 = set()
    for item in csv_users:
        if item[1] == 'ABC':
            logger.info('Processing directory: {}'.format(item[1]))
            response = ws_client.describe_workspaces(
                DirectoryId=ABC_DIR,
                UserName=item[0]
            )
            logger.info('Existing workspace?: {}'.format(response))
            workspaces = response['Workspaces']

            if workspaces:
                logger.info('workspace already exists for user: {}'.format(item[0]))
                ad_users_1.add(item[0])
            elif item[2] == 'WIN_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_1.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'WIN_GPU':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_1.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_1.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.debug('Error: {}'.format(e))
            elif item[2] == 'LINUX_POWERPRO':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': ABC_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_1.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))

        elif item[1] == 'DEF':
            logger.info('Processing directory: {}'.format(item[1]))
            response = ws_client.describe_workspaces(
                DirectoryId=DEF_DIR,
                UserName=item[0]
            )
            workspaces = response['Workspaces']
            if workspaces:
                logger.info('workspace already exists for user: {}'.format(item[0]))
                ad_users_2.add(item[0])
            elif item[2] == 'WIN_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_2.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'WIN_GPU':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_2.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.debug('Error: {}'.format(e))
            elif item[2] == 'LINUX_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_2.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_POWERPRO':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': DEF_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_2.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))

# Directory 3
        elif item[1] == 'GHI':
            logger.info('Processing directory: {}'.format(item[1]))
            response = ws_client.describe_workspaces(
                DirectoryId=GHI_DIR,
                UserName=item[0]
            )
            workspaces = response['Workspaces']
            if workspaces:
                logger.info('workspace already exists for user: {}'.format(item[0]))
                ad_users_3.add(item[0])
            elif item[2] == 'WIN_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_3.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'WIN_GPU':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_3.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_3.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_POWERPRO':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': GHI_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_3.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
# Directory 4
        elif item[1] == 'JKL':
            logger.info('Processing directory: {}'.format(item[1]))
            response = ws_client.describe_workspaces(
                DirectoryId=JKL_DIR,
                UserName=item[0]
            )
            workspaces = response['Workspaces']
            if workspaces:
                logger.info('workspace already exists for user: {}'.format(item[0]))
                ad_users_4.add(item[0])
            elif item[2] == 'WIN_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_4.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'WIN_GPU':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': WIN_GPU,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_4.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_PERF':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_PERF,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_4.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error')
                    logger.error('Error: {}'.format(e))
            elif item[2] == 'LINUX_POWERPRO':
                try:
                    logger.info('Creating Workspaces for user: {}'.format(item[0]))
                    logger.info('bundle Id used: {}'.format(item[2]))
                    if item[4] == 'True':
                        ENCRYPTION_ENABLED = True
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'VolumeEncryptionKey': ENCRYPTION_KEY,
                                    'UserVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'RootVolumeEncryptionEnabled': ENCRYPTION_ENABLED,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )    
                    elif item[4] != 'True':
                        create_ws = ws_client.create_workspaces(
                            Workspaces=[
                            {
                                    'DirectoryId': JKL_DIR,
                                    'UserName': item[0],
                                    'BundleId': LINUX_POWERPRO,
                                    'WorkspaceProperties': {
                                        'RunningMode': RUNNING_MODE,
                                        'RunningModeAutoStopTimeoutInMinutes': 60
                                    },
                                    'Tags': [
                                    {
                                        'Key': 'ResourceCostCenter',
                                        'Value': item[3]
                                    }
                                    ]
                                }
                            ]
                        )
                    ad_users_4.add(item[0])
                except Exception as e:
                    logger.error('Unable to Create Workspaces because of an error because of an error')
                    logger.error('Error: {}'.format(e))

    # Get current workspaces
    response = ws_client.describe_workspaces(
        DirectoryId=ABC_DIR
        )
    workspaces_1 = response['Workspaces']
    current_ws_1 = set()
    for workspace in workspaces_1:
        current_ws_1.add(workspace['UserName'])
    logger.info('Existing workspaces list: {}'.format(current_ws_1))
    logger.info('Workspaces in ad_users: {}'.format(ad_users_1))
    # If user is present in WorkSpaces list but not in AD user list, terminate WorkSpace
    ws_to_terminate_1 = current_ws_1 - ad_users_1
    logger.info('Workspaces to terminate: {}'.format(ws_to_terminate_1))
    for user in ws_to_terminate_1:
        try:
            logger.info('Terminating Workspaces for user: {}'.format(user))
            describe_ws = ws_client.describe_workspaces(
                UserName=user,
                DirectoryId=ABC_DIR

            )
            logger.info('describe workspaces: {}'.format(describe_ws))
            workspace_id = describe_ws['Workspaces'][0]['WorkspaceId']
            logger.info('Terminating Workspaces for id: {}'.format(workspace_id))
            terminate_ws = ws_client.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {
                        'WorkspaceId': workspace_id
                    },
                ])
        except Exception as e:
            logger.error('Error executing describe_workspaces or terminate_workspaces{}'.format(e))
            logger.error('Error: {}'.format(e))


    # Get current workspaces for domain 2
    response = ws_client.describe_workspaces(
        DirectoryId=DEF_DIR
        )
    workspaces_2 = response['Workspaces']
    current_ws_2 = set()
    for workspace in workspaces_2:
        current_ws_2.add(workspace['UserName'])

    logger.debug('Workspaces in ad_users: {}'.format(ad_users_2))
    # If user is present in WorkSpaces list but not in AD user list, terminate WorkSpace
    ws_to_terminate_2 = current_ws_2 - ad_users_2
    logger.debug('Workspaces to terminate: {}'.format(ws_to_terminate_2))
    for user in ws_to_terminate_2:
        try:
            logger.info('Terminating Workspaces for user: {}'.format(user))
            describe_ws = ws_client.describe_workspaces(
                UserName=user,
                DirectoryId=DEF_DIR

            )
            logger.info('describe workspaces: {}'.format(describe_ws))
            workspace_id = describe_ws['Workspaces'][0]['WorkspaceId']
            logger.info('Terminating Workspaces for id: {}'.format(workspace_id))
            terminate_ws = ws_client.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {
                        'WorkspaceId': workspace_id
                    },
                ])
        except Exception as e:
            logger.error('Error executing describe_workspaces or terminate_workspaces{}'.format(e))
            logger.error('Error: {}'.format(e))
    # Get current workspaces for domain 3
    response = ws_client.describe_workspaces(
        DirectoryId=GHI_DIR
        )
    workspaces_3 = response['Workspaces']
    current_ws_3 = set()
    for workspace in workspaces_3:
        current_ws_3.add(workspace['UserName'])


    # If user is present in WorkSpaces list but not in AD user list, terminate WorkSpace
    ws_to_terminate_3 = current_ws_3 - ad_users_3
    logger.debug('Workspaces to terminate: {}'.format(ws_to_terminate_3))
    for user in ws_to_terminate_3:
        try:
            logger.info('Terminating Workspaces for user: {}'.format(user))
            describe_ws = ws_client.describe_workspaces(
                UserName=user,
                DirectoryId=GHI_DIR

            )
            logger.info('describe workspaces: {}'.format(describe_ws))
            workspace_id = describe_ws['Workspaces'][0]['WorkspaceId']
            logger.info('Terminating Workspaces for id: {}'.format(workspace_id))
            terminate_ws = ws_client.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {
                        'WorkspaceId': workspace_id
                    },
                ])
        except Exception as e:
            logger.error('Error executing describe_workspaces or terminate_workspaces{}'.format(e))
            logger.error('Error: {}'.format(e))
    # Get current workspaces for domain 4
    response = ws_client.describe_workspaces(
        DirectoryId=JKL_DIR
        )
    workspaces_4 = response['Workspaces']
    current_ws_4 = set()
    for workspace in workspaces_4:
        current_ws_4.add(workspace['UserName'])



    # If user is present in WorkSpaces list but not in AD user list, terminate WorkSpace
    ws_to_terminate_4 = current_ws_4 - ad_users_4
    logger.debug('Workspaces to terminate: {}'.format(ws_to_terminate_4))
    for user in ws_to_terminate_4:
        try:
            logger.info('Terminating Workspaces for user: {}'.format(user))
            describe_ws = ws_client.describe_workspaces(
                UserName=user,
                DirectoryId=JKL_DIR

            )
            logger.info('describe workspaces: {}'.format(describe_ws))
            workspace_id = describe_ws['Workspaces'][0]['WorkspaceId']
            logger.info('Terminating Workspaces for id: {}'.format(workspace_id))
            terminate_ws = ws_client.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {
                        'WorkspaceId': workspace_id
                    },
                ])
        except Exception as e:
            logger.error('Error executing describe_workspaces or terminate_workspaces{}'.format(e))
            logger.error('Error: {}'.format(e))
