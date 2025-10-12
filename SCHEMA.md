

schema_version: "String"

timestamp_iso: POSIX (INT)

cpu: Percent (double)

memory: mb (double)

disks: list: name(string), mb (double)

processes: list: PID(int), TTY(string), time(posix[int]), name(string), 