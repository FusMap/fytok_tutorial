import collections
import collections.abc
import pathlib
import numpy as np
import scipy.constants

from fytok.modules.core_profiles import CoreProfiles
from fytok.modules.core_transport import CoreTransport
from fytok.modules.equilibrium import Equilibrium
from fytok.utils.logger import logger
from spdm.core.function import function_like
from spdm.numlib.misc import array_like


@CoreTransport.Model.register(["spitzer"])
class SpitzerDemo(CoreTransport.Model):
    def execute(self, current: CoreTransport.Model.TimeSlice, *previous, working_dir: pathlib.Path = None):
        
        super().execute(current, *previous, working_dir=working_dir)

        equilibrium: Equilibrium.TimeSlice = self.inputs.get_source("equilibrium").time_slice.current

        core_profiles_1d: CoreProfiles.TimeSlice.Profiles1D = self.inputs.get_source(
            "core_profiles"
        ).time_slice.current.profiles_1d

        eV = scipy.constants.electron_volt

        radial_grid = core_profiles_1d.grid

        B0 = equilibrium.vacuum_toroidal_field.b0
        R0 = equilibrium.vacuum_toroidal_field.r0

        rho_tor_norm = radial_grid.rho_tor_norm
        rho_tor = radial_grid.rho_tor
        psi_norm = radial_grid.psi_norm
        psi_axis = equilibrium.global_quantities.psi_axis
        psi_boundary = equilibrium.global_quantities.psi_boundary
        psi = psi_norm * (psi_boundary - psi_axis) + psi_axis

        q = equilibrium.profiles_1d.q(psi)

        # Tavg = np.sum([ion.density*ion.temperature for ion in core_profile.ion]) / \
        #     np.sum([ion.density for ion in core_profile.ion])

        Te = core_profiles_1d.electrons.temperature(rho_tor_norm)
        Ne = core_profiles_1d.electrons.density(rho_tor_norm)
        # Pe = core_profile.electrons.pressure(rho_tor_norm)

        # Coulomb logarithm
        #  Ch.14.5 p727 Tokamaks 2003
        # lnCoul = (14.9 - 0.5*np.log(Ne/1e20) + np.log(Te/1000)) * (Te < 10) +\
        #     (15.2 - 0.5*np.log(Ne/1e20) + np.log(Te/1000))*(Te >= 10)
        # (17.3 - 0.5*np.log(Ne/1e20) + 1.5*np.log(Te/1000))*(Te >= 10)

        # lnCoul = 14
        lnCoul = core_profiles_1d.coulomb_logarithm(rho_tor_norm)

        # electron collision time , eq 14.6.1
        tau_e = 1.09e16 * ((Te / 1000) ** (3 / 2)) / Ne / lnCoul

        vTe = np.sqrt(Te * eV / scipy.constants.electron_mass)

        # Larmor radius,   eq 14.7.2
        # rho_e = 1.07e-4*((Te/1000)**(1/2))/B0

        # rho_tor[0] = max(rho_e[0], rho_tor[0])

        epsilon = rho_tor / R0
        epsilon12 = np.sqrt(epsilon)
        epsilon32 = epsilon ** (3 / 2)
        ###########################################################################################
        #  Sec 14.10 Resistivity
        #
        eta_s = 1.65e-9 * lnCoul * (Te / 1000) ** (-3 / 2)
        Zeff = core_profiles_1d.zeff(rho_tor_norm)
        fT = 1.0 - (1 - epsilon) ** 2 / np.sqrt(1.0 - epsilon**2) / (1 + 1.46 * np.sqrt(epsilon))

        phi = np.zeros_like(rho_tor_norm)
        nu_e = R0 * q[1:] / vTe[1:] / tau_e[1:] / epsilon32[1:]
        phi[1:] = fT[1:] / (1.0 + (0.58 + 0.20 * Zeff[1:]) * nu_e)
        phi[0] = 0

        C = 0.56 / Zeff * (3.0 - Zeff) / (3.0 + Zeff)

        eta = eta_s * Zeff / (1 - phi) / (1.0 - C * phi) * (1.0 + 0.27 * (Zeff - 1.0)) / (1.0 + 0.47 * (Zeff - 1.0))

        current.profiles_1d["conductivity_parallel"] = function_like(array_like(rho_tor_norm, 1.0 / eta), rho_tor_norm)
