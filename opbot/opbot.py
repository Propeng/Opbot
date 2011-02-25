import socket, random, time, sys
#Opbot modules
import options

class Opbot():
  def __init__(self):
    #initializing and connecting to IRC server
    self.randnum = random.randint(1, 10000)
    self.shutdowncmd = "!die " + str(self.randnum)
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.irc.connect ((options.network, options.port))

    #identifying
    self.send("NICK %s" % options.botnick)
    self.send("USER %s %s %s :%s" % (options.botuser, options.network, options.network, options.botreal))
    time.sleep(0.5)

  def send(self, msg):
    print "[OUT] %s" % msg
    self.irc.send("%s\r\n" % msg)

  def parseline(self, line):
    colonSplit = line.partition(" :")
    isColonSplit = False
    if colonSplit[1] == ' :':
      isColonSplit = True

    spaceSplit = colonSplit[0].split(' ')
    if isColonSplit:
      spaceSplit.append(colonSplit[2])

    args = spaceSplit
    command = args[0]
    args.pop(0)

    return (command, args)

  def parsemask(self, hostmask):
    nickSplit = hostmask.partition("!")
    hostSplit = nickSplit[2].partition("@")

    nick = nickSplit[0]
    user = hostSplit[0]
    host = hostSplit[2]

    if user == "":
      userSplit = nick.partition("@")
      nick = ""
      user = userSplit[0]
      host = userSplit[2]

    return (nick, user, host)

  def listen(self):
    #socket receive loop
    while True:
      raw = self.irc.recv(4096)
      lines = raw.splitlines()

      for line in lines: #TODO: IMPORTANT: correct argument parsing
        print "[IN ] %s" % line
        command, args = self.parseline(line)

        #pings and pongs
        if command == "PING":
          self.send("PONG :%s" % args[0])

        #joining channels
        if line.find("376") != -1:
          self.send("PRIVMSG %s :The random number is %d" % (options.owner, self.randnum))
          self.send("JOIN %s" % options.channel)

        #random number shutdown
        if line.find(self.shutdowncmd) != -1:
          self.send("QUIT :by direct order")
          sys.exit()

        #denying access
        if line.find("!die") != -1:
          self.send("PRIVMSG %s :Access denied. This incident will be reported." % options.channel)
          self.send("PRIVMSG %s :Someone tried to shut me down!" % options.owner)

        #rejoin on kick
        if line.find("KICK") != -1:
          self.send("JOIN %s" % options.channel)
