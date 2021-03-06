# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
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
"""
Fake drivers used in testing.
"""

from oslo_utils import importutils

from ironic.common import exception
from ironic.common.i18n import _
from ironic.drivers import base
from ironic.drivers.modules.cimc import management as cimc_mgmt
from ironic.drivers.modules.cimc import power as cimc_power
from ironic.drivers.modules.drac import inspect as drac_inspect
from ironic.drivers.modules.drac import management as drac_mgmt
from ironic.drivers.modules.drac import power as drac_power
from ironic.drivers.modules.drac import raid as drac_raid
from ironic.drivers.modules.drac import vendor_passthru as drac_vendor
from ironic.drivers.modules import fake
from ironic.drivers.modules.ilo import inspect as ilo_inspect
from ironic.drivers.modules.ilo import management as ilo_management
from ironic.drivers.modules.ilo import power as ilo_power
from ironic.drivers.modules import ipmitool
from ironic.drivers.modules.irmc import inspect as irmc_inspect
from ironic.drivers.modules.irmc import management as irmc_management
from ironic.drivers.modules.irmc import power as irmc_power
from ironic.drivers.modules import iscsi_deploy
from ironic.drivers.modules.oneview import management as oneview_management
from ironic.drivers.modules.oneview import power as oneview_power
from ironic.drivers.modules import snmp
from ironic.drivers.modules.ucs import management as ucs_mgmt
from ironic.drivers.modules.ucs import power as ucs_power


class FakeIPMIToolDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = ipmitool.IPMIPower()
        self.console = ipmitool.IPMIShellinaboxConsole()
        self.deploy = fake.FakeDeploy()
        self.vendor = ipmitool.VendorPassthru()
        self.management = ipmitool.IPMIManagement()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'console': 'ipmitool-shellinabox',
            'deploy': 'fake',
            'management': 'ipmitool',
            'power': 'ipmitool',
            'vendor': 'ipmitool'
        }


class FakeIPMIToolSocatDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = ipmitool.IPMIPower()
        self.console = ipmitool.IPMISocatConsole()
        self.deploy = fake.FakeDeploy()
        self.vendor = ipmitool.VendorPassthru()
        self.management = ipmitool.IPMIManagement()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'console': 'ipmitool-socat',
            'deploy': 'fake',
            'management': 'ipmitool',
            'power': 'ipmitool',
            'vendor': 'ipmitool'
        }


class FakeIloDriver(base.BaseDriver):
    """Fake iLO driver, used in testing."""

    def __init__(self):
        if not importutils.try_import('proliantutils'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import proliantutils library"))
        self.power = ilo_power.IloPower()
        self.deploy = fake.FakeDeploy()
        self.management = ilo_management.IloManagement()
        self.inspect = ilo_inspect.IloInspect()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'inspect': 'ilo',
            'management': 'ilo',
            'power': 'ilo'
        }


class FakeDracDriver(base.BaseDriver):
    """Fake Drac driver."""

    def __init__(self):
        if not importutils.try_import('dracclient'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_('Unable to import python-dracclient library'))

        self.power = drac_power.DracPower()
        self.deploy = iscsi_deploy.ISCSIDeploy()
        self.management = drac_mgmt.DracManagement()
        self.raid = drac_raid.DracRAID()
        self.vendor = drac_vendor.DracVendorPassthru()
        self.inspect = drac_inspect.DracInspect()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            # NOTE(dtantsur): the classic driver uses boot=None and
            # deploy=iscsi. This cannot work, so correcting it based on the
            # intended purpose of these fake drivers.
            'deploy': 'fake',
            'inspect': 'idrac',
            'management': 'idrac',
            'power': 'idrac',
            'raid': 'idrac',
            'vendor': 'idrac'
        }


class FakeSNMPDriver(base.BaseDriver):
    """Fake SNMP driver."""

    def __init__(self):
        if not importutils.try_import('pysnmp'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import pysnmp library"))
        self.power = snmp.SNMPPower()
        self.deploy = fake.FakeDeploy()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'management': 'fake',
            'power': 'snmp',
        }


class FakeIRMCDriver(base.BaseDriver):
    """Fake iRMC driver."""

    def __init__(self):
        if not importutils.try_import('scciclient'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import python-scciclient library"))
        self.power = irmc_power.IRMCPower()
        self.deploy = fake.FakeDeploy()
        self.management = irmc_management.IRMCManagement()
        self.inspect = irmc_inspect.IRMCInspect()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'inspect': 'irmc',
            'management': 'irmc',
            'power': 'irmc'
        }


class FakeUcsDriver(base.BaseDriver):
    """Fake UCS driver."""

    def __init__(self):
        if not importutils.try_import('UcsSdk'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import UcsSdk library"))
        self.power = ucs_power.Power()
        self.deploy = fake.FakeDeploy()
        self.management = ucs_mgmt.UcsManagement()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'management': 'ucsm',
            'power': 'ucsm'
        }


class FakeCIMCDriver(base.BaseDriver):
    """Fake CIMC driver."""

    def __init__(self):
        if not importutils.try_import('ImcSdk'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import ImcSdk library"))
        self.power = cimc_power.Power()
        self.deploy = fake.FakeDeploy()
        self.management = cimc_mgmt.CIMCManagement()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'management': 'cimc',
            'power': 'cimc'
        }


class FakeOneViewDriver(base.BaseDriver):
    """Fake OneView driver. For testing purposes."""

    def __init__(self):
        if not importutils.try_import('hpOneView.oneview_client'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import hpOneView library"))

        self.power = oneview_power.OneViewPower()
        self.management = oneview_management.OneViewManagement()
        self.boot = fake.FakeBoot()
        self.deploy = fake.FakeDeploy()
        self.inspect = fake.FakeInspect()

    @classmethod
    def to_hardware_type(cls):
        return 'fake-hardware', {
            'boot': 'fake',
            'deploy': 'fake',
            'inspect': 'fake',
            'management': 'oneview',
            'power': 'oneview'
        }
