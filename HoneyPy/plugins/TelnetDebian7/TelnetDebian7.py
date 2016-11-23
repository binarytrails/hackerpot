from twisted.internet import protocol, reactor, endpoints, defer
from twisted.python import log
import uuid

from HackerPot import HackerPot

class TelnetDebian7(protocol.Protocol): ### Set custom protocol class name
	localhost   = None
	remote_host = None
	session     = None

	state = 'INIT'
	uname = None
	pword = None

        def __init__(self, factory, iotPot):
            self.factory = factory
            self.iotPot = iotPot

	def connectionMade(self):
		self.connect()
                self.tx('Debian GNU/Linux 7\r\n')

	def dataReceived(self, data):
		self.rx(data)

                if 'INIT' == self.state:
			self.state = 'NO_UNAME'
			self.tx('Login: ')
		elif 'NO_UNAME' == self.state:
			self.uname = data.strip()
			if len(self.uname) > 0:
				self.state = 'NO_PWORD'
				self.tx('Password: ')
			else:
				self.tx('Login: ')
		elif 'NO_PWORD' == self.state:
			self.pword = data.rstrip()
			if self.authn(self.pword):
				self.state = 'COMMAND'
				self.tx(self.uname + '$ ')
			else:
				self.state = 'NO_UNAME'
				self.tx('Login incorrect\n')
				self.tx('Login: ')
		elif 'COMMAND' == self.state:
			# parse command
			commandParts = str(data).split()

			if 0 == len(commandParts):
				self.tx(self.uname + '$ ')
			else:
				command      = commandParts[0].lower()
				args         = commandParts[1:]

				try:
					method = getattr(self, 'do_' + command)
				except AttributeError, e:
					self.tx('- bash: ' + command + ': command not found\r\n')
					self.tx(self.uname + '$ ')
				else:
					try:
						method(*args)
						self.tx(self.uname + '$ ')
					except Exception, e:
						self.tx('WARNING: System error, closing connection.\n')
						self.transport.loseConnection()
		else:
			# should never reach here
			self.tx('WARNING: System error, closing connection.\n')
			self.transport.loseConnection()

	def authn(self, password=None):
		authenticated = False

		if 'admin' == password or 'root' == password or 'god' == password:
			authenticated = True
		        self.iotPot.intrusion(self.transport.getPeer())

		return authenticated

	def do_exit(self, args=None):
		self.transport.loseConnection()

	def do_whoami(self, args=None):
		self.tx(self.uname)

	def do_uname(self, args=None):
		self.tx('Linux bitminer 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt9-3~deb8u1 (2015-04-24) x86_64 GNU/Linux\r\n')

	def do_which(self, args=None):
		if None != args:
			command = args.split()
			self.tx('/bin/' + command[0] + '\r\n')

	def connect(self):
		self.local_host  = self.transport.getHost()
		self.remote_host = self.transport.getPeer()
		self.session     = uuid.uuid1()

                self.iotPot.connection(self.remote_host)

		log.msg('%s %s CONNECT %s %s %s %s %s' % (
                    self.session, self.remote_host.type, self.local_host.host,
                    self.local_host.port, self.factory.name,
                    self.remote_host.host, self.remote_host.port))

	def tx(self, data):
		log.msg('%s %s TX %s %s %s %s %s %s' % (self.session,
                    self.remote_host.type, self.local_host.host,
                    self.local_host.port, self.factory.name,
                    self.remote_host.host, self.remote_host.port,
                    data.encode("hex")))

                self.transport.write(data)

	def rx(self, data):
		log.msg('%s %s RX %s %s %s %s %s %s' % (self.session,
                    self.remote_host.type, self.local_host.host,
                    self.local_host.port, self.factory.name,
                    self.remote_host.host, self.remote_host.port,
                    data.encode("hex")))

class pluginFactory(protocol.Factory):
	protocol = TelnetDebian7

	def __init__(self, name, iotPot):
		self.name = name
                self.iotPot = iotPot

        def buildProtocol(self, addr):
            return TelnetDebian7(self, self.iotPot)

