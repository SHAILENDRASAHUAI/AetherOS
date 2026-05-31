#include <tunables/global>

/usr/bin/python3 /opt/aetheros/ai-core/aether_daemon.py {
  #include <abstractions/base>
  #include <abstractions/python>

  /opt/aetheros/ai-core/** r,
  /run/aetheros-ai.sock rw,
  deny /** wklx,
}
