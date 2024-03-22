#! /usr/bin/env python3

import os
import fire
import time
import subprocess

from loguru import logger

class Make:
    def all(self):
        self.coremark(parallel=os.cpu_count())
        self.coremarkpro(parallel=os.cpu_count())

    def stress(self):
        while True:
            self.all()

    def coremark(self, parallel: int = 1, iterations: int = 0):
        opath = "../"
        cmd = 'cd coremark'
        cmd += f'&& make XCFLAGS="-DMULTITHREAD={parallel} -DUSE_PTHREAD -pthread" OPATH={opath} ITERATIONS={iterations}'
        self._run(cmd)

    def coremarkpro(self, parallel: int = 1):
        cmd = f"cd coremark-pro && make TARGET=linux64 build && make TARGET=linux64 XCMD='-c{parallel}' certify-all"
        self._run(cmd)
    
    def _run(self, cmd: str):
        logger.debug(f"Command = {cmd}")
        start_time = time.time()
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        # result = subprocess.check_output(cmd, shell=True)
        logger.trace(f"STDOUT = {result.stdout}")
        logger.trace(f"STDERR = {result.stderr}")
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Execution time = {duration}")
        return result

if __name__ == "__main__":
    fire.Fire(Make)