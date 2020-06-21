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
        callbackContext=callback_context if callback_context is not None else {}
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
        # resuming from a long CREATE operation
        if 'DEPLOY_ID' in callback_context:
            req_payload['DeployId'] = callback_context['DEPLOY_ID']
        req = http.request(
            'POST', url=CD4AUTO_ML_API, headers=HTTP_REQUEST_HEADER, body=json.dumps(req_payload)
        )

        payload = json.loads(req.data)
        deploy_status = payload['DeployStatus']
        progress.callbackContext['DEPLOY_ID'] = payload['DeployId']
        progress.callbackDelaySeconds = 20
        progress.status = OperationStatus.IN_PROGRESS
        if deploy_status in ('FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT'):
            LOG.error(f"Workflow ${model.WorkflowName} creation failed with status ${deploy_status}")
            progress.status = OperationStatus.FAILED
        elif deploy_status == 'IN_PROGRESS':
            model.InferenceApi = payload.get('ApiUri', 'MyTestUrl')
            LOG.info(f"Created workflow ${model.WorkflowName} successfully")
            progress.status = OperationStatus.IN_PROGRESS
        else:
            progress.status = OperationStatus.SUCCESS
        return progress

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
    return create_handler(session, request, callback_context)


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
    progress.status = OperationStatus.SUCCESS
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
