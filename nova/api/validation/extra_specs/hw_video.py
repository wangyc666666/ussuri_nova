# Copyright 2020 Red Hat, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Validators for ``hw_video`` namespaced extra specs."""

from nova.api.validation.extra_specs import base


# TODO(stephenfin): Move these to the 'hw:' namespace
EXTRA_SPEC_VALIDATORS = [
    base.ExtraSpecValidator(
        name='hw_video:ram_max_mb',
        description=(
            'The maximum amount of memory the user can request using the '
            '``hw_video_ram`` image metadata property, which represents the '
            'video memory that the guest OS will see. This has no effect for '
            'vGPUs.'
        ),
        value={
            'type': int,
            'min': 0,
        },
    ),
]


def register():
    return EXTRA_SPEC_VALIDATORS
