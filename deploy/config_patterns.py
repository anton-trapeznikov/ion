patterns = {
    'supervisor': "[program:{daemon_name}]\n"
                  "directory={directory}\n"
                  "command={exec_command}\n"
                  "user={user}\n"
                  "group={user_group}\n"
                  "autostart=true\n"
                  "autorestart=true\n"
                  "startretries=5\n"
                  "redirect_stderr=false\n"
                  "stdout_logfile={stdout_logfile}\n"
                  "stdout_logfile_maxbytes=1MB\n"
                  "stdout_logfile_backups=10\n"
                  "stdout_capture_maxbytes=1MB\n"
                  "stderr_logfile={stderr_logfile}\n"
                  "stderr_logfile_maxbytes=1MB\n"
                  "stderr_logfile_backups=10\n"
                  "stderr_capture_maxbytes=1MB\n",
}
