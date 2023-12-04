import os
import pathlib
import shutil
import subprocess
import tempfile

import numpy as np
from fytok.modules.Equilibrium import Equilibrium
from fytok.modules.Magnetics import Magnetics
from fytok.modules.PFActive import PFActive
from fytok.modules.TF import TF
from fytok.modules.Wall import Wall
from fytok.plugins.equilibrium.fy_eq import FyEqAnalyze
from fytok.utils.logger import logger
from spdm.data.File import File
from fytok.modules.Utilities import *
from spdm.utils.constants import *


@Equilibrium.register(["efit_east"])
@sp_tree
class EquilibriumEFITEAST(FyEqAnalyze):
    """
    EFIT is part of GACODE and use of this module requires a license from GA.
    See https://gacode.io/license.html.
    """

    code = {"name": "efit_east", "copyright": "Third-party Plugin for FyTok"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self._shot = self.code.parameters.get("shot", None) or kwargs.get("shot", 0)

    def execute(self, current: Equilibrium.TimeSlice, *previous, **kwargs):
        super().execute(current, *previous, **kwargs)

        tf: TF = self.inputs.get_source("tf")
        wall: Wall = self.inputs.get_source("wall")
        magnetics: Magnetics = self.inputs.get_source("magnetics")
        pf_active: PFActive = self.inputs.get_source(
            "pf_active",
        )
        shot = self._root.shot
        ####################
        # 在这里添加，调用外部程序代码
        # 工作目录为 working_dir
        #################

        """run efit on shot batch way."""
        logger.debug("The execute is start")
        # current_slice = self.time_slice.current

        itime = int(np.round(self.time * 1000))

        mdsdata = {}

        mdsdata["coils"] = [flux_loop.flux(self.time) / (2.0 * np.pi) for flux_loop in magnetics.flux_loop]

        mdsdata["expmp2"] = [bpol.field(self.time) for bpol in magnetics.b_field_pol_probe]

        # for IP

        mdsdata["plasma"] = magnetics.ip[0](self.time)

        # pf_active: PFActive
        # logger.debug(pf_active.coil[0].element[0].turns_with_sign * pf_active.coil[0].current(time))

        mdsdata["brsp"] = [coil.element[0].turns_with_sign * coil.current(self.time) for coil in pf_active.coil]

        # tf: TF   1 tesla@r=1.7m with 4086A in IT coils

        try:
            # logger.debug(tf.coil[0].current(time))

            mdsdata["btor"] = np.mean([tf.coil[0].current(self.time)]) * 1.7 / (4086 * 1.85)
            # mdsdata["btor"] = (np.mean([coil.current(self.time) for coil in tf.coil]) * 1.7 / (4086 * 1.85))

        except Exception:
            logger.error("Can not find TF coil")
            mdsdata["btor"] = 8000 * 1.7 / (4086 * 1.85)

        shot = 70754
        mdsdata["ishot"] = shot

        mdsdata["itime"] = itime

        ##################################################################################################################

        snap_filepath = pathlib.Path(__file__).parent / "snap_files"

        # for EAST ,on SHENMA cluster

        EFIT_ROOT = pathlib.Path(os.environ.get("EFIT_ROOT", "/project/imd/codes/EFIT_Qian"))

        EFIT_LIBRARY_PATH = os.environ.get(
            "EFIT_LIBRARY_PATH",
            "/project/imd/codes/utilities/pgplot/:/home/users/ligq/lib64:/pkg/pgi/linux86/14.10/lib",
        )
        logger.debug(shot)
        if shot <= 44326 and shot > 4774:
            snap_file = snap_filepath / "snap.nam_12"
            efit_exec = EFIT_ROOT / "bin/efitd129d_east_2010"
        elif shot > 44326 and shot <= 52804:
            snap_file = snap_filepath / "snap.nam_14"
            efit_exec = EFIT_ROOT / "bin/efitd129d_east_2014"
        elif shot > 52804 and shot <= 96915:
            snap_file = snap_filepath / "snap.nam_15"
            efit_exec = EFIT_ROOT / "bin/efitd129d_east_2015"
        elif shot > 96915:
            snap_file = snap_filepath / "snap.nam_21"
            efit_exec = EFIT_ROOT / "bin/efitd129d_east_2021"
        else:
            raise Exception("no such shot")

        envs = {
            "LD_LIBRARY_PATH": f"{EFIT_LIBRARY_PATH}:{os.environ.get('LD_LIBRARY_PATH')}",
        }

        with self.working_dir() as working_dir:
            # working_dir = pathlib.Path(working_dir)
            logger.debug(working_dir)

            File(working_dir / "temp", format="namelist", template=snap_file).write({"in1": mdsdata})

            pwd = os.getcwd()

            if not efit_exec.is_file():
                raise Exception(f"no such file {efit_exec}")

            try:
                procss = subprocess.run([efit_exec.as_posix()], shell=True, check=True, env=envs, cwd=working_dir)
            except Exception as error:
                # logger.debug(File(working_dir / "temp", format="namelist").read().dump())
                raise RuntimeError(f"Fail to run {efit_exec}") from error

            if procss.returncode > 0:  # for debug
                shutil.copytree(working_dir, f"{pwd}/{shot:06d}.{itime:05d}", dirs_exist_ok=True)
                logger.debug(f"OUTPUT {pwd}")

            if procss.returncode > 0:
                raise RuntimeError(f"Fail to run {efit_exec}! error code={procss.returncode}")

            output = working_dir / f"g{shot:06d}.{itime:05d}"

            if not output.exists():
                raise RuntimeError(f"Can not find output {output}")

            eq = File(output, format="GEQdsk").read().dump()
            # logger.debug(eq["equilibrium"]["time_slice"][0])

            # refresh 会触发 execute 操作，所以这里不需要再次刷新
            # update  仅仅更新当前时间点的数据，不会触发 execute 操作
            current.update(eq["equilibrium"]["time_slice"][0])

        # logger.debug(eq)

        logger.info(f"Refresh Equilibrium: {self.__class__.__name__} Done")

    # def refresh(
    #     self,
    #     *args,
    #     time: float | None = None,  # unit: s
    #     magnetics: Magnetics | None = None,
    #     pf_active: PFActive | None = None,
    #     tf: TF | None = None,
    #     wall: Wall | None = None,
    #     **kwargs,
    # ):
    #     """update the last time slice, base on profiles_2d[-1].psi, and core_profiles_1d, wall, pf_active"""

    #     super().refresh(*args, time=time, **kwargs)

    #     current_slice = self.time_slice.current

    #     if self._parent is not None:
    #         if magnetics is None:
    #             magnetics = self._parent.magnetics  # type:ignore

    #         if pf_active is None:
    #             pf_active = self._parent.pf_active  # type:ignore

    #         if tf is None:
    #             tf = self._parent.tf  # type:ignore

    #         if wall is None:
    #             wall = self._parent.wall  # type:ignore

    #     time = time or kwargs.pop("time", None) or current_slice.time

    #     eq = self._run_backend(
    #         shot=self._shot, time=time, magnetics=magnetics, pf_active=pf_active, tf=tf, wall=wall,
    #     )

    #     self.time_slice.refresh(eq["time_slice"][0])

    #     logger.info(f"Refresh Equilibrium: {self.__class__.__name__} Done")

    #     return current_slice

    # def advance(self, *args, dt=0.1, **kwargs):
    #     return super().advance(*args, **kwargs)