# -*- coding: GBK -*-

MSG_CS_LOGIN	= 0x1001
MSG_SC_CONFIRM	= 0x2001

MSG_CS_MOVETO	= 0x1002
MSG_SC_MOVETO	= 0x2002

NET_STATE_STOP	= 0				# state: init value
NET_STATE_CONNECTING	= 1		# state: connecting
NET_STATE_ESTABLISHED	= 2		# state: connected

NET_HEAD_LENGTH_SIZE	= 1		# 4 bytes little endian (x86)
NET_HEAD_LENGTH_FORMAT	= '<I'

NET_CONNECTION_NEW	= 0	# new connection
NET_CONNECTION_LEAVE	= 1	# lost connection
NET_CONNECTION_DATA	= 2	# data comming

NET_HOST_DEFAULT_TIMEOUT	= 70

MAX_HOST_CLIENTS_INDEX	= 0xffff
MAX_HOST_CLIENTS_BYTES	= 16

MSG_UNMEANING = 0
MSG_REGISTER = 1
MSG_LOGIN = 2
MSG_LOBBY = 3
MSG_RECONNECT = 4
MSG_GAME = 5
MSG_SYNCHRONIZATION = 6

MSG_SYN_DELAY = 1
MSG_SYN_TIME = 2

MSG_LOBBY_CREATEROOM = 1
MSG_LOBBY_JOINROOM = 2
MSG_LOBBY_QUITROOM = 3
MSG_LOBBY_GETROOMMSG = 4
MSG_LOBBY_READY = 5
MSG_LOBBY_START = 6

MSG_GAME_UPDATE = 1
MSG_GAME_QUIT = 2
MSG_GAME_LOAD = 3

MSG_GAME_UPDATE_CHANGEMOTION = 1
MSG_GAME_UPDATE_CHANGEMOVE = 2
MSG_GAME_UPDATE_CHANGEATTACK = 3
MSG_GAME_UPDATE_CHANGEROT = 4
MSG_GAME_UPDATE_CHANGELOOK = 5
MSG_GAME_UPDATE_DAMAGE = 6
MSG_GAME_UPDATE_PROP = 7

USER_STATE_LOBBY = 0
USER_STATE_ROOM = 1
USER_STATE_GAME = 2
