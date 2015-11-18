from daemon import DaemonContext

from tflrepub import do_main_program

consumerDaemonLogFile = open('consumerDaemonLogFile', 'w')

context = DaemonContext(
    stdout = consumerDaemonLogFile,
    sderr = consumerDaemonLogFile
    )

context.open()

with context:
    do_main_program()
