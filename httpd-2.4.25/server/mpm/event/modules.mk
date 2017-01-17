libevent.la: event.lo fdqueue.lo
	$(MOD_LINK) event.lo fdqueue.lo
DISTCLEAN_TARGETS = modules.mk
static = libevent.la
shared =
