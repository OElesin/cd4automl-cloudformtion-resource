import json
import logging
from time import sleep
from typing import Any, MutableMapping, Optional
from urllib3 import PoolManager


from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
)


from .models import ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "CD4AutoML::Workflow::Deploy"
CD4AUTO_ML_API = "https://cd4automl.vtion.ai/v1/resource"
HTTP_REQUEST_HEADER = {"Accept": "application/json"}

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint
http = PoolManager()


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    try:
        req_payload = {
            'S3TrainingDataPath': model.S3TrainingDataPath,
            'TargetColumnName': model.TargetColumnName,
            'NotificationEmail': model.NotificationEmail,
            'WorkflowName': model.WorkflowName,
        }
        # auth = HTTPBasicAuth('API_KEY', '')
        LOG.info(f"Creating workflow ${model.WorkflowName}")
        req = http.request(
            'POST', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
        )
        payload = json.loads(req.data)
        deploy_status = payload['DeployStatus']
        while deploy_status == 'IN_PROGRESS':
            progress.status = OperationStatus.IN_PROGRESS
            req_payload['DeployId'] = payload['DeployId']
            req = http.request(
                'POST', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
            )
            payload = json.loads(req.data)
            deploy_status = payload['DeployStatus']
            sleep(30)
        if deploy_status in ('FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT'):
            LOG.error(f"Workflow ${model.WorkflowName} creation failed with status ${deploy_status}")
            raise exceptions.GeneralServiceException(f"creation failed with status ${deploy_status}")
        else:
            # Setting Status to success will signal to cfn that the operation is complete
            model.InferenceApi = payload.get('ApiUri', 'MyTestUrl')
            LOG.info(f"Created workflow ${model.WorkflowName} successfully")
            progress.status = OperationStatus.SUCCESS
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        LOG.error(f"Workflow creation failed with status ${e}")
        raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InvalidRequest, f"was not expecting type {e}")
    return ProgressEvent(status=OperationStatus.SUCCESS, resourceModel=model, message="Workflow created")


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    try:
        req_payload = {
            'S3TrainingDataPath': model.S3TrainingDataPath,
            'TargetColumnName': model.TargetColumnName,
            'NotificationEmail': model.NotificationEmail,
            'WorkflowName': model.WorkflowName,
        }
        # auth = HTTPBasicAuth('API_KEY', '')
        LOG.info(f"Updating workflow ${model.WorkflowName}")
        req = http.request(
            'POST', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
        )
        payload = json.loads(req.data)
        deploy_status = payload['DeployStatus']
        while deploy_status == 'IN_PROGRESS':
            progress.status = OperationStatus.IN_PROGRESS
            req_payload['DeployId'] = payload['DeployId']
            req = http.request(
                'POST', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
            )
            payload = json.loads(req.data)
            deploy_status = payload['DeployStatus']
            sleep(30)
        if deploy_status in ('FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT'):
            LOG.error(f"Workflow ${model.WorkflowName} update failed with status ${deploy_status}")
            raise exceptions.GeneralServiceException(f"update failed with status ${deploy_status}")
        else:
            # Setting Status to success will signal to cfn that the operation is complete
            model.InferenceApi = payload.get('ApiUri')
            LOG.info(f"Updated workflow ${model.WorkflowName} successfully")
            progress.status = OperationStatus.SUCCESS
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        # raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        LOG.error(f"Workflow creation failed with status ${e}")
        return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")
    return ProgressEvent(status=OperationStatus.SUCCESS, resourceModel=model, message="Workflow updated")


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    req_payload = {
        'S3TrainingDataPath': model.S3TrainingDataPath,
        'TargetColumnName': model.TargetColumnName,
        'NotificationEmail': model.NotificationEmail,
        'WorkflowName': model.WorkflowName,
    }
    http.request(
        'DELETE', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
    )
    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )
