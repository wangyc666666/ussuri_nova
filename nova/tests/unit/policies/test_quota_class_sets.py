#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from nova.api.openstack.compute import quota_classes
from nova.policies import quota_class_sets as policies
from nova.tests.unit.api.openstack import fakes
from nova.tests.unit.policies import base


class QuotaClassSetsPolicyTest(base.BasePolicyTest):
    """Test Quota Class Set APIs policies with all possible context.
    This class defines the set of context with different roles
    which are allowed and not allowed to pass the policy checks.
    With those set of context, it will call the API operation and
    verify the expected behaviour.
    """

    def setUp(self):
        super(QuotaClassSetsPolicyTest, self).setUp()
        self.controller = quota_classes.QuotaClassSetsController()
        self.req = fakes.HTTPRequest.blank('')

        # Check that admin is able to update quota class
        self.admin_authorized_contexts = [
            self.legacy_admin_context, self.system_admin_context,
            self.project_admin_context]
        # Check that non-admin is not able to update quota class
        self.admin_unauthorized_contexts = [
            self.system_member_context, self.system_reader_context,
            self.system_foo_context, self.project_member_context,
            self.project_reader_context, self.project_foo_context,
            self.other_project_member_context
        ]
        # Check that system reader is able to get quota class
        self.system_reader_authorized_contexts = [
            self.legacy_admin_context, self.system_admin_context,
            self.project_admin_context, self.system_member_context,
            self.system_reader_context]
        # Check that non-system reader is not able to get quota class
        self.system_reader_unauthorized_contexts = [
            self.system_foo_context, self.project_member_context,
            self.project_reader_context, self.project_foo_context,
            self.other_project_member_context
        ]

    @mock.patch('nova.objects.Quotas.update_class')
    def test_update_quota_class_sets_policy(self, mock_update):
        rule_name = policies.POLICY_ROOT % 'update'
        body = {'quota_class_set':
                    {'metadata_items': 128,
                        'ram': 51200, 'floating_ips': -1,
                        'fixed_ips': -1, 'instances': 10,
                        'injected_files': 5, 'cores': 20}}
        self.common_policy_check(self.admin_authorized_contexts,
                                 self.admin_unauthorized_contexts,
                                 rule_name,
                                 self.controller.update,
                                 self.req, 'test_class',
                                 body=body)

    @mock.patch('nova.quota.QUOTAS.get_class_quotas')
    def test_show_quota_class_sets_policy(self, mock_get):
        rule_name = policies.POLICY_ROOT % 'show'
        self.common_policy_check(self.system_reader_authorized_contexts,
                                 self.system_reader_unauthorized_contexts,
                                 rule_name,
                                 self.controller.show,
                                 self.req, 'test_class')


class QuotaClassSetsScopeTypePolicyTest(QuotaClassSetsPolicyTest):
    """Test Quota Class Sets APIs policies with system scope enabled.
    This class set the nova.conf [oslo_policy] enforce_scope to True
    so that we can switch on the scope checking on oslo policy side.
    It defines the set of context with scoped token
    which are allowed and not allowed to pass the policy checks.
    With those set of context, it will run the API operation and
    verify the expected behaviour.
    """

    def setUp(self):
        super(QuotaClassSetsScopeTypePolicyTest, self).setUp()
        self.flags(enforce_scope=True, group="oslo_policy")
        # Check that system admin is able to update and get quota class
        self.admin_authorized_contexts = [
            self.system_admin_context]
        # Check that non-system/admin is not able to update and get quota class
        self.admin_unauthorized_contexts = [
            self.legacy_admin_context, self.system_member_context,
            self.system_reader_context, self.project_admin_context,
            self.system_foo_context, self.project_member_context,
            self.project_reader_context, self.project_foo_context,
            self.other_project_member_context
        ]
        # Check that system reader is able to get quota class
        self.system_reader_authorized_contexts = [
            self.system_admin_context, self.system_member_context,
            self.system_reader_context]
        # Check that non-system reader is not able to get quota class
        self.system_reader_unauthorized_contexts = [
            self.legacy_admin_context, self.project_admin_context,
            self.system_foo_context, self.project_member_context,
            self.project_reader_context, self.project_foo_context,
            self.other_project_member_context
        ]


class QuotaClassSetsNoLegacyPolicyTest(QuotaClassSetsScopeTypePolicyTest):
    """Test Quota Class Sets APIs policies with system scope enabled,
    and no more deprecated rules that allow the legacy admin API to
    access system APIs.
    """
    without_deprecated_rules = True

    def setUp(self):
        super(QuotaClassSetsNoLegacyPolicyTest, self).setUp()
