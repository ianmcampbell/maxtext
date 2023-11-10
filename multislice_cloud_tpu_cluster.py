# Copyright 2022 The JAX Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Optional
from jax._src import xla_bridge
from jax._src import clusters
from jax._src.cloud_tpu_init import running_in_cloud_tpu_vm


def get_metadata(key):
  import requests  # pytype: disable=import-error
  import time  # pytype: disable=import-error
  # Based on https://github.com/tensorflow/tensorflow/pull/40317
  gce_metadata_endpoint = 'http://' + os.environ.get(
      'GCE_METADATA_IP', 'metadata.google.internal')

  retry_count = 0
  retrySeconds = 0.500
  api_resp = None

  while retry_count < 6:
    api_resp = requests.get(
        f'{gce_metadata_endpoint}/computeMetadata/v1/instance/attributes/{key}',
        headers={'Metadata-Flavor': 'Google'})
    if api_resp.status_code == 200:
      break
    retry_count += 1
    time.sleep(retrySeconds)

  if api_resp is None:
    raise RuntimeError(f"Getting metadata['{key}'] failed for 6 tries")
  return api_resp.text


class MultisliceTpuCluster(clusters.ClusterEnv):

  def get_tpu_env_dict():
    tpu_env_data = get_metadata('tpu-env')
    # should trim this to ignore last blank linke
    items = tpu_env_data.split('\n')
    print(vals)
    tpu_env_dict = dict()
    for item in items[0:-1]:
        col_split = item.split(':')
        key,val = col_split[0], col_split[1]
        tpu_env_dict[a]=b
    return tpu_env_dict

  @classmethod
  def is_env_present(cls) -> bool:
    return running_in_cloud_tpu_vm
    # DO NOT SUBMIT: also check in multislice environment

  @classmethod
  def get_coordinator_address(cls) -> str:
    # TODO: First try to get from environment variable before TPU env
    tpu_env_dict = get_tpu_env_dict()
    coordinator_address = tpu_env_dict['MEGASCALE_COORDINATOR_ADDRESS']
    coordinator_address.split(':')[0] + ':8476'
    return cls._get_worker_endpoints()[0].split(':')[2] + ':8476'

  @classmethod
  def get_process_count(cls) -> int:
    tpu_env_dict = get_tpu_env_dict()
    num_slices = tpu_env_dict['MEGASCALE_NUM_SLICES']
    return int(xla_bridge.process_count() * num_slices)

  @classmethod
  def get_process_id(cls) -> int:
    if cls.get_process_count() != len(cls._get_worker_endpoints()):
      raise RuntimeError('Number of workers does not equal the number of '
                         'processes. Auto detecting process_id is not possible.'
                         'Please pass process_id to jax.distributed.initialize() manually.')
    return int(get_metadata('agent-worker-number'))

  @classmethod
  def get_local_process_id(cls) -> Optional[int]:
    return None

  @staticmethod
  def _get_worker_endpoints() -> str:
    return get_metadata('worker-network-endpoints').split(',')