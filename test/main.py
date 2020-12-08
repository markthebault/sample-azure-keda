#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show receiving batch messages from a Service Bus Queue.
"""

# pylint: disable=C0111

import os
import time
import logging
from azure.servicebus import ServiceBusClient
from azure.identity import ManagedIdentityCredential, DeviceCodeCredential


SERVICEBUS_NAMESPACE = os.environ["SERVICEBUS_NAMESPACE"]
QUEUE_NAME = os.environ["SERVICE_BUS_QUEUE_NAME"]
local = os.environ["LOCAL"]

def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
  log = get_module_logger("default-logger")

  #Get credentials
  credential=None
  if local == "true":
    log.info("Using device code credential")
    credential = DeviceCodeCredential()
    credential.get_token("https://management.azure.com/.default")
  else:
    log.info("Using default credential")
    credential = ManagedIdentityCredential()
  log.info("Authentication success")

  ### Connect to service bus
  servicebus_client = ServiceBusClient(
        fully_qualified_namespace=SERVICEBUS_NAMESPACE,
        credential=credential
      )

  log.info("Proceed connection to service bus namespace")
  while True:
    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
        with receiver:
            ## Fetch messages
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                ### Print message
                log.info(str(msg))
                receiver.complete_message(msg)
    log.info("Receive is done.")
    log.info("Sleeping for 2 sec")
    time.sleep(2)