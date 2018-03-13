c.NotebookApp.session_manager_class = 'nb2kg.managers.SessionManager'
c.NotebookApp.kernel_manager_class = 'nb2kg.managers.RemoteKernelManager'
c.NotebookApp.kernel_spec_manager_class = 'nb2kg.managers.RemoteKernelSpecManager'

import logging
c.NotebookApp.log_level=logging.DEBUG
